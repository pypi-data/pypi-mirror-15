/*
 * The Python Imaging Library.
 * $Id$
 *
 * decoder for JPEG2000 image data.
 *
 * history:
 * 2014-03-12 ajh  Created
 *
 * Copyright (c) 2014 Coriolis Systems Limited
 * Copyright (c) 2014 Alastair Houghton
 *
 * See the README file for details on usage and redistribution.
 */

#include "Imaging.h"

#ifdef HAVE_OPENJPEG

#include <stdlib.h>
#include "Jpeg2K.h"

typedef struct {
    OPJ_UINT32 tile_index;
    OPJ_UINT32 data_size;
    OPJ_INT32  x0, y0, x1, y1;
    OPJ_UINT32 nb_comps;
} JPEG2KTILEINFO;

/* -------------------------------------------------------------------- */
/* Error handler                                                        */
/* -------------------------------------------------------------------- */

static void
j2k_error(const char *msg, void *client_data)
{
    JPEG2KDECODESTATE *state = (JPEG2KDECODESTATE *) client_data;
    free((void *)state->error_msg);
    state->error_msg = strdup(msg);
}

/* -------------------------------------------------------------------- */
/* Buffer input stream                                                  */
/* -------------------------------------------------------------------- */

static OPJ_SIZE_T
j2k_read(void *p_buffer, OPJ_SIZE_T p_nb_bytes, void *p_user_data)
{
    ImagingIncrementalCodec decoder = (ImagingIncrementalCodec)p_user_data;

    size_t len = ImagingIncrementalCodecRead(decoder, p_buffer, p_nb_bytes);

    return len ? len : (OPJ_SIZE_T)-1;
}

static OPJ_OFF_T
j2k_skip(OPJ_OFF_T p_nb_bytes, void *p_user_data)
{
    ImagingIncrementalCodec decoder = (ImagingIncrementalCodec)p_user_data;
    off_t pos = ImagingIncrementalCodecSkip(decoder, p_nb_bytes);

    return pos ? pos : (OPJ_OFF_T)-1;
}

/* -------------------------------------------------------------------- */
/* Unpackers                                                            */
/* -------------------------------------------------------------------- */

typedef void (*j2k_unpacker_t)(opj_image_t *in,
                               const JPEG2KTILEINFO *tileInfo,
                               const UINT8 *data,
                               Imaging im);

struct j2k_decode_unpacker {
    const char          *mode;
    OPJ_COLOR_SPACE     color_space;
    unsigned            components;
    j2k_unpacker_t      unpacker;
};

static inline
unsigned j2ku_shift(unsigned x, int n)
{
    if (n < 0)
        return x >> -n;
    else
        return x << n;
}

static void
j2ku_gray_l(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
            const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shift = 8 - in->comps[0].prec;
    int offset = in->comps[0].sgnd ? 1 << (in->comps[0].prec - 1) : 0;
    int csiz = (in->comps[0].prec + 7) >> 3;

    unsigned x, y;

    if (csiz == 3)
        csiz = 4;

    if (shift < 0)
        offset += 1 << (-shift - 1);

    switch (csiz) {
    case 1:
        for (y = 0; y < h; ++y) {
            const UINT8 *data = &tiledata[y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    case 2:
        for (y = 0; y < h; ++y) {
            const UINT16 *data = (const UINT16 *)&tiledata[2 * y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    case 4:
        for (y = 0; y < h; ++y) {
            const UINT32 *data = (const UINT32 *)&tiledata[4 * y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    }
}


static void
j2ku_gray_i(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
            const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shift = 16 - in->comps[0].prec;
    int offset = in->comps[0].sgnd ? 1 << (in->comps[0].prec - 1) : 0;
    int csiz = (in->comps[0].prec + 7) >> 3;

    unsigned x, y;

    if (csiz == 3)
        csiz = 4;

    if (shift < 0)
        offset += 1 << (-shift - 1);

    switch (csiz) {
    case 1:
        for (y = 0; y < h; ++y) {
            const UINT8 *data = &tiledata[y * w];
            UINT16 *row = (UINT16 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    case 2:
        for (y = 0; y < h; ++y) {
            const UINT16 *data = (const UINT16 *)&tiledata[2 * y * w];
            UINT16 *row = (UINT16 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    case 4:
        for (y = 0; y < h; ++y) {
            const UINT32 *data = (const UINT32 *)&tiledata[4 * y * w];
            UINT16 *row = (UINT16 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x)
                *row++ = j2ku_shift(offset + *data++, shift);
        }
        break;
    }
}


static void
j2ku_gray_rgb(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
              const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shift = 8 - in->comps[0].prec;
    int offset = in->comps[0].sgnd ? 1 << (in->comps[0].prec - 1) : 0;
    int csiz = (in->comps[0].prec + 7) >> 3;

    unsigned x, y;

    if (shift < 0)
        offset += 1 << (-shift - 1);

    if (csiz == 3)
        csiz = 4;

    switch (csiz) {
    case 1:
        for (y = 0; y < h; ++y) {
            const UINT8 *data = &tiledata[y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x) {
                UINT8 byte = j2ku_shift(offset + *data++, shift);
                row[0] = row[1] = row[2] = byte;
                row[3] = 0xff;
                row += 4;
            }
        }
        break;
    case 2:
        for (y = 0; y < h; ++y) {
            const UINT16 *data = (UINT16 *)&tiledata[2 * y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x) {
                UINT8 byte = j2ku_shift(offset + *data++, shift);
                row[0] = row[1] = row[2] = byte;
                row[3] = 0xff;
                row += 4;
            }
        }
        break;
    case 4:
        for (y = 0; y < h; ++y) {
            const UINT32 *data = (UINT32 *)&tiledata[4 * y * w];
            UINT8 *row = (UINT8 *)im->image[y0 + y] + x0;
            for (x = 0; x < w; ++x) {
                UINT8 byte = j2ku_shift(offset + *data++, shift);
                row[0] = row[1] = row[2] = byte;
                row[3] = 0xff;
                row += 4;
            }
        }
        break;
    }
}

static void
j2ku_graya_la(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
              const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shift = 8 - in->comps[0].prec;
    int offset = in->comps[0].sgnd ? 1 << (in->comps[0].prec - 1) : 0;
    int csiz = (in->comps[0].prec + 7) >> 3;
    int ashift = 8 - in->comps[1].prec;
    int aoffset = in->comps[1].sgnd ? 1 << (in->comps[1].prec - 1) : 0;
    int acsiz = (in->comps[1].prec + 7) >> 3;
    const UINT8 *atiledata;

    unsigned x, y;

    if (csiz == 3)
        csiz = 4;
    if (acsiz == 3)
        acsiz = 4;

    if (shift < 0)
        offset += 1 << (-shift - 1);
    if (ashift < 0)
        aoffset += 1 << (-ashift - 1);

    atiledata = tiledata + csiz * w * h;

    for (y = 0; y < h; ++y) {
        const UINT8 *data = &tiledata[csiz * y * w];
        const UINT8 *adata = &atiledata[acsiz * y * w];
        UINT8 *row = (UINT8 *)im->image[y0 + y] + x0 * 4;
        for (x = 0; x < w; ++x) {
            UINT32 word = 0, aword = 0, byte;

            switch (csiz) {
            case 1: word = *data++; break;
            case 2: word = *(const UINT16 *)data; data += 2; break;
            case 4: word = *(const UINT32 *)data; data += 4; break;
            }

            switch (acsiz) {
            case 1: aword = *adata++; break;
            case 2: aword = *(const UINT16 *)adata; adata += 2; break;
            case 4: aword = *(const UINT32 *)adata; adata += 4; break;
            }

            byte = j2ku_shift(offset + word, shift);
            row[0] = row[1] = row[2] = byte;
            row[3] = j2ku_shift(aoffset + aword, ashift);
            row += 4;
        }
    }
}

static void
j2ku_srgb_rgb(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
              const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shifts[3], offsets[3], csiz[3];
    const UINT8 *cdata[3];
    const UINT8 *cptr = tiledata;
    unsigned n, x, y;

    for (n = 0; n < 3; ++n) {
        cdata[n] = cptr;
        shifts[n] = 8 - in->comps[n].prec;
        offsets[n] = in->comps[n].sgnd ? 1 << (in->comps[n].prec - 1) : 0;
        csiz[n] = (in->comps[n].prec + 7) >> 3;

        if (csiz[n] == 3)
            csiz[n] = 4;

        if (shifts[n] < 0)
            offsets[n] += 1 << (-shifts[n] - 1);

        cptr += csiz[n] * w * h;
    }

    for (y = 0; y < h; ++y) {
        const UINT8 *data[3];
        UINT8 *row = (UINT8 *)im->image[y0 + y] + x0 * 4;
        for (n = 0; n < 3; ++n)
            data[n] = &cdata[n][csiz[n] * y * w];
        
        for (x = 0; x < w; ++x) {
            for (n = 0; n < 3; ++n) {
                UINT32 word = 0;

                switch (csiz[n]) {
                case 1: word = *data[n]++; break;
                case 2: word = *(const UINT16 *)data[n]; data[n] += 2; break;
                case 4: word = *(const UINT32 *)data[n]; data[n] += 4; break;
                }

                row[n] = j2ku_shift(offsets[n] + word, shifts[n]);
            }
            row[3] = 0xff;
            row += 4;
        }
    }
}

static void
j2ku_sycc_rgb(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
              const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shifts[3], offsets[3], csiz[3];
    const UINT8 *cdata[3];
    const UINT8 *cptr = tiledata;
    unsigned n, x, y;

    for (n = 0; n < 3; ++n) {
        cdata[n] = cptr;
        shifts[n] = 8 - in->comps[n].prec;
        offsets[n] = in->comps[n].sgnd ? 1 << (in->comps[n].prec - 1) : 0;
        csiz[n] = (in->comps[n].prec + 7) >> 3;

        if (csiz[n] == 3)
            csiz[n] = 4;

        if (shifts[n] < 0)
            offsets[n] += 1 << (-shifts[n] - 1);

        cptr += csiz[n] * w * h;
    }

    for (y = 0; y < h; ++y) {
        const UINT8 *data[3];
        UINT8 *row = (UINT8 *)im->image[y0 + y] + x0 * 4;
        UINT8 *row_start = row;
        for (n = 0; n < 3; ++n)
            data[n] = &cdata[n][csiz[n] * y * w];
        
        for (x = 0; x < w; ++x) {
            for (n = 0; n < 3; ++n) {
                UINT32 word = 0;

                switch (csiz[n]) {
                case 1: word = *data[n]++; break;
                case 2: word = *(const UINT16 *)data[n]; data[n] += 2; break;
                case 4: word = *(const UINT32 *)data[n]; data[n] += 4; break;
                }

                row[n] = j2ku_shift(offsets[n] + word, shifts[n]);
            }
            row[3] = 0xff;
            row += 4;
        }

        ImagingConvertYCbCr2RGB(row_start, row_start, w);
    }
}

static void
j2ku_srgba_rgba(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
                const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shifts[4], offsets[4], csiz[4];
    const UINT8 *cdata[4];
    const UINT8 *cptr = tiledata;
    unsigned n, x, y;

    for (n = 0; n < 4; ++n) {
        cdata[n] = cptr;
        shifts[n] = 8 - in->comps[n].prec;
        offsets[n] = in->comps[n].sgnd ? 1 << (in->comps[n].prec - 1) : 0;
        csiz[n] = (in->comps[n].prec + 7) >> 3;

        if (csiz[n] == 3)
            csiz[n] = 4;

        if (shifts[n] < 0)
            offsets[n] += 1 << (-shifts[n] - 1);

        cptr += csiz[n] * w * h;
    }

    for (y = 0; y < h; ++y) {
        const UINT8 *data[4];
        UINT8 *row = (UINT8 *)im->image[y0 + y] + x0 * 4;
        for (n = 0; n < 4; ++n)
            data[n] = &cdata[n][csiz[n] * y * w];
        
        for (x = 0; x < w; ++x) {
            for (n = 0; n < 4; ++n) {
                UINT32 word = 0;

                switch (csiz[n]) {
                case 1: word = *data[n]++; break;
                case 2: word = *(const UINT16 *)data[n]; data[n] += 2; break;
                case 4: word = *(const UINT32 *)data[n]; data[n] += 4; break;
                }

                row[n] = j2ku_shift(offsets[n] + word, shifts[n]);
            }
            row += 4;
        }
    }
}

static void
j2ku_sycca_rgba(opj_image_t *in, const JPEG2KTILEINFO *tileinfo,
                const UINT8 *tiledata, Imaging im)
{
    unsigned x0 = tileinfo->x0 - in->x0, y0 = tileinfo->y0 - in->y0;
    unsigned w = tileinfo->x1 - tileinfo->x0;
    unsigned h = tileinfo->y1 - tileinfo->y0;

    int shifts[4], offsets[4], csiz[4];
    const UINT8 *cdata[4];
    const UINT8 *cptr = tiledata;
    unsigned n, x, y;

    for (n = 0; n < 4; ++n) {
        cdata[n] = cptr;
        shifts[n] = 8 - in->comps[n].prec;
        offsets[n] = in->comps[n].sgnd ? 1 << (in->comps[n].prec - 1) : 0;
        csiz[n] = (in->comps[n].prec + 7) >> 3;

        if (csiz[n] == 3)
            csiz[n] = 4;

        if (shifts[n] < 0)
            offsets[n] += 1 << (-shifts[n] - 1);

        cptr += csiz[n] * w * h;
    }

    for (y = 0; y < h; ++y) {
        const UINT8 *data[4];
        UINT8 *row = (UINT8 *)im->image[y0 + y] + x0 * 4;
        UINT8 *row_start = row;
        for (n = 0; n < 4; ++n)
            data[n] = &cdata[n][csiz[n] * y * w];
        
        for (x = 0; x < w; ++x) {
            for (n = 0; n < 4; ++n) {
                UINT32 word = 0;

                switch (csiz[n]) {
                case 1: word = *data[n]++; break;
                case 2: word = *(const UINT16 *)data[n]; data[n] += 2; break;
                case 4: word = *(const UINT32 *)data[n]; data[n] += 4; break;
                }

                row[n] = j2ku_shift(offsets[n] + word, shifts[n]);
            }
            row += 4;
        }

        ImagingConvertYCbCr2RGB(row_start, row_start, w);
    }
}

static const struct j2k_decode_unpacker j2k_unpackers[] = {
    { "L", OPJ_CLRSPC_GRAY, 1, j2ku_gray_l },
    { "I;16", OPJ_CLRSPC_GRAY, 1, j2ku_gray_i },
    { "I;16B", OPJ_CLRSPC_GRAY, 1, j2ku_gray_i },
    { "LA", OPJ_CLRSPC_GRAY, 2, j2ku_graya_la },
    { "RGB", OPJ_CLRSPC_GRAY, 1, j2ku_gray_rgb },
    { "RGB", OPJ_CLRSPC_GRAY, 2, j2ku_gray_rgb },
    { "RGB", OPJ_CLRSPC_SRGB, 3, j2ku_srgb_rgb },
    { "RGB", OPJ_CLRSPC_SYCC, 3, j2ku_sycc_rgb },
    { "RGB", OPJ_CLRSPC_SRGB, 4, j2ku_srgb_rgb },
    { "RGB", OPJ_CLRSPC_SYCC, 4, j2ku_sycc_rgb },
    { "RGBA", OPJ_CLRSPC_GRAY, 1, j2ku_gray_rgb },
    { "RGBA", OPJ_CLRSPC_GRAY, 2, j2ku_graya_la },
    { "RGBA", OPJ_CLRSPC_SRGB, 3, j2ku_srgb_rgb },
    { "RGBA", OPJ_CLRSPC_SYCC, 3, j2ku_sycc_rgb },
    { "RGBA", OPJ_CLRSPC_SRGB, 4, j2ku_srgba_rgba },
    { "RGBA", OPJ_CLRSPC_SYCC, 4, j2ku_sycca_rgba },
};

/* -------------------------------------------------------------------- */
/* Decoder                                                              */
/* -------------------------------------------------------------------- */

enum {
    J2K_STATE_START = 0,
    J2K_STATE_DECODING = 1,
    J2K_STATE_DONE = 2,
    J2K_STATE_FAILED = 3,
};

static int
j2k_decode_entry(Imaging im, ImagingCodecState state,
                 ImagingIncrementalCodec decoder)
{
    JPEG2KDECODESTATE *context = (JPEG2KDECODESTATE *) state->context;
    opj_stream_t *stream = NULL;
    opj_image_t *image = NULL;
    opj_codec_t *codec = NULL;
    opj_dparameters_t params;
    OPJ_COLOR_SPACE color_space;
    j2k_unpacker_t unpack = NULL;
    size_t buffer_size = 0;
    unsigned n;

    stream = opj_stream_default_create(OPJ_TRUE);

    if (!stream) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }

    opj_stream_set_read_function(stream, j2k_read);
    opj_stream_set_skip_function(stream, j2k_skip);

    /* OpenJPEG 2.0 doesn't have OPJ_VERSION_MAJOR */
#ifndef OPJ_VERSION_MAJOR
    opj_stream_set_user_data(stream, decoder);
#else
    opj_stream_set_user_data(stream, decoder, NULL);

    /* Hack: if we don't know the length, the largest file we can
       possibly support is 4GB.  We can't go larger than this, because
       OpenJPEG truncates this value for the final box in the file, and
       the box lengths in OpenJPEG are currently 32 bit. */
    if (context->length < 0)
        opj_stream_set_user_data_length(stream, 0xffffffff);
    else
        opj_stream_set_user_data_length(stream, context->length);
#endif

    /* Setup decompression context */
    context->error_msg = NULL;
    
    opj_set_default_decoder_parameters(&params);
    params.cp_reduce = context->reduce;
    params.cp_layer = context->layers;
    
    codec = opj_create_decompress(context->format);
    
    if (!codec) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }

    opj_set_error_handler(codec, j2k_error, context);
    opj_setup_decoder(codec, &params);

    if (!opj_read_header(stream, codec, &image)) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }

    /* Check that this image is something we can handle */
    if (image->numcomps < 1 || image->numcomps > 4
        || image->color_space == OPJ_CLRSPC_UNKNOWN) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }
    
    for (n = 1; n < image->numcomps; ++n) {
        if (image->comps[n].dx != 1 || image->comps[n].dy != 1) {
            state->errcode = IMAGING_CODEC_BROKEN;
            state->state = J2K_STATE_FAILED;
            goto quick_exit;
        }
    }
    
    /*
         Colorspace    Number of components    PIL mode
       ------------------------------------------------------
         sRGB          3                       RGB
         sRGB          4                       RGBA
         gray          1                       L or I
         gray          2                       LA
         YCC           3                       YCbCr
       
       
       If colorspace is unspecified, we assume:
       
           Number of components   Colorspace
         -----------------------------------------
           1                      gray
           2                      gray (+ alpha)
           3                      sRGB
           4                      sRGB (+ alpha)
       
    */
    
    /* Find the correct unpacker */
    color_space = image->color_space;
    
    if (color_space == OPJ_CLRSPC_UNSPECIFIED) {
        switch (image->numcomps) {
        case 1: case 2: color_space = OPJ_CLRSPC_GRAY; break;
        case 3: case 4: color_space = OPJ_CLRSPC_SRGB; break;
        }
    }

    for (n = 0; n < sizeof(j2k_unpackers) / sizeof (j2k_unpackers[0]); ++n) {
        if (color_space == j2k_unpackers[n].color_space
            && image->numcomps == j2k_unpackers[n].components
            && strcmp (im->mode, j2k_unpackers[n].mode) == 0) {
            unpack = j2k_unpackers[n].unpacker;
            break;
        }
    }

    if (!unpack) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }

    /* Decode the image tile-by-tile; this means we only need use as much
       memory as is required for one tile's worth of components. */
    for (;;) {
        JPEG2KTILEINFO tile_info;
        OPJ_BOOL should_continue;
        unsigned correction = (1 << params.cp_reduce) - 1;

        if (!opj_read_tile_header(codec,
                                  stream,
                                  &tile_info.tile_index,
                                  &tile_info.data_size,
                                  &tile_info.x0, &tile_info.y0,
                                  &tile_info.x1, &tile_info.y1,
                                  &tile_info.nb_comps,
                                  &should_continue)) {
            state->errcode = IMAGING_CODEC_BROKEN;
            state->state = J2K_STATE_FAILED;
            goto quick_exit;
        }

        if (!should_continue)
            break;

        /* Adjust the tile co-ordinates based on the reduction (OpenJPEG
           doesn't do this for us) */
        tile_info.x0 = (tile_info.x0 + correction) >> context->reduce;
        tile_info.y0 = (tile_info.y0 + correction) >> context->reduce;
        tile_info.x1 = (tile_info.x1 + correction) >> context->reduce;
        tile_info.y1 = (tile_info.y1 + correction) >> context->reduce;

        if (buffer_size < tile_info.data_size) {
            UINT8 *new = realloc (state->buffer, tile_info.data_size);
            if (!new) {
                state->errcode = IMAGING_CODEC_MEMORY;
                state->state = J2K_STATE_FAILED;
                goto quick_exit;
            }
            state->buffer = new;
            buffer_size = tile_info.data_size;
        }

        if (!opj_decode_tile_data(codec,
                                  tile_info.tile_index,
                                  (OPJ_BYTE *)state->buffer,
                                  tile_info.data_size,
                                  stream)) {
            state->errcode = IMAGING_CODEC_BROKEN;
            state->state = J2K_STATE_FAILED;
            goto quick_exit;
        }

        /* Check the tile bounds; if the tile is outside the image area,
           or if it has a negative width or height (i.e. the coordinates are
           swapped), bail. */
        if (tile_info.x0 >= tile_info.x1
            || tile_info.y0 >= tile_info.y1
            || tile_info.x0 < image->x0
            || tile_info.y0 < image->y0
            || tile_info.x1 - image->x0 > im->xsize
            || tile_info.y1 - image->y0 > im->ysize) {
            state->errcode = IMAGING_CODEC_BROKEN;
            state->state = J2K_STATE_FAILED;
            goto quick_exit;
        }

        unpack(image, &tile_info, state->buffer, im);
    }

    if (!opj_end_decompress(codec, stream)) {
        state->errcode = IMAGING_CODEC_BROKEN;
        state->state = J2K_STATE_FAILED;
        goto quick_exit;
    }

    state->state = J2K_STATE_DONE;
    state->errcode = IMAGING_CODEC_END;

 quick_exit:
    if (codec)
        opj_destroy_codec(codec);
    if (image)
        opj_image_destroy(image);
    if (stream)
        opj_stream_destroy(stream);

    return -1;
}

int
ImagingJpeg2KDecode(Imaging im, ImagingCodecState state, UINT8* buf, int bytes)
{
    JPEG2KDECODESTATE *context = (JPEG2KDECODESTATE *) state->context;

    if (state->state == J2K_STATE_DONE || state->state == J2K_STATE_FAILED)
        return -1;

    if (state->state == J2K_STATE_START) {
        context->decoder = ImagingIncrementalCodecCreate(j2k_decode_entry,
                                                         im, state,
                                                         INCREMENTAL_CODEC_READ,
                                                         INCREMENTAL_CODEC_NOT_SEEKABLE,
                                                         context->fd);

        if (!context->decoder) {
            state->errcode = IMAGING_CODEC_BROKEN;
            state->state = J2K_STATE_FAILED;
            return -1;
        }

        state->state = J2K_STATE_DECODING;
    }

    return ImagingIncrementalCodecPushBuffer(context->decoder, buf, bytes);
}

/* -------------------------------------------------------------------- */
/* Cleanup                                                              */
/* -------------------------------------------------------------------- */

int
ImagingJpeg2KDecodeCleanup(ImagingCodecState state) {
    JPEG2KDECODESTATE *context = (JPEG2KDECODESTATE *)state->context;

    if (context->error_msg)
        free ((void *)context->error_msg);

    if (context->decoder)
        ImagingIncrementalCodecDestroy(context->decoder);

    context->error_msg = NULL;

    /* Prevent multiple calls to ImagingIncrementalCodecDestroy */
    context->decoder = NULL;

    return -1;
}

const char *
ImagingJpeg2KVersion(void)
{
    return opj_version();
}

#endif /* HAVE_OPENJPEG */

/*
 * Local Variables:
 * c-basic-offset: 4
 * End:
 *
 */
