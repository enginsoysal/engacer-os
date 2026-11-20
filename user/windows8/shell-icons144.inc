/* Own generic system icons, not application-owned resources or a shell namespace. */
static HANDLE shell_lists144[2];
static HANDLE shell_icon144(unsigned size,unsigned folder){lock_enter142(&image_lock144);image_object144*icon=image_new144(1,size,size);if(!icon){lock_leave142(&image_lock144);return 0;}size_t bytes=(size_t)size*size*4;icon->pixels=image_memory144(bytes);if(!icon->pixels){image_destroy144(icon);lock_leave142(&image_lock144);return 0;}
 for(unsigned y=0;y<size;++y)for(unsigned x=0;x<size;++x){unsigned xx=x*16/size,yy=y*16/size;uint32_t pixel=0;if(folder){if(xx>=1&&xx<=14&&yy>=5&&yy<=13)pixel=0xffe8b853;if(xx>=2&&xx<=7&&yy>=3&&yy<=5)pixel=0xffd7a345;if(xx>=1&&xx<=14&&yy==6)pixel=0xfff8d88e;}else{if(xx>=3&&xx<=12&&yy>=1&&yy<=14)pixel=0xffdbe4ec;if(xx>=4&&xx<=11&&yy>=2&&yy<=13)pixel=0xfffafcfe;if(xx>=5&&xx<=10&&(yy==7||yy==9||yy==11))pixel=0xff708594;if(xx>=9&&yy<=4&&xx+yy>12)pixel=0xffb6c8d7;}icon->pixels[y*size+x]=pixel;}
 HANDLE result=icon->handle;lock_leave142(&image_lock144);return result;
}
static HANDLE shell_list144(unsigned small){unsigned slot=small?0:1,size=small?16:32;lock_enter142(&image_lock144);HANDLE list=shell_lists144[slot];unsigned exists=0;for(image_object144*i=images144;i;i=i->next)if(i->handle==list&&i->kind==3){exists=1;break;}lock_leave142(&image_lock144);if(exists)return list;list=f_ImageList_Create((int)size,(int)size,0x21,2,0);if(!list)return 0;for(unsigned n=0;n<2;++n){HANDLE icon=shell_icon144(size,n);if(!icon||f_ImageList_ReplaceIcon(list,-1,icon)!=(int)n){if(icon)f_DestroyIcon(icon);f_ImageList_Destroy(list);return 0;}f_DestroyIcon(icon);}shell_lists144[slot]=list;return list;}
typedef struct {HANDLE icon;int index;unsigned attributes;WCHAR name[260],type[80];} shell_fileinfo144;
_Static_assert(sizeof(shell_fileinfo144)==696,"Win64 SHFILEINFOW layout");
static uint64_t MS f_SHGetFileInfoW(const WCHAR*path,unsigned attributes,void*output,unsigned bytes,unsigned flags){if(!path||!output||bytes<sizeof(shell_fileinfo144)){last8(87);return 0;}shell_fileinfo144*out=output;memset(out,0,sizeof(*out));out->index=-1;if(flags&~0x4713u){last8(50);return 0;}if(!(flags&0x10)){attributes=f_GetFileAttributesW(path);if(attributes==UINT32_MAX)return 0;}unsigned folder=(attributes&0x10)!=0;out->index=(int)folder;
 if(flags&0x200){const WCHAR*base=path;for(const WCHAR*p=path;*p;++p)if(*p=='/'||*p=='\\')base=p+1;widecopy8(out->name,base,260);}if(flags&0x400)widecopy8(out->type,folder?u"File folder":u"File",80);
 if(flags&0x100){out->icon=shell_icon144(flags&1?16:32,folder);if(!out->icon)return 0;}if(flags&0x4000){HANDLE list=shell_list144(flags&1);if(!list){if(out->icon)f_DestroyIcon(out->icon);out->icon=0;return 0;}return list;}return 1;
}
/* Initial own stock view-toolbar artwork; item 8 is the parent-folder action. */
static HANDLE shell_view_icon144(unsigned size,unsigned index){HANDLE handle=shell_icon144(size,index==8||index==10);if(!handle)return 0;lock_enter142(&image_lock144);image_object144*icon=image_find144(handle,1);if(icon)for(unsigned y=0;y<size;++y)for(unsigned x=0;x<size;++x){unsigned xx=x*16/size,yy=y*16/size;uint32_t color=0;
 if(index==8){if((xx>=7&&xx<=9&&yy>=4&&yy<=12)||(yy>=2&&yy<=6&&xx>=8-(yy-2)&&xx<=8+(yy-2)))color=0xff225f83;}
 else if(index<=3){unsigned step=index==0?6:4;if(xx>=2&&xx<14&&yy>=2&&yy<14&&((xx-2)%step)<step-1&&((yy-2)%step)<step-1)color=0xff4b86ac;if(index>=2&&xx>=7&&xx<14&&(yy==3||yy==7||yy==11))color=0xff35576d;}
 else if(index==10){if((xx==11&&yy>=8&&yy<=12)||(yy==10&&xx>=9&&xx<=13))color=0xff225f83;}
 else if(index==9){if(xx>=2&&xx<=13&&yy>=4&&yy<=11)color=0xff5f91b1;if(xx>=4&&xx<=11&&yy>=6&&yy<=9)color=0xffd4edf8;}
 else if(xx>=4&&xx<=12&&(yy==5||yy==8||yy==11)&&xx<6+(index%4)*2)color=0xff4b86ac;
 if(color)icon->pixels[y*size+x]=color;}
 lock_leave142(&image_lock144);return handle;}
static HANDLE MS f_CreateToolbarEx(HANDLE parent,unsigned style,unsigned id,int bitmap_count,HANDLE module,unsigned bitmap_id,const toolbar_button144*buttons,int button_count,int button_width,int button_height,int bitmap_width,int bitmap_height,unsigned structure_size){
 if(structure_size!=32||bitmap_count<0||bitmap_count>32||button_count<0||button_count>64||(!buttons&&button_count)||button_width<0||button_height<0||bitmap_width<0||bitmap_height<0){last8(87);return 0;}
 if(module==UINT64_MAX&&bitmap_id!=4&&bitmap_id!=5){last8(50);return 0;}
 HANDLE list=0;if(bitmap_count){int width=bitmap_width?bitmap_width:16,height=bitmap_height?bitmap_height:16;if(width!=height||width>64){last8(50);return 0;}list=f_ImageList_Create(width,height,0x21,bitmap_count,0);if(!list)return 0;
 if(module==UINT64_MAX){for(int n=0;n<bitmap_count;++n){HANDLE icon=shell_view_icon144((unsigned)width,(unsigned)n);if(!icon||f_ImageList_ReplaceIcon(list,-1,icon)!=n){if(icon)f_DestroyIcon(icon);f_ImageList_Destroy(list);return 0;}f_DestroyIcon(icon);}}
 else{HANDLE bitmap=f_LoadBitmapW(module,(const WCHAR*)(uintptr_t)bitmap_id);if(!bitmap||f_ImageList_AddMasked(list,bitmap,0xc0c0c0)<0){if(bitmap)f_DeleteObject(bitmap);f_ImageList_Destroy(list);return 0;}f_DeleteObject(bitmap);}}
 HANDLE window=f_CreateWindowExW(0,u"ToolbarWindow32",u"",style,0,0,0,0,parent,id,0,0);if(!window){if(list)f_ImageList_Destroy(list);return 0;}f_SendMessageW(window,0x41e,32,0);if(list)f_SendMessageW(window,0x430,0,(int64_t)list);if(button_width&&button_height)f_SendMessageW(window,0x41f,0,(button_width&65535)|((int64_t)(button_height&65535)<<16));if(button_count&&!f_SendMessageW(window,0x444,(unsigned)button_count,(int64_t)(uintptr_t)buttons)){f_DestroyWindow(window);if(list)f_ImageList_Destroy(list);return 0;}ui_window_runtime144*w=ui_window_lookup144(window);if(w&&w->control)((control_state144*)w->control)->checked=list!=0;f_SendMessageW(window,0x421,0,0);return window;
}
