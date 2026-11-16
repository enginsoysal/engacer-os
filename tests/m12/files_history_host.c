/* Location identity and bounded real back/forward semantics, independent of I/O. */
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <engine/ui/files12.h>
static ui12_file_location location(unsigned provider,unsigned context,const char*path){ui12_file_location l={0};l.provider=provider;l.context=context;l.disk=2;l.part=0xffffffffu;snprintf(l.path,sizeof(l.path),"%s",path);return l;}
int main(void){
 struct {uint64_t before;ui12_file_history history;uint64_t after;} guarded={.before=0x123456789abcdef0,.after=0xfedcba9876543210};
 ui12_file_history*h=&guarded.history;
 ui12_file_location docs=location(UI12_NATIVE,0,"/Users/Owner/Documents"),drives=location(UI12_USB_DRIVES,0,""),root=location(UI12_USB_FOLDER,7,"/"),games=location(UI12_USB_FOLDER,7,"/Games"),downloads=location(UI12_NATIVE,0,"/Users/Owner/Downloads"),pictures=location(UI12_NATIVE,0,"/Users/Owner/Pictures");
 ui12_history_push(h,&docs,&docs);assert(h->count==1&&!ui12_history_can(h,0)&&!ui12_history_can(h,1));
 ui12_history_push(h,&docs,&drives);ui12_history_push(h,&drives,&root);ui12_history_push(h,&root,&games);ui12_history_push(h,&games,&downloads);
 assert(h->count==5&&h->position==4);--h->position;assert(ui12_location_equal(&h->locations[h->position],&games));--h->position;assert(ui12_location_equal(&h->locations[h->position],&root));--h->position;assert(ui12_location_equal(&h->locations[h->position],&drives));++h->position;++h->position;
 games.offset=6;ui12_history_push(h,&games,&pictures);assert(h->count==5&&!ui12_history_can(h,1)&&h->locations[3].offset==6&&ui12_location_equal(&h->locations[4],&pictures));
 ui12_file_location replacement=root;replacement.context=8;assert(!ui12_location_equal(&root,&replacement));replacement=root;replacement.part=1;assert(!ui12_location_equal(&root,&replacement));replacement=root;replacement.disk=3;assert(!ui12_location_equal(&root,&replacement));
 memset(h,0,sizeof(*h));ui12_history_push(h,&root,&root);replacement=root;replacement.context=8;ui12_history_push(h,&root,&replacement);assert(h->count==2&&h->locations[0].context==7&&h->locations[1].context==8);
 replacement.offset=4;ui12_history_push(h,&h->locations[1],&replacement);assert(h->count==2&&h->locations[1].offset==4);
 for(unsigned i=0;i<10000;++i){ui12_file_location before=h->locations[h->position],next=location(UI12_NATIVE,0,"");snprintf(next.path,sizeof(next.path),"/folder-%u",i);ui12_history_push(h,&before,&next);assert(h->count<=8&&h->position+1==h->count&&guarded.before==0x123456789abcdef0&&guarded.after==0xfedcba9876543210);}
 assert(!strcmp(h->locations[0].path,"/folder-9992")&&!strcmp(h->locations[7].path,"/folder-9999"));
 h->count=9;h->position=8;ui12_history_push(h,&docs,&docs);assert(h->count==1&&h->position==0&&ui12_location_equal(&h->locations[0],&docs));
 for(int height=356;height<=2160;++height){unsigned rows=ui12_usb_rows(height);assert(rows>=1&&rows<=6);assert(184+(int)(rows-1)*44+36<=height-82);if(ui12_files_sidebar(700,height))assert(142+38+7*38+36<=height-82);}
 assert(sizeof(ui12_file_location)==276&&sizeof(ui12_file_history)==2216);
 puts("PASS: native/USB collection/leased USB history, back/forward, branch replacement, offset retention, generation/partition/device isolation, 10000 bounded transitions and 1805 row layouts.");return 0;
}
