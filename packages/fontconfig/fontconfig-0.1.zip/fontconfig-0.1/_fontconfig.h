/**
 * Copyright (c) 2016 Marco Giusti
 * See LICENSE for details.
 */


/* stdlib */

void free(void *ptr);

/* CONDITIONALS */

#define PYFC_HAS_DirCacheRescan ...
#define PYFC_HAS_FcRange ...

/* Defines */

static char *const FC_CACHE_VERSION;

static char *const FC_FAMILY;
static char *const FC_STYLE;
static char *const FC_SLANT;
static char *const FC_WEIGHT;
static char *const FC_SIZE;
static char *const FC_ASPECT;
static char *const FC_PIXEL_SIZE;
static char *const FC_SPACING;
static char *const FC_FOUNDRY;
static char *const FC_ANTIALIAS;
static char *const FC_HINTING;
static char *const FC_HINT_STYLE;
static char *const FC_VERTICAL_LAYOUT;
static char *const FC_AUTOHINT;
static char *const FC_GLOBAL_ADVANCE;
static char *const FC_WIDTH;
static char *const FC_FILE;
static char *const FC_INDEX;
static char *const FC_FT_FACE;
static char *const FC_RASTERIZER;
static char *const FC_OUTLINE;
static char *const FC_SCALABLE;
static char *const FC_COLOR;
static char *const FC_SCALE;
static char *const FC_SYMBOL;
static char *const FC_DPI;
static char *const FC_RGBA;
static char *const FC_MINSPACE;
static char *const FC_SOURCE;
static char *const FC_CHARSET;
static char *const FC_LANG;
static char *const FC_FONTVERSION;
static char *const FC_FULLNAME;
static char *const FC_FAMILYLANG;
static char *const FC_STYLELANG;
static char *const FC_FULLNAMELANG;
static char *const FC_CAPABILITY;
static char *const FC_FONTFORMAT;
static char *const FC_EMBOLDEN;
static char *const FC_EMBEDDED_BITMAP;
static char *const FC_DECORATIVE;
static char *const FC_LCD_FILTER;
static char *const FC_FONT_FEATURES;
static char *const FC_NAMELANG;
static char *const FC_PRGNAME;
static char *const FC_HASH;
static char *const FC_POSTSCRIPT_NAME;

static char *const FC_CACHE_SUFFIX;
static char *const FC_DIR_CACHE_FILE;
static char *const FC_USER_CACHE_FILE;

static char *const FC_CHAR_WIDTH;
static char *const FC_CHAR_HEIGHT;
static char *const FC_MATRIX;

#define FC_WEIGHT_THIN ...
#define FC_WEIGHT_EXTRALIGHT ...
#define FC_WEIGHT_ULTRALIGHT ...
#define FC_WEIGHT_LIGHT ...
#define FC_WEIGHT_DEMILIGHT ...
#define FC_WEIGHT_SEMILIGHT ...
#define FC_WEIGHT_BOOK ...
#define FC_WEIGHT_REGULAR ...
#define FC_WEIGHT_NORMAL ...
#define FC_WEIGHT_MEDIUM ...
#define FC_WEIGHT_DEMIBOLD ...
#define FC_WEIGHT_SEMIBOLD ...
#define FC_WEIGHT_BOLD ...
#define FC_WEIGHT_EXTRABOLD ...
#define FC_WEIGHT_ULTRABOLD ...
#define FC_WEIGHT_BLACK ...
#define FC_WEIGHT_HEAVY ...
#define FC_WEIGHT_EXTRABLACK ...
#define FC_WEIGHT_ULTRABLACK ...

#define FC_SLANT_ROMAN ...
#define FC_SLANT_ITALIC ...
#define FC_SLANT_OBLIQUE ...

#define FC_WIDTH_ULTRACONDENSED ...
#define FC_WIDTH_EXTRACONDENSED ...
#define FC_WIDTH_CONDENSED ...
#define FC_WIDTH_SEMICONDENSED ...
#define FC_WIDTH_NORMAL ...
#define FC_WIDTH_SEMIEXPANDED ...
#define FC_WIDTH_EXPANDED ...
#define FC_WIDTH_EXTRAEXPANDED ...
#define FC_WIDTH_ULTRAEXPANDED ...

#define FC_PROPORTIONAL ...
#define FC_DUAL ...
#define FC_MONO ...
#define FC_CHARCELL ...

/* sub-pixel order */
#define FC_RGBA_UNKNOWN ...
#define FC_RGBA_RGB ...
#define FC_RGBA_BGR ...
#define FC_RGBA_VRGB ...
#define FC_RGBA_VBGR ...
#define FC_RGBA_NONE ...

/* hinting style */
#define FC_HINT_NONE ...
#define FC_HINT_SLIGHT ...
#define FC_HINT_MEDIUM ...
#define FC_HINT_FULL ...

/* LCD filter */
#define FC_LCD_NONE ...
#define FC_LCD_DEFAULT ...
#define FC_LCD_LIGHT ...
#define FC_LCD_LEGACY ...

/* Types */

typedef unsigned char FcChar8;
typedef unsigned short FcChar16;
typedef unsigned int FcChar32;
typedef int FcBool;

typedef enum _FcType {
    FcTypeUnknown = -1,
    FcTypeVoid,
    FcTypeInteger,
    FcTypeDouble,
    FcTypeString,
    FcTypeBool,
    FcTypeMatrix,
    FcTypeCharSet,
    FcTypeFTFace,
    FcTypeLangSet,
    ...
    /* new in 2.11.1 */
    /* FcTypeRange */
} FcType;

typedef struct _FcMatrix {
    double xx, xy, yx, yy;
} FcMatrix;

typedef ... FcCharSet;

/* "const char" in fontconfig <= 2.11.93, "char" in master */
typedef ... _FcObjectType_s;
typedef struct _FcObjectType {
    _FcObjectType_s *object;
    FcType type;
} FcObjectType;

typedef struct _FcConstant {
    const FcChar8 *name;
    const char *object;
    int value;
} FcConstant;

typedef enum _FcResult {
    FcResultMatch,
    FcResultNoMatch,
    FcResultTypeMismatch,
    FcResultNoId,
    FcResultOutOfMemory
} FcResult;

typedef ... FcPattern;

typedef ... FcLangSet;

typedef ... FcRange;

typedef struct _FcValue {
    FcType type;
    union {
        const FcChar8 *s;
        int i;
        FcBool b;
        double d;
        const FcMatrix *m;
        const FcCharSet *c;
        void *f;
        const FcLangSet *l;
        const FcRange *r;
    } u;
} FcValue;

typedef struct _FcFontSet {
    int nfont;
    int sfont;
    FcPattern **fonts;
} FcFontSet;

typedef struct _FcObjectSet {
    int nobject;
    int sobject;
    const char **objects;
} FcObjectSet;
    
typedef enum _FcMatchKind {
    FcMatchPattern,
    FcMatchFont,
    FcMatchScan
} FcMatchKind;

typedef enum _FcLangResult {
    FcLangEqual = 0,
    FcLangDifferentCountry = 1,
    FcLangDifferentTerritory = 1,
    FcLangDifferentLang = 2
} FcLangResult;

typedef enum _FcSetName {
    FcSetSystem = 0,
    FcSetApplication = 1
} FcSetName;

typedef ... FcAtomic;

typedef enum {
    FcEndianBig,
    FcEndianLittle
} FcEndian;

typedef ... FcConfig;

typedef ... FcFileCache;

typedef ... FcBlanks;

typedef ... FcStrList;

typedef ... FcStrSet;

typedef ... FcCache;

/* Initialization */

FcConfig *FcInitLoadConfig(void);
FcConfig *FcInitLoadConfigAndFonts(void);
FcBool FcInit(void);
void FcFini(void);
int FcGetVersion(void);
FcBool FcInitReinitialize(void);
FcBool FcInitBringUptoDate(void);

/* FcPattern */

FcPattern *FcPatternCreate(void);
FcPattern *FcPatternDuplicate(const FcPattern *p);
void FcPatternReference(FcPattern *p);
void FcPatternDestroy(FcPattern *p);
FcBool FcPatternEqual(const FcPattern *pa, const FcPattern *pb);
FcBool FcPatternEqualSubset(const FcPattern *pa, const FcPattern *pb,
        const FcObjectSet *os);
FcPattern *FcPatternFilter(FcPattern *p, const FcObjectSet *os);
FcChar32 FcPatternHash(const FcPattern *p);
FcBool FcPatternAdd(FcPattern *p, const char *object, FcValue value,
        FcBool append);
FcBool FcPatternAddWeak(FcPattern *p, const char *object, FcValue value,
        FcBool append);
FcBool FcPatternAddInteger(FcPattern *p, const char *object, int i);
FcBool FcPatternAddDouble(FcPattern *p, const char *object, double d);
FcBool FcPatternAddString(FcPattern *p, const char *object, const FcChar8 *s);
FcBool FcPatternAddMatrix(FcPattern *p, const char *object, const FcMatrix *s);
FcBool FcPatternAddCharSet(FcPattern *p, const char *object,
        const FcCharSet *c);
FcBool FcPatternAddBool(FcPattern *p, const char *object, FcBool b);
FcBool FcPatternAddLangSet(FcPattern *p, const char *object,
        const FcLangSet *ls);
FcBool FcPatternAddRange(FcPattern *p, const char *object, const FcRange *r);
FcResult FcPatternGet(const FcPattern *p, const char *object, int id,
        FcValue *v);
FcResult FcPatternGetInteger(const FcPattern *p, const char *object, int n,
        int *i);
FcResult FcPatternGetDouble(const FcPattern *p, const char *object, int n,
        double *d);
FcResult FcPatternGetString(const FcPattern *p, const char *object, int n,
        FcChar8 **s);
FcResult FcPatternGetMatrix(const FcPattern *p, const char *object, int n,
        FcMatrix **s);
FcResult FcPatternGetCharSet(const FcPattern *p, const char *object, int n,
        FcCharSet **c);
FcResult FcPatternGetBool(const FcPattern *p, const char *object, int n,
        FcBool *b);
FcResult FcPatternGetLangSet(const FcPattern *p, const char *object, int n,
        FcLangSet **ls);
FcResult FcPatternGetRange(const FcPattern *p, const char *object, int id,
        FcRange **r);
FcPattern *FcPatternBuild(FcPattern *p, ...);
FcBool FcPatternDel(FcPattern *p, const char *object);
FcBool FcPatternRemove(FcPattern *p, const char *object, int id);
void FcPatternPrint(const FcPattern *p);
void FcDefaultSubstitute(FcPattern *pattern);
FcPattern *FcNameParse(const FcChar8 *name);
FcChar8 *FcNameUnparse(FcPattern *pat);
FcChar8 *FcPatternFormat(FcPattern *pat, const FcChar8 *format);
/* TODO: FcPatternVaBuild */
/* FcPattern *FcPatternVaBuild(FcPattern *p, va_list va); */

/* FcFontSet */

FcFontSet *FcFontSetCreate(void);
void FcFontSetDestroy(FcFontSet *s);
FcBool FcFontSetAdd(FcFontSet *s, FcPattern *font);
FcFontSet *FcFontSetList(FcConfig *config, FcFontSet **sets, int nsets,
  FcPattern *p, FcObjectSet *os);
FcPattern *FcFontSetMatch(FcConfig *config, FcFontSet **sets, int nsets,
  FcPattern *p, FcResult *result);
void FcFontSetPrint(const FcFontSet *s);
FcFontSet *FcFontSetSort(FcConfig *config, FcFontSet **sets, int nsets,
  FcPattern *p, FcBool trim, FcCharSet **csp, FcResult *result);
void FcFontSetSortDestroy(FcFontSet *fs);

/* FcObjectSet */

FcObjectSet *FcObjectSetCreate(void);
FcBool FcObjectSetAdd(FcObjectSet *os, const char *object);
void FcObjectSetDestroy(FcObjectSet *os);
FcObjectSet *FcObjectSetBuild(const char *first, ...);
/* TODO: FcObjectSetVaBuild */
/* FcObjectSet *FcObjectSetVaBuild(const char *first, va_list va); */


/* FreeType */

typedef unsigned int FT_UInt;
typedef signed long FT_Long;
typedef unsigned char FT_Byte;
typedef int FT_Error;
typedef struct FT_FaceRec_ {
	FT_Long num_faces;
	...;
} *FT_Face;
typedef ... *FT_Library;

FT_Error FT_Init_FreeType(FT_Library *alibrary);
FT_Error FT_Done_FreeType(FT_Library library);
FT_Error FT_New_Memory_Face(FT_Library library, const FT_Byte *file_base,
		FT_Long file_size, FT_Long face_index, FT_Face *aface);
FT_Error FT_Done_Face(FT_Face face);

FT_UInt FcFreeTypeCharIndex(FT_Face face, FcChar32 ucs4);
FcCharSet *FcFreeTypeCharSet(FT_Face face, FcBlanks *blanks);
FcCharSet *FcFreeTypeCharSetAndSpacing(FT_Face face, FcBlanks *blanks,
        int *spacing);
FcPattern *FcFreeTypeQuery(const FcChar8 *file, int id, FcBlanks *blanks,
        int *count);
FcPattern *FcFreeTypeQueryFace(const FT_Face face, const FcChar8 *file, int id,
        FcBlanks *blanks);
FcResult FcPatternGetFTFace(const FcPattern *p, const char *object, int n,
        FT_Face *f);
FcBool FcPatternAddFTFace(FcPattern *p, const char *object, const FT_Face f);

/* FcValue */

void FcValueDestroy(FcValue v);
FcValue FcValueSave(FcValue v);
FcBool FcValueEqual(FcValue va, FcValue vb);
void FcValuePrint(const FcValue v);

/* FcCharSet */

FcCharSet *FcCharSetCreate(void);
void FcCharSetDestroy(FcCharSet *fcs);
FcBool FcCharSetAddChar(FcCharSet *fcs, FcChar32 ucs4);
FcBool FcCharSetDelChar(FcCharSet *fcs, FcChar32 ucs4);
FcCharSet *FcCharSetCopy(FcCharSet *src);
FcBool FcCharSetEqual(const FcCharSet *a, const FcCharSet *b);
FcCharSet *FcCharSetIntersect(const FcCharSet *a, const FcCharSet *b);
FcCharSet *FcCharSetUnion(const FcCharSet *a, const FcCharSet *b);
FcCharSet *FcCharSetSubtract(const FcCharSet *a, const FcCharSet *b);
FcBool FcCharSetMerge(FcCharSet *a, const FcCharSet *b, FcBool *changed);
FcBool FcCharSetHasChar(const FcCharSet *fcs, FcChar32 ucs4);
FcChar32 FcCharSetCount(const FcCharSet *a);
FcChar32 FcCharSetIntersectCount(const FcCharSet *a, const FcCharSet *b);
FcChar32 FcCharSetSubtractCount(const FcCharSet *a, const FcCharSet *b);
FcBool FcCharSetIsSubset(const FcCharSet *a, const FcCharSet *b);
/* map[8] => map[FC_CHARSET_MAP_SIZE] => #define FC_CHARSET_MAP_SIZE(256/32) */
FcChar32 FcCharSetFirstPage(const FcCharSet *a, FcChar32 map[8],
        FcChar32 *next);
FcChar32 FcCharSetNextPage(const FcCharSet *a, FcChar32 map[8],
        FcChar32 *next);
/* TODO: What to do with FcCharSetCoverage? */
FcChar32 FcCharSetCoverage(const FcCharSet *a, FcChar32 page,
        FcChar32 result[8]);

/* FcLangSet */

FcLangSet *FcLangSetCreate(void);
void FcLangSetDestroy(FcLangSet *ls);
FcLangSet *FcLangSetCopy(const FcLangSet *ls);
FcBool FcLangSetAdd(FcLangSet *ls, const FcChar8 *lang);
FcBool FcLangSetDel(FcLangSet *ls, const FcChar8 *lang);
FcLangSet *FcLangSetUnion(const FcLangSet *a, const FcLangSet *b);
FcLangSet *FcLangSetSubtract(const FcLangSet *a, const FcLangSet *b);
FcLangResult FcLangSetCompare(const FcLangSet *lsa, const FcLangSet *lsb);
FcBool FcLangSetContains(const FcLangSet *lsa, const FcLangSet *lsb);
FcBool FcLangSetEqual(const FcLangSet *lsa, const FcLangSet *lsb);
FcChar32 FcLangSetHash(const FcLangSet *ls);
FcLangResult FcLangSetHasLang(const FcLangSet *ls, const FcChar8 *lang);
FcStrSet *FcGetDefaultLangs(void);
FcStrSet *FcGetLangs(void);
FcChar8 *FcLangNormalize(const FcChar8 *lang);
const FcCharSet *FcLangGetCharSet(const FcChar8 *lang);
FcStrSet *FcLangSetGetLangs(const FcLangSet *ls);

/* FcMatrix */

void FcMatrixInit(FcMatrix *mat);
FcMatrix *FcMatrixCopy(const FcMatrix *mat);
FcBool FcMatrixEqual(const FcMatrix *mat1, const FcMatrix *mat2);
void FcMatrixMultiply(FcMatrix *result, const FcMatrix *a, const FcMatrix *b);
void FcMatrixRotate(FcMatrix *m, double c, double s);
void FcMatrixScale(FcMatrix *m, double sx, double sy);
void FcMatrixShear(FcMatrix *m, double sh, double sv);

/* FcConfig */

FcConfig *FcConfigCreate(void);
FcConfig *FcConfigReference(FcConfig *config);
void FcConfigDestroy(FcConfig *config);
FcBool FcConfigSetCurrent(FcConfig *config);
FcConfig *FcConfigGetCurrent(void);
FcBool FcConfigUptoDate(FcConfig *config);
FcChar8 *FcConfigHome();
FcBool FcConfigEnableHome(FcBool enable);
FcBool FcConfigBuildFonts(FcConfig *config);
FcStrList *FcConfigGetConfigDirs(FcConfig *config);
FcStrList *FcConfigGetFontDirs(FcConfig *config);
FcStrList *FcConfigGetConfigFiles(FcConfig *config);
FcChar8 *FcConfigGetCache(FcConfig *config); /* DEPRECATED */
FcStrList *FcConfigGetCacheDirs(FcConfig *config);
FcFontSet *FcConfigGetFonts(FcConfig *config, FcSetName set);
FcBlanks *FcConfigGetBlanks(FcConfig *config);
int FcConfigGetRescanInterval(FcConfig *config);
FcBool FcConfigSetRescanInterval(FcConfig *config, int rescalInterval);
FcBool FcConfigAppFontAddFile(FcConfig *config, const FcChar8 *file);
FcBool FcConfigAppFontAddDir(FcConfig *config, const FcChar8 *dir);
void FcConfigAppFontClear(FcConfig *config);
FcBool FcConfigSubstituteWithPat(FcConfig *config, FcPattern *p,
    FcPattern *p_pat, FcMatchKind kind);
FcBool FcConfigSubstitute(FcConfig *config, FcPattern *p, FcMatchKind kind);
FcPattern *FcFontMatch(FcConfig *config, FcPattern *p, FcResult *result);
FcFontSet *FcFontSort(FcConfig *config, FcPattern *p, FcBool trim,
    FcCharSet **csp, FcResult *result);
FcPattern *FcFontRenderPrepare(FcConfig *config, FcPattern *pat,
    FcPattern *font);
FcFontSet *FcFontList(FcConfig *config, FcPattern *p, FcObjectSet *os);
FcChar8 *FcConfigFilename(const FcChar8 *name);
FcBool FcConfigParseAndLoad(FcConfig *config, const FcChar8 *file,
    FcBool complain);
const FcChar8 *FcConfigGetSysRoot(const FcConfig *config);
void FcConfigSetSysRoot(FcConfig *config, const FcChar8 *sysroot);

/* FcObjectType */


FcBool FcNameRegisterObjectTypes(const FcObjectType *types, int ntype);
FcBool FcNameUnregisterObjectTypes(const FcObjectType *types, int ntype);
const FcObjectType *FcNameGetObjectType(const char *object);

/* FcConstant */

FcBool FcNameRegisterConstants(const FcConstant *consts, int nconsts);
FcBool FcNameUnregisterConstants(const FcConstant *consts, int nconsts);
const FcConstant *FcNameGetConstant(const FcChar8 *string);
FcBool FcNameConstant(const FcChar8 *string, int *result);

/* FcBlanks */

FcBlanks *FcBlanksCreate(void);
void FcBlanksDestroy(FcBlanks *b);
FcBool FcBlanksAdd(FcBlanks *b, FcChar32 ucs4);
FcBool FcBlanksIsMember(FcBlanks *b, FcChar32 ucs4);

/* FcAtomic */

FcAtomic *FcAtomicCreate(const FcChar8 *file);
FcBool FcAtomicLock(FcAtomic *atomic);
FcChar8 *FcAtomicNewFile(FcAtomic *atomic);
FcChar8 *FcAtomicOrigFile(FcAtomic *atomic);
FcBool FcAtomicReplaceOrig(FcAtomic *atomic);
void FcAtomicDeleteNew(FcAtomic *atomic);
void FcAtomicUnlock(FcAtomic *atomic);
void FcAtomicDestroy(FcAtomic *atomic);

/* File and Directory routines */

FcBool FcFileScan(FcFontSet *set, FcStrSet *dirs, FcFileCache *cache,
        FcBlanks *blanks, const FcChar8 *file, FcBool force);
FcBool FcFileIsDir(const FcChar8 *file);
FcBool FcDirScan(FcFontSet *set, FcStrSet *dirs, FcFileCache *cache,
        FcBlanks *blanks, const FcChar8 *dir, FcBool force);
FcBool FcDirSave(FcFontSet *set, FcStrSet *dirs, const FcChar8 *dir);
FcBool FcDirCacheUnlink(const FcChar8 *dir, FcConfig *config);
FcBool FcDirCacheValid(const FcChar8 *cache_file);
FcCache *FcDirCacheLoad(const FcChar8 *dir, FcConfig *config,
        FcChar8 **cache_file);
FcCache *FcDirCacheRead(const FcChar8 *dir, FcBool force, FcConfig *config);
FcCache *FcDirCacheLoadFile(const FcChar8 *cache_file, struct stat *file_stat);
void FcDirCacheUnload(FcCache *cache);
FcCache *FcDirCacheRescan(const FcChar8 *dir, FcConfig *config);

/* FcCache */

const FcChar8 *FcCacheDir(const FcCache *c);
FcFontSet *FcCacheCopySet(const FcCache *c);
const FcChar8 *FcCacheSubdir(const FcCache *c, int i);
int FcCacheNumSubdir(const FcCache *c);
int FcCacheNumFont(const FcCache *c);
FcBool FcDirCacheClean(const FcChar8 *cache_dir, FcBool verbose);
void FcCacheCreateTagFile(const FcConfig *config);

/* FcStrSet and FcStrList */

FcStrSet *FcStrSetCreate(void);
FcBool FcStrSetMember(FcStrSet *set, const FcChar8 *s);
FcBool FcStrSetEqual(FcStrSet *set_a, FcStrSet *set_b);
FcBool FcStrSetAdd(FcStrSet *set, const FcChar8 *s);
FcBool FcStrSetAddFilename(FcStrSet *set, const FcChar8 *s);
FcBool FcStrSetDel(FcStrSet *set, const FcChar8 *s);
void FcStrSetDestroy(FcStrSet *set);
FcStrList *FcStrListCreate(FcStrSet *set);
void FcStrListFirst(FcStrList *list);
FcChar8 *FcStrListNext(FcStrList *list);
void FcStrListDone(FcStrList *list);

/* String utilities */

int FcUtf8ToUcs4(const FcChar8 *src_orig, FcChar32 *dst, int len);
/* dest[6] ==> dest[FC_UTF8_MAX_LEN] => #define FC_UTF8_MAX_LEN 6 */
int FcUcs4ToUtf8(FcChar32 ucs4, FcChar8 dest[6]);
FcBool FcUtf8Len(const FcChar8 *string, int len, int *nchar, int *wchar);
int FcUtf16ToUcs4(const FcChar8 *src_orig, FcEndian endian, FcChar32 *dst,
        int len); /* in bytes */
FcBool FcUtf16Len(const FcChar8 *string, FcEndian endian,
        int len, /* in bytes */ int *nchar, int *wchar);
FcBool FcIsLower(FcChar8 c);
FcBool FcIsUpper(FcChar8 c);
FcChar8 FcToLower(FcChar8 c);
FcChar8 *FcStrCopy(const FcChar8 *s);
FcChar8 *FcStrDowncase(const FcChar8 *s);
FcChar8 *FcStrCopyFilename(const FcChar8 *s);
int FcStrCmp(const FcChar8 *s1, const FcChar8 *s2);
int FcStrCmpIgnoreCase(const FcChar8 *s1, const FcChar8 *s2);
const FcChar8 *FcStrStr(const FcChar8 *s1, const FcChar8 *s2);
const FcChar8 *FcStrStrIgnoreCase(const FcChar8 *s1, const FcChar8 *s2);
FcChar8 *FcStrPlus(const FcChar8 *s1, const FcChar8 *s2);
void FcStrFree(FcChar8 *s);
FcChar8 *FcStrDirname(const FcChar8 *file);
FcChar8 *FcStrBasename(const FcChar8 *file);
