#include <assert.h>
#include <string.h>
#include <engine/winmigration1410.h>

#define APP WIN_PRODUCT_BASE147 "{A23B657D-838B-4C9B-8F9D-386E50C1A76B}"
typedef struct { uint8_t *bytes; unsigned count; } test_journal;
static unsigned read_journal(void *context,unsigned offset,void *out,unsigned bytes){
 test_journal *journal=context;
 if(offset>journal->count||bytes>journal->count-offset)return 1;
 memcpy(out,journal->bytes+offset,bytes);return 0;
}
static void verify_reader(void){
 union { uint64_t align; uint8_t bytes[1200]; } blob={0};
 win_tx_header147 *header=(void*)blob.bytes;
 win_tx_record147 *record=(void*)(blob.bytes+sizeof(*header));
 win_tx_reg147 *effect=(void*)(record+1);
 const char key[]="Software\\Example",name[]="Sample";
 const uint8_t expected[]={1,2,3,4};
 effect->root=1;effect->view=64;effect->after_type=4;effect->after_bytes=sizeof(expected);
 effect->key_bytes=sizeof(key);effect->name_bytes=sizeof(name);
 char *strings=(void*)(effect+1);
 memcpy(strings,key,sizeof(key));memcpy(strings+sizeof(key),name,sizeof(name));
 memcpy(strings+sizeof(key)+sizeof(name),expected,sizeof(expected));
 record->type=WIN_TX_REG147;
 record->bytes=(sizeof(*record)+sizeof(*effect)+sizeof(key)+sizeof(name)+sizeof(expected)+7)&~7u;
 header->magic=WIN_TX_MAGIC147;header->schema=1;header->records=1;header->registry=1;
 header->bytes=sizeof(*header)+record->bytes;header->source_sha[0]=1;
 memcpy(header->code,&APP[sizeof(WIN_PRODUCT_BASE147)-1],39);
 memcpy(header->user,"/Users/Owner",sizeof("/Users/Owner"));
 memcpy(header->alias,"C:\\Program Files\\Example",sizeof("C:\\Program Files\\Example"));
 memcpy(header->product,"Example",sizeof("Example"));header->version[0]='1';header->publisher[0]='P';
 assert(win_tx_digest147(blob.bytes,header->bytes,header->checksum));
 test_journal journal={blob.bytes,header->bytes};
 win_tx_header147 loaded;
 win_migration_value1410 value;
 unsigned offset=sizeof(*header);
 assert(win_migration_open1410(read_journal,&journal,journal.count,APP,"/Users/Owner",&loaded));
 assert(!win_migration_open1410(read_journal,&journal,journal.count,APP,"/Users/Other",&loaded));
 assert(win_migration_next1410(read_journal,&journal,journal.count,&offset,&value)==1);
 assert(!strcmp(value.key,key)&&!strcmp(value.name,name)&&!memcmp(value.after,expected,sizeof(expected)));
 assert(win_migration_next1410(read_journal,&journal,journal.count,&offset,&value)==0);
 effect->after_bytes=2049;
 assert(!win_migration_open1410(read_journal,&journal,journal.count,APP,"/Users/Owner",&loaded));
 offset=sizeof(*header);
 assert(win_migration_next1410(read_journal,&journal,journal.count,&offset,&value)==-1);
}
int main(void){
 verify_reader();
 const uint8_t installed[]={1,2,3,4},prior[]={5,6,7,8},changed[]={1,2,3,5};
 assert(win_migration_postimage1410(4,installed,4,4,installed,4,0,0,0,0));
 assert(win_migration_postimage1410(4,installed,4,4,installed,4,1,4,prior,4));
 assert(!win_migration_postimage1410(4,installed,4,4,installed,4,1,4,installed,4));
 assert(!win_migration_postimage1410(4,changed,4,4,installed,4,1,4,prior,4));
 assert(!win_migration_postimage1410(3,installed,4,4,installed,4,0,0,0,0));

 win_tx_reg147 claim={.root=2,.view=32};
 assert(win_migration_same_value1410(2,32,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(2,64,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(1,32,"Software\\Example","Name",&claim,"software\\example","NAME"));
 claim.root=1;
 assert(win_migration_same_value1410(1,64,"Software\\Example","Name",&claim,"software\\example","NAME"));
 assert(!win_migration_same_value1410(1,64,"Software\\Example","Other",&claim,"software\\example","NAME"));
 return 0;
}
