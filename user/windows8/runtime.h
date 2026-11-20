#ifndef W8_RUNTIME_H
#define W8_RUNTIME_H
#define W8_USER
#include <engine/windows8.h>
#include <stdint.h>
#include <stddef.h>
#define MS __attribute__((ms_abi))
#define NORETURN __attribute__((noreturn))
typedef uint16_t WCHAR;
typedef uint64_t HANDLE;
typedef struct {uint32_t lo,hi;} FILETIME;
extern w8_mailbox *const job8;
uint64_t sys8(uint64_t,uint64_t,uint64_t,uint64_t,uint64_t,uint64_t);
NORETURN void fail8(const char*);
NORETURN void exit8(unsigned);
void print8(const char*);
void number8(uint64_t);
unsigned len8(const char*);
unsigned wlen8(const WCHAR*);
int equal8(const char*,const char*);
int case8(const char*,const char*);
void copy8(char*,const char*,unsigned);
void append8(char*,const char*,unsigned);
typedef struct {uint32_t owner,depth;} lock142;
uint64_t teb142(void);
unsigned tid142(void);
void lock_enter142(lock142*);
void lock_leave142(lock142*);
void *alloc8(size_t);
void free8(void*);
size_t allocation_size8(const void*);
void *realloc8(void*,size_t);
void *calloc8(size_t,size_t);
void *memcpy(void*,const void*,size_t);
void *memset(void*,int,size_t);
void *memmove(void*,const void*,size_t);
int memcmp(const void*,const void*,size_t);
size_t strlen(const char*);
int utf8_to16(const char*,WCHAR*,unsigned);
int utf16_to8(const WCHAR*,char*,unsigned);
int open8(const char*,unsigned);
int read8(int,void*,unsigned);
int write8(int,const void*,unsigned);
int64_t seek8(int,int64_t,unsigned);
int close8(int);
int stat8(const char*,w8_file_info*);
unsigned load8(const char*,void**,unsigned);
int save8(const char*,const void*,unsigned);
int mkdir8(const char*);
int remove8(const char*);
void progress8(unsigned,const char*);
void init_win8(void);
void *resolve8(const char*,const char*,unsigned);
uint64_t pe8_load(const char*);
uint64_t pe8_named(const char*);
void *pe8_symbol(uint64_t,const char*,unsigned);
void *pe8_import(const char*,const char*,unsigned);
void pe8_inspect(const char*);
uint64_t pe8_find_resource(uint64_t,const WCHAR*,const WCHAR*,unsigned,unsigned,unsigned*);
unsigned pe8_resource_data(uint64_t,uint64_t,const void**,unsigned*);
uint64_t pe8_module(const char*);
const char *pe8_path(uint64_t);
uint64_t pe8_main(void);
int pe8_release(uint64_t);
void pe8_shutdown(void);
void pe8_thread_attach(void);
void pe8_thread_detach(void);
NORETURN void pe8_exit(unsigned);
void pe8_run(const char*,const char*);
unsigned pe8_exception_dispatch(w8_exception_record142*,w8_context142*);
int seh_c_specific142(w8_exception_record142*,uint64_t,w8_context142*,void*);
void msi8_execute(void);
#endif
