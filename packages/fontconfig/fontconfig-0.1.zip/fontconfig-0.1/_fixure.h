/**
 * Copyright (c) 2016 Marco Giusti
 * See LICENSE for details.
 */

#include <stdlib.h>
#include <fontconfig/fontconfig.h>
#include <fontconfig/fcfreetype.h>
#include <ft2build.h>
#include FT_FREETYPE_H


/* Changes in fontconfig 2.11.94 */
#if FC_VERSION < 21194
#define FC_SYMBOL "symbol"
typedef const char _FcObjectType_s;
#else
typedef char _FcObjectType_s;
#endif


/* Changes in fontconfig 2.11.91 */
#if FC_VERSION < 21191
#define PYFC_HAS_FcRange 0

#define FC_COLOR "color"
#define FC_WEIGHT_DEMILIGHT 55
#define FC_WEIGHT_SEMILIGHT FC_WEIGHT_DEMILIGHT

typedef struct _FcRange {
} FcRange;

FcBool (*FcPatternAddRange)(FcPattern *p, const char *object,
		const FcRange *r) = NULL;
FcResult (*FcPatternGetRange)(const FcPattern *p, const char *object, int id,
		FcRange **r) = NULL;
FcRange *(*FcRangeCreateDouble)(double begin, double end) = NULL;
FcRange *(*FcRangeCreateInteger)(FcChar32 begin, FcChar32 end) = NULL;
void (*FcRangeDestroy)(FcRange *range) = NULL;
FcRange *(*FcRangeCopy)(const FcRange *r) = NULL;
FcBool (*FcRangeGetDouble)(const FcRange *range, double *begin,
		double *end) = NULL;
int (*FcWeightFromOpenType)(int ot_weight) = NULL;
int (*FcWeightToOpenType)(int fc_weight) = NULL;
#else
#define PYFC_HAS_FcRange 1
#endif

/* Changes in fontconfig 2.11.1 */
#if FC_VERSION < 21101
#define PYFC_HAS_DirCacheRescan 0

FcCache *(*FcDirCacheRescan)(const FcChar8 *dir, FcConfig *config) = NULL;
#else
#define PYFC_HAS_DirCacheRescan 1
#endif
