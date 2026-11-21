#ifndef ENGACER_WINMESSAGE148_H
#define ENGACER_WINMESSAGE148_H
#include <engine/winatom147.h>
/* Separate session namespace: registrations are never reference-counted or
 * deleted by GlobalDeleteAtom. Numeric-looking names remain ordinary strings.
 * The current bounded profile folds ASCII; other scalars compare exactly. */
static inline int wmessage_register148(watom_table147 *table,
                                      const uint16_t *name, unsigned length) {
 if (!watom_valid147(name,length)) return -87;
 if (!table) return -8;
 unsigned slot=0;
 for (;slot<WATOM_SLOTS147&&table->references[slot];++slot)
  if (watom_equal147(table->text+table->offsets[slot],table->lengths[slot],
                    name,length,watom_case147)) return (int)(0xc000u+slot);
 if (slot==WATOM_SLOTS147||length+1>WATOM_UNITS147-table->used) return -1816;
 table->offsets[slot]=table->used;
 table->lengths[slot]=(uint16_t)length;
 table->references[slot]=1;
 for (unsigned i=0;i<length;++i) table->text[table->used+i]=name[i];
 table->text[table->used+length]=0;
 table->used=(uint16_t)(table->used+length+1);
 return (int)(0xc000u+slot);
}
#endif
