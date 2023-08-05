#
# The Python Imaging Library.
# $Id$
#
# IPTC/NAA file handling
#
# history:
# 1995-10-01 fl   Created
# 1998-03-09 fl   Cleaned up and added to PIL
# 2002-06-18 fl   Added getiptcinfo helper
#
# Copyright (c) Secret Labs AB 1997-2002.
# Copyright (c) Fredrik Lundh 1995.
#
# See the README file for information on usage and redistribution.
#

from __future__ import print_function

from PIL import Image, ImageFile, _binary
import os
import tempfile

__version__ = "0.3"

i8 = _binary.i8
i16 = _binary.i16be
i32 = _binary.i32be
o8 = _binary.o8

COMPRESSION = {
    1: "raw",
    5: "jpeg"
}

PAD = o8(0) * 4


#
# Helpers

def i(c):
    return i32((PAD + c)[-4:])


def dump(c):
    for i in c:
        print("%02x" % i8(i), end=' ')
    print()


##
# Image plugin for IPTC/NAA datastreams.  To read IPTC/NAA fields
# from TIFF and JPEG files, use the <b>getiptcinfo</b> function.

class IptcImageFile(ImageFile.ImageFile):

    format = "IPTC"
    format_description = "IPTC/NAA"

    def getint(self, key):
        return i(self.info[key])

    def field(self):
        #
        # get a IPTC field header
        s = self.fp.read(5)
        if not len(s):
            return None, 0

        tag = i8(s[1]), i8(s[2])

        # syntax
        if i8(s[0]) != 0x1C or tag[0] < 1 or tag[0] > 9:
            raise SyntaxError("invalid IPTC/NAA file")

        # field size
        size = i8(s[3])
        if size > 132:
            raise IOError("illegal field length in IPTC/NAA file")
        elif size == 128:
            size = 0
        elif size > 128:
            size = i(self.fp.read(size-128))
        else:
            size = i16(s[3:])

        return tag, size

    def _open(self):

        # load descriptive fields
        while True:
            offset = self.fp.tell()
            tag, size = self.field()
            if not tag or tag == (8, 10):
                break
            if size:
                tagdata = self.fp.read(size)
            else:
                tagdata = None
            if tag in list(self.info.keys()):
                if isinstance(self.info[tag], list):
                    self.info[tag].append(tagdata)
                else:
                    self.info[tag] = [self.info[tag], tagdata]
            else:
                self.info[tag] = tagdata

            # print tag, self.info[tag]

        # mode
        layers = i8(self.info[(3, 60)][0])
        component = i8(self.info[(3, 60)][1])
        if (3, 65) in self.info:
            id = i8(self.info[(3, 65)][0])-1
        else:
            id = 0
        if layers == 1 and not component:
            self.mode = "L"
        elif layers == 3 and component:
            self.mode = "RGB"[id]
        elif layers == 4 and component:
            self.mode = "CMYK"[id]

        # size
        self.size = self.getint((3, 20)), self.getint((3, 30))

        # compression
        try:
            compression = COMPRESSION[self.getint((3, 120))]
        except KeyError:
            raise IOError("Unknown IPTC image compression")

        # tile
        if tag == (8, 10):
            self.tile = [("iptc", (compression, offset),
                         (0, 0, self.size[0], self.size[1]))]

    def load(self):

        if len(self.tile) != 1 or self.tile[0][0] != "iptc":
            return ImageFile.ImageFile.load(self)

        type, tile, box = self.tile[0]

        encoding, offset = tile

        self.fp.seek(offset)

        # Copy image data to temporary file
        o_fd, outfile = tempfile.mkstemp(text=False)
        o = os.fdopen(o_fd)
        if encoding == "raw":
            # To simplify access to the extracted file,
            # prepend a PPM header
            o.write("P5\n%d %d\n255\n" % self.size)
        while True:
            type, size = self.field()
            if type != (8, 10):
                break
            while size > 0:
                s = self.fp.read(min(size, 8192))
                if not s:
                    break
                o.write(s)
                size -= len(s)
        o.close()

        try:
            try:
                # fast
                self.im = Image.core.open_ppm(outfile)
            except:
                # slightly slower
                im = Image.open(outfile)
                im.load()
                self.im = im.im
        finally:
            try:
                os.unlink(outfile)
            except OSError:
                pass


Image.register_open(IptcImageFile.format, IptcImageFile)

Image.register_extension(IptcImageFile.format, ".iim")


##
# Get IPTC information from TIFF, JPEG, or IPTC file.
#
# @param im An image containing IPTC data.
# @return A dictionary containing IPTC information, or None if
#     no IPTC information block was found.

def getiptcinfo(im):

    from PIL import TiffImagePlugin, JpegImagePlugin
    import io

    data = None

    if isinstance(im, IptcImageFile):
        # return info dictionary right away
        return im.info

    elif isinstance(im, JpegImagePlugin.JpegImageFile):
        # extract the IPTC/NAA resource
        try:
            app = im.app["APP13"]
            if app[:14] == b"Photoshop 3.0\x00":
                app = app[14:]
                # parse the image resource block
                offset = 0
                while app[offset:offset+4] == b"8BIM":
                    offset += 4
                    # resource code
                    code = i16(app, offset)
                    offset += 2
                    # resource name (usually empty)
                    name_len = i8(app[offset])
                    # name = app[offset+1:offset+1+name_len]
                    offset = 1 + offset + name_len
                    if offset & 1:
                        offset += 1
                    # resource data block
                    size = i32(app, offset)
                    offset += 4
                    if code == 0x0404:
                        # 0x0404 contains IPTC/NAA data
                        data = app[offset:offset+size]
                        break
                    offset = offset + size
                    if offset & 1:
                        offset += 1
        except (AttributeError, KeyError):
            pass

    elif isinstance(im, TiffImagePlugin.TiffImageFile):
        # get raw data from the IPTC/NAA tag (PhotoShop tags the data
        # as 4-byte integers, so we cannot use the get method...)
        try:
            data = im.tag.tagdata[TiffImagePlugin.IPTC_NAA_CHUNK]
        except (AttributeError, KeyError):
            pass

    if data is None:
        return None  # no properties

    # create an IptcImagePlugin object without initializing it
    class FakeImage(object):
        pass
    im = FakeImage()
    im.__class__ = IptcImageFile

    # parse the IPTC information chunk
    im.info = {}
    im.fp = io.BytesIO(data)

    try:
        im._open()
    except (IndexError, KeyError):
        pass  # expected failure

    return im.info
