#ifndef ENGINE_WINEXCEPTION32_1410_H
#define ENGINE_WINEXCEPTION32_1410_H
#include <stdint.h>
#include <stddef.h>

#define WIN32_FULL_CONTEXT1410 UINT32_C(0x00010007)

/* The fixed layouts are the Windows i386 ABI, including reserved register
 * storage outside the control/integer/segment fields supplied here. */
typedef struct {
 uint32_t flags,debug[6];
 uint8_t floating[112];
 uint32_t gs,fs,es,ds,edi,esi,ebx,edx,ecx,eax,ebp,eip,cs,eflags,esp,ss;
 uint8_t extended[512];
} win_context321410;

typedef struct {
 uint32_t code,flags,nested,address,count,arguments[15];
} win_exception_record321410;

typedef struct {
 uint32_t record,context;
} win_exception_pointers321410;

_Static_assert(sizeof(win_context321410)==716,"i386 Windows CONTEXT size");
_Static_assert(offsetof(win_context321410,eip)==184,"i386 Windows instruction pointer");
_Static_assert(offsetof(win_context321410,esp)==196,"i386 Windows stack pointer");
_Static_assert(sizeof(win_exception_record321410)==80,"i386 Windows exception record");
_Static_assert(sizeof(win_exception_pointers321410)==8,"i386 Windows exception pointer record");
#endif
