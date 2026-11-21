#ifndef ENGINE_WINCONTEXT142_H
#define ENGINE_WINCONTEXT142_H
#include <stdint.h>
#include <stddef.h>
typedef struct {
 uint64_t home[6];uint32_t flags,mxcsr;uint16_t cs,ds,es,fs,gs,ss;uint32_t eflags;uint64_t debug[6];
 uint64_t rax,rcx,rdx,rbx,rsp,rbp,rsi,rdi,r8,r9,r10,r11,r12,r13,r14,r15,rip;
 _Alignas(16) uint8_t fx[512];uint8_t vectors[26][16];uint64_t vector_control,debug_control,last_branch_to,last_branch_from,last_exception_to,last_exception_from;
} w8_context142;
typedef struct {uint32_t code,flags;uint64_t next,address;uint32_t count,pad;uint64_t arguments[15];} w8_exception_record142;
typedef struct {uint64_t record,context;} w8_exception_pointers142;
typedef struct {w8_exception_record142 record;w8_exception_pointers142 pointers;_Alignas(16) w8_context142 context;uint32_t software148,reserved148;} w8_exception_packet142;
_Static_assert(sizeof(w8_context142)==1232,"Windows AMD64 CONTEXT ABI");
_Static_assert(offsetof(w8_context142,rax)==120,"Windows integer context offset");
_Static_assert(offsetof(w8_context142,rip)==248,"Windows instruction pointer offset");
_Static_assert(offsetof(w8_context142,fx)==256,"Windows floating context offset");
_Static_assert(sizeof(w8_exception_record142)==152,"Windows exception record ABI");
#endif
