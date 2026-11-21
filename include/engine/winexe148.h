/* Initial original-EXE launch profile. Shared Windows API implementations do not
 * depend on this table; source identity limits what this stage can qualify. */
#ifndef ENGINE_WINEXE148_H
#define ENGINE_WINEXE148_H
#include <stdint.h>
#include <stddef.h>
#define EXE148_CODE "{D6E9EC8F-75FD-5D1F-8990-8DE725154FFF}"
#define EXE148_ROOT "/Applications/Windows/" EXE148_CODE
#define EXE148_ALIAS "C:\\Program Files\\SumatraPDF"
#define EXE148_SOURCE_BYTES UINT64_C(11075960)
#define EXE148_SOURCE_SHA "1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381"
typedef struct {const char*name;uint64_t bytes;const char*sha;uint32_t crc;} exe_payload148;
static const exe_payload148 exe_payloads148[]={
 {"SumatraPDF.exe",11075960,EXE148_SOURCE_SHA,2042335303u},
 {"libmupdf.dll",16625528,"a1290f350cc6c5de0c44d64be2f8e193f927c368224cb6b0738f9b843110c08c",197125815u},
 {"PdfFilter.dll",342904,"f4de564a26049dd93c0cbb33a40273bccfacf29b266f57dbe7673c4b1f363e8f",1167518459u},
 {"PdfPreview.dll",746360,"7f4ee56e1d36d2dc53dc684841316a163c9d91c8e0b544baf6992b4596c26e92",1534824848u}
};
static inline unsigned exe_nibble148(unsigned c){return c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:256;}
static inline unsigned exe_digest148(const uint8_t digest[32],const char*hex){if(!digest||!hex)return 0;for(unsigned i=0;i<32;++i){unsigned a=exe_nibble148((uint8_t)hex[i*2]),b=exe_nibble148((uint8_t)hex[i*2+1]);if(a>15||b>15||digest[i]!=(a*16+b))return 0;}return hex[64]==0;}
enum {EXE148_INSTALLING=1,EXE148_INSTALLED,EXE148_REMOVING,EXE148_REMOVED,EXE148_INCOMPLETE};
typedef struct {uint32_t present,type,bytes,key_present;uint8_t data[512];} exe_shared148;
typedef struct {uint64_t magic;uint32_t schema,bytes,state,nonce;uint8_t source_sha[32],checksum[32];char user[256],root[256],alias[256],source[256],temporary[256];exe_shared148 shared[2];uint32_t reserved[8];} exe_record148;
#define EXE148_RECORD_MAGIC UINT64_C(0x314558454e453431)
_Static_assert(offsetof(exe_record148,checksum)==56&&sizeof(exe_record148)<=4096,"EXE record must retain a checked single-page schema");
#ifndef W8_USER
unsigned w8_exe_record148(const char*,exe_record148*);
#endif
#endif
