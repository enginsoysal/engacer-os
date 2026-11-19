#ifndef ENGACER_MODULE142_H
#define ENGACER_MODULE142_H
typedef struct {char path[256],name[96];uint8_t*base;uint32_t size,exports,export_size,entry,dependencies;unsigned state,dll,references,attached,sequence,subsystem;uint64_t tls_template;uint32_t tls_bytes,tls_zero,tls_callbacks,tls_alignment,tls_present;} module141;
#endif
