/* Native M13 disk tools reuse the bounded trusted plans and setup compositor. */
static unsigned u13_framed,u13_width,u13_height,u13_accent;
static void u13_outline(control c,uint32_t color){
 gui6_rect(c.x,c.y,c.w,2,color);gui6_rect(c.x,c.y+c.h-2,c.w,2,color);gui6_rect(c.x,c.y,2,c.h,color);gui6_rect(c.x+c.w-2,c.y,2,c.h,color);
}
static void u13_button(unsigned x,unsigned y,unsigned w,const char*title,unsigned action,unsigned enabled,unsigned primary,unsigned selected){
 ui12_palette p=ui12_theme(0,accent);unsigned state=(!enabled?UI12_DISABLED:0)|(selected?UI12_SELECTED:0);ui12_style s=ui12_control_style(p,state,primary);
 ui73_round(x,y,w,40,UI12_RADIUS,s.border);ui73_round(x+2,y+2,w-4,36,UI12_RADIUS-2,s.fill);ui73_fit(x+12,y+9,w-24,title,UI12_BODY,s.ink);
 if(enabled&&controls<24)buttons[controls++]=(control){x,y,w,40,action};
}
static void u13_number(unsigned x,unsigned y,uint64_t n,const char*suffix,uint32_t ink){
 char b[64];decimal(n,b);unsigned at=0;while(b[at])++at;for(unsigned i=0;(b[at+i]=suffix[i]);++i){}label(x,y,b,UI12_BODY,ink);
}
static void u13_frame(void){
 ui12_palette p=ui12_theme(0,accent);
 if(!u13_framed||u13_width!=width||u13_height!=height||u13_accent!=accent){
  gui7_clip_reset();gui6_rect(0,0,screen->framebuffer_width,screen->framebuffer_height,UI13_SETUP_BACKDROP);ui73_shadow(left,top,width,height);ui73_round(left,top,width,height,16,p.paper);
  ui73_round(left,top,196,height,16,UI13_SETUP_BACKDROP);gui6_rect(left+180,top,16,height,UI13_SETUP_BACKDROP);
  ui73_fit(left+24,top+28,152,DISTRO_NAME,UI12_SECTION,0xffffff);label(left+24,top+76,"DISK TOOLS",UI12_SECONDARY,0xb4ced8);
  ui73_paragraph(left+24,top+132,148,4,"Inspect your disks. Review each change before applying it.",0xffffff);
  ui73_paragraph(left+24,top+height-90,148,3,"Your installation choices are kept.",0xb4ced8);
  u13_framed=1;u13_width=width;u13_height=height;u13_accent=accent;
 }
 gui6_rect(left+196,top+16,width-212,height-32,p.paper);label(body+12,top+29,"SETUP / DISK TOOLS",UI12_SECONDARY,p.muted);
 gui6_rect(body+12,top+65,width-276,2,p.line);
}
static void u13_working(void){
 ui12_palette p=ui12_theme(0,accent);unsigned x=body+12,y=top+98,w=width-276;
 gui6_rect(x,y,w,bottom-y,p.paper);label(x,y,"Applying disk changes",UI12_HEADING,p.ink);ui73_paragraph(x,y+64,w,3,"Keep the disk connected. The operation will be checked before it is reported complete.",p.muted);graphics9_flush();
}
static void u71_draw(unsigned unused_x,unsigned unused_y){
 (void)unused_x;(void)unused_y;unsigned x=body+12,y=top+98,w=width-276,h=bottom-y-12;ui12_palette p=ui12_theme(0,accent);unsigned old=focus;
 const char*title=u71_mode==1?"Disks and partitions":u71_mode==2?"Create a partition":u71_mode==3?"Choose a format":u71_mode==5?"Repair the partition table":"Review disk changes";
 label(x,y,title,UI12_HEADING,p.ink);char identity[64]="Disk ";decimal(u71_disk+1,identity+5);unsigned at=0;while(identity[at])++at;identity[at++]=' ';identity[at++]='/';identity[at++]=' ';decimal(u71_target.sectors/2048,identity+at);while(identity[at])++at;memcpy(identity+at," MiB",5);
 label(x,y+44,identity,UI12_BODY,p.ink);ui73_fit(x,y+70,w,u71_scheme(),UI12_SECONDARY,p.muted);
 unsigned writable=u71_state.sectors&&u71_device.sector_bytes==512,part=u71_row<u71_state.count,gap=u71_row>=u71_state.count&&u71_row<u71_state.count+u71_state.gaps;
 unsigned editable=writable&&u71_state.editable,mutable_part=editable&&part&&!u71_state.parts[u71_row].protected;
 if(u71_mode==1){
  unsigned total=u71_state.count+u71_state.gaps,panel=y+104,row_h=h<450?40:46,panel_h=32+row_h*4;
  ui73_round(x,panel,w,panel_h,UI12_RADIUS,p.line);ui73_round(x+2,panel+2,w-4,panel_h-4,UI12_RADIUS-2,p.surface);
  label(x+14,panel+8,"PARTITION / FREE SPACE",UI12_SECONDARY,p.muted);label(x+w-116,panel+8,"SIZE",UI12_SECONDARY,p.muted);
  if(!total)ui73_paragraph(x+16,panel+50,w-32,2,u71_state.scheme==D71_BLANK?"This disk has no partition table. Choose New GPT to prepare data partitions, or return to setup for automatic whole-disk installation.":"No editable partitions are available. Inspect the connection or the verified table copies.",p.muted);
  for(unsigned row=0;row<4;++row){unsigned item=u71_page*4+row;if(item>=total)break;unsigned yy=panel+28+row*row_h,selected=u71_row==item;uint64_t first,last;char name[48];const char*detail;
   if(item<u71_state.count){const d71_partition*v=&u71_state.parts[item];memcpy(name,"Partition ",10);decimal(v->index+1,name+10);first=v->first;last=v->last;detail=v->protected?"Protected system partition":v->format;}
   else{d71_gap v=u71_state.free[item-u71_state.count];first=v.first;last=v.last;memcpy(name,"Free space",11);detail="Available for a new partition";}
   uint32_t bg=selected?p.selection:p.surface;gui6_rect(x+4,yy,w-8,row_h-2,bg);if(selected)gui6_rect(x+4,yy,4,row_h-2,p.accent);
   if(controls<24)buttons[controls++]=(control){x+4,yy,w-8,row_h-2,300+row};ui73_fit(x+16,yy+2,w-150,name,UI12_BODY,p.ink);ui73_fit(x+16,yy+22,w-150,detail,UI12_SECONDARY,p.muted);u13_number(x+w-116,yy+10,(last-first+1)/2048," MiB",p.ink);
  }
  unsigned yy=panel+panel_h+10,cell=(w-24)/3;
  u13_button(x,yy,140,"Previous disk",201,storage_count()>1,0,0);u13_button(x+152,yy,140,"Next disk",202,storage_count()>1,0,0);u13_button(x+304,yy,100,"Refresh",205,1,0,0);
  u13_button(x+w-164,yy,76,"<",203,u71_page>0,0,0);u13_button(x+w-76,yy,76,">",204,(u71_page+1)*4<total,0,0);
  yy+=50;u13_button(x,yy,cell,"New partition",210,editable&&gap,0,0);u13_button(x+cell+12,yy,cell,"Format",212,mutable_part,0,0);u13_button(x+2*(cell+12),yy,cell,"Delete",211,mutable_part,0,0);
  yy+=50;u13_button(x,yy,cell,"New GPT",213,writable&&u71_state.scheme==D71_BLANK,0,0);u13_button(x+cell+12,yy,cell,"Clear disk",214,writable,0,0);u13_button(x+2*(cell+12),yy,cell,"Repair GPT",215,writable&&(u71_state.scheme==D71_GPT||u71_state.scheme==D71_DAMAGED)&&u71_state.valid_copies,0,0);
 }else if(u71_mode==2){
  label(x,y+112,"Partition size in MiB",UI12_BODY,p.ink);u13_button(x,y+144,w-184,u71_size,220,1,0,0);u13_button(x+w-172,y+144,172,"Use all free space",221,1,0,0);
  if(u71_state.scheme==D71_GPT){label(x,y+206,"Partition name",UI12_BODY,p.ink);u13_button(x,y+238,w,u71_name,222,1,0,0);}
  ui73_paragraph(x,y+304,w,3,"Creates an unformatted data partition. Existing partitions stay. Format the new partition afterward. Use Backspace to replace the suggested values.",p.muted);u13_button(x,y+h-114,220,"Review creation",223,1,1,0);
 }else if(u71_mode==3){
  ui73_paragraph(x,y+112,w,3,"Formatting removes files from the selected partition. Other partitions are kept.",0x994334);
  u13_button(x,y+188,w,"FAT32 - shared data, 64 MiB minimum",224,1,0,0);u13_button(x,y+242,w,"Engacer data - 1 MiB minimum",225,1,0,0);
  ui73_paragraph(x,y+304,w,3,"Quick format does not securely erase old contents. Resizing, filesystem conversion and data-preserving dual boot are not available.",p.muted);
 }else if(u71_mode==5){
  ui73_paragraph(x,y+112,w,3,"Choose the verified table copy to keep. The wrong copy can hide partitions. Filesystem data is not written.",0x994334);
  label(x,y+200,(u71_state.valid_copies&1)?"Primary copy verified":"Primary copy invalid",UI12_BODY,p.ink);label(x,y+232,(u71_state.valid_copies&2)?"Backup copy verified":"Backup copy invalid",UI12_BODY,p.ink);
  unsigned cell=(w-12)/2;u13_button(x,y+284,cell,"Use primary GPT",229,!!(u71_state.valid_copies&1),0,0);u13_button(x+cell+12,y+284,cell,"Use backup GPT",230,!!(u71_state.valid_copies&2),0,0);
 }else{
  ui73_paragraph(x,y+112,w,2,u71_title(u71_op),p.ink);
  if(u71_op==D71_CREATE){ui73_fit(x,y+176,w,u71_plan.name,UI12_BODY,p.ink);u13_number(x,y+212,(u71_plan.last-u71_plan.first+1)/2048," MiB new partition",p.ink);}
  else if(u71_op==D71_DELETE||u71_op==D71_FAT32||u71_op==D71_NATIVE)u13_number(x,y+176,u71_plan.index+1," - partition number",p.ink);
  ui73_paragraph(x,y+258,w,3,u71_op==D71_ERASE?"All partitions on this disk become inaccessible. Other disks are kept. Quick operations do not securely erase old data.":u71_op==D71_CREATE?"This creates an unformatted partition. Other partitions are kept. Check the selected disk and size before applying.":"Only the reviewed target changes. Formatting or deleting a partition loses its files. Quick operations are not secure erasure.",0x994334);
  u13_button(x,y+h-164,w,u71_consent?"[x] I understand these disk changes":"[ ] I understand these disk changes",226,1,0,u71_consent);
  unsigned cell=(w-12)/2;u13_button(x,y+h-114,cell,"Keep / Cancel",227,1,1,0);u13_button(x+cell+12,y+h-114,cell,"Apply changes",228,u71_consent,0,0);
 }
 if(u71_notice)ui73_paragraph(x,bottom-42,w,2,u71_notice,0x994334);
 else if(u71_mode==1)ui73_paragraph(x,bottom-42,w,2,!writable?"Inspection only. This device cannot be changed by the supported disk tools.":"Select a partition to format or delete it; select free space to create one. Every change needs review.",p.muted);
 u13_button(x,bottom+24,180,u71_mode==1?"Back to setup":"Back",200,1,0,0);
 focus=old<controls?old:0;if(focus<controls)u13_outline(buttons[focus],p.ink);
}
