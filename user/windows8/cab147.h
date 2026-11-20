#ifndef ENGINE_CAB147_H
#define ENGINE_CAB147_H
#include "msi_db.h"
typedef struct {const char *name;uint32_t offset,size;uint16_t date,time,attributes;} cab147_file;
typedef struct {msi8_blob source;unsigned count,bytes,blocks,window,data_at;cab147_file files[];} cab147_archive;
enum {CAB147_OK=0,CAB147_FORMAT=1,CAB147_MEMORY=2,CAB147_SINK=3,CAB147_DECODE=4};
/* A validated archive borrows immutable source bytes; close never frees source.
 * Sink receives ordered per-file byte offsets, including one zero-byte call
 * for an empty file. Writes belong to the caller's staged transaction.
 */
typedef int (*cab147_sink)(void *,const cab147_file *,unsigned,const void *,unsigned);
unsigned cab147_open(msi8_blob,cab147_archive **);
unsigned cab147_walk(const cab147_archive *,cab147_sink,void *);
void cab147_close(cab147_archive *);
#endif
