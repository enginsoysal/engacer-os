#ifndef ENGINE_WINDOWS8_H
#define ENGINE_WINDOWS8_H
#include <stdint.h>
#include <stddef.h>
#include <engine/wincontext142.h>
#define W8_BASE UINT64_C(0x100000000)
#define W8_LIMIT UINT64_C(0x140000000)
#define W8_MAILBOX UINT64_C(0x100800000)
#define W8_STACK_LOW UINT64_C(0x10a000000)
#define W8_STACK_TOP UINT64_C(0x10a800000)
#define W8_TEB UINT64_C(0x100a00000)
#define W8_HEAP UINT64_C(0x120000000)
#define W8_MAGIC 0x38574f53u
#define W8_IO 4096u
#define W8_TEXT 16384u
enum {W8_PREVIEW=1,W8_INSTALL,W8_RUN,W8_REMOVE,W8_INSPECT};
enum {W8_SYS_MAP=0x800,W8_SYS_UNMAP,W8_SYS_PROTECT,W8_SYS_OPEN,W8_SYS_READ,
 W8_SYS_WRITE,W8_SYS_SEEK,W8_SYS_CLOSE,W8_SYS_STAT,W8_SYS_ENUM,W8_SYS_MKDIR,
 W8_SYS_DELETE,W8_SYS_MOVE,W8_SYS_OUTPUT,W8_SYS_EXIT,W8_SYS_TIME,W8_SYS_YIELD,
 W8_SYS_METADATA,W8_SYS_INFO,W8_SYS_TRUNCATE,W8_SYS_RESERVE,W8_SYS_VMINFO,
 W8_SYS_THREAD_CREATE,W8_SYS_THREAD_EXIT,W8_SYS_THREAD_RESUME,
 W8_SYS_THREAD_STATUS,W8_SYS_SLEEP,W8_SYS_PARK,W8_SYS_WAKE,W8_SYS_THREAD_CLOSE,W8_SYS_QUIESCE,W8_SYS_THREAD_LIST,W8_SYS_ACCESS,W8_SYS_THREAD_BEGIN_EXIT,W8_SYS_PROCESS_CREATE,W8_SYS_PROCESS_STATUS,
 W8_SYS_PROCESS_CLOSE,W8_SYS_PROCESS_ID,W8_SYS_THREAD_ID,W8_SYS_PROCESS_TERMINATE,W8_SYS_EXCEPTION_REGISTER,W8_SYS_EXCEPTION_RETURN};
#define W8_PROCESS_TAG UINT64_C(0x80000000)
#define W8_HANDLE_TAG_MASK UINT64_C(0xffffffffe0000000)
typedef struct {char source[256],command[1200],directory[256];uint32_t flags;} w8_process_request;
typedef struct {uint64_t process,thread;uint32_t process_id,thread_id;} w8_process_result;
typedef struct {uint64_t teb;uint32_t id,state;} w8_thread_snapshot;
typedef struct {uint64_t size,time[3];uint32_t attributes,crc,kind;char name[256];} w8_file_info;
typedef struct {
 uint32_t magic,command,status,percent;
 char source[256],product_root[256],user_root[256],windows_root[256],arguments[1024];
 char product[96],version[32],publisher[96],code[40];
 uint32_t files,registry,shortcuts,features;
 uint64_t total_bytes;
 char message[192];
 char startup_command[1200],startup_directory[256];
 uint32_t process_id,startup_flags;
} w8_mailbox;
_Static_assert(sizeof(w8_mailbox)<=4096,"Windows startup mailbox must fit its checked page");
#ifndef W8_USER
#include <engine/process.h>
typedef struct {unsigned state,command,status,percent,revision;uint64_t peak_pages,quanta;
 char product[96],version[32],publisher[96],code[40],message[192],output[W8_TEXT];
 unsigned files;uint64_t total_bytes;} w8_info;
extern volatile unsigned w8_active;
unsigned w8_start(unsigned,const char*,const char*,const char*,const char*);
unsigned w8_pending(void);
unsigned w8_runnable(void);
void w8_pump(void);
void w8_cancel(void);
const w8_info *w8_current(void);
trap_frame *w8_trap(trap_frame*);
unsigned w8_install_runtime(void*);
#endif
#endif
