#ifndef ENGACER_WINPROCESS148_H
#define ENGACER_WINPROCESS148_H
#include <stdint.h>
#define W8_PROCESS_SNAPSHOT_MAX148 4u
typedef struct {uint32_t pid,parent,threads;char name[64];} w8_process_record148;
typedef struct {uint32_t count;w8_process_record148 records[W8_PROCESS_SNAPSHOT_MAX148];} w8_process_snapshot148;
_Static_assert(sizeof(w8_process_snapshot148)==308,"Bounded process metadata snapshot ABI");
#endif
