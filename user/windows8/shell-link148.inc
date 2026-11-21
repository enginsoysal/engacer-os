/* Selected in-process ShellLink COM contracts. Real files use MS-SHLLINK.
 * No RPC, shell namespace PIDLs, search resolution or shortcut activation. */
#include "shell-link-format148.h"
typedef struct shell_link148 {void**link;void**persist;unsigned refs,dirty,show,revision;int icon_index;char*text[5];char*current;} shell_link148;
static shell_link148*shell_links148[32];static lock142 shell_link_lock148;
static void*shell_link_vtable148[21],*shell_persist_vtable148[9];static unsigned shell_tables_ready148;
static const uint8_t shell_clsid148[16]={1,0x14,2,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
static const uint8_t shell_iid148[16]={0xf9,0x14,2,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
static const uint8_t persist_iid148[16]={0x0b,1,0,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
static const uint8_t persist_base_iid148[16]={0x0c,1,0,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
static const uint8_t unknown_iid148[16]={0,0,0,0,0,0,0,0,0xc0,0,0,0,0,0,0,0x46};
static int shell_hr148(unsigned error){return error?(int)(0x80070000u|error):0;}
static unsigned shell_file_error148(void){unsigned error=f_GetLastError();return error?error:29;}
static unsigned shell_access148(const void*p,unsigned bytes,unsigned write){return p&&!sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)p,bytes,write?2:1,0,0);}
static shell_link148*shell_find148(const void*p){for(unsigned i=0;i<32;++i){shell_link148*s=shell_links148[i];if(s&&(p==s||p==&s->persist))return s;}return 0;}
static int MS shell_notimpl148(void*self){(void)self;return(int)0x80004001u;}
static int MS shell_query148(void*self,const void*iid,void**out){
 if(!shell_access148(out,8,1))return(int)0x80004003u;*out=0;if(!shell_access148(iid,16,0))return(int)0x80004003u;
 lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);int result=(int)0x80004002u;
 if(!s)result=(int)0x80070006u;
 else if(!memcmp(iid,unknown_iid148,16)||!memcmp(iid,shell_iid148,16)){*out=s;if(s->refs>=1048576)fail8("Shell link reference quota exceeded.");++s->refs;result=0;}
 else if(!memcmp(iid,persist_iid148,16)||!memcmp(iid,persist_base_iid148,16)){*out=&s->persist;if(s->refs>=1048576)fail8("Shell link reference quota exceeded.");++s->refs;result=0;}
 lock_leave142(&shell_link_lock148);return result;
}
static unsigned shell_ref148(shell_link148*s){if(s->refs>=1048576)fail8("Shell link reference quota exceeded.");return ++s->refs;}
static unsigned MS shell_addref148(void*self){lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);unsigned refs=s?shell_ref148(s):0;lock_leave142(&shell_link_lock148);return refs;}
static unsigned MS shell_release148(void*self){lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);unsigned refs=0;if(s){refs=--s->refs;if(!refs){for(unsigned i=0;i<32;++i)if(shell_links148[i]==s)shell_links148[i]=0;for(unsigned i=0;i<5;++i)if(s->text[i])free8(s->text[i]);if(s->current)free8(s->current);free8(s);}}lock_leave142(&shell_link_lock148);return refs;}
static int shell_set148(void*self,const WCHAR*text,unsigned field){
 if(!text)return(int)0x80070057u;WCHAR wide[260];unsigned n=0;
 for(;n<260;++n){if(!shell_access148(text+n,2,0))return(int)0x80004003u;wide[n]=text[n];if(!wide[n])break;}if(n==260)return shell_hr148(206);
 char utf8[1040];unsigned status=msit_fromwide147(wide,utf8,sizeof(utf8));if(status)return shell_hr148(status);
 if(field==0&&(!n||n>255||utf8[1]!=':'||utf8[2]!='\\'||(utf8[0]!='C'&&utf8[0]!='c')))return shell_hr148(50);
 unsigned bytes=len8(utf8)+1;char*copy=alloc8(bytes);if(!copy)return(int)0x8007000eu;memcpy(copy,utf8,bytes);
 lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(!s){lock_leave142(&shell_link_lock148);free8(copy);return shell_hr148(6);}char*old=s->text[field];s->text[field]=copy;s->dirty=1;++s->revision;lock_leave142(&shell_link_lock148);if(old)free8(old);return 0;
}
static int shell_get148(void*self,WCHAR*out,int capacity,unsigned field){
 if(capacity<=0||capacity>32768||!shell_access148(out,(unsigned)capacity*2,1))return(int)0x80070057u;out[0]=0;
 lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);unsigned units=(unsigned)capacity;unsigned status=s?msit_outwide147(s->text[field]?s->text[field]:"",out,&units):6;lock_leave142(&shell_link_lock148);return shell_hr148(status);
}
static int MS shell_path_set148(void*s,const WCHAR*t){return shell_set148(s,t,0);}
static int MS shell_work_set148(void*s,const WCHAR*t){return shell_set148(s,t,1);}
static int MS shell_args_set148(void*s,const WCHAR*t){return shell_set148(s,t,2);}
static int MS shell_desc_set148(void*s,const WCHAR*t){return shell_set148(s,t,3);}
static int MS shell_desc_get148(void*s,WCHAR*t,int n){return shell_get148(s,t,n,3);}
static int MS shell_work_get148(void*s,WCHAR*t,int n){return shell_get148(s,t,n,1);}
static int MS shell_args_get148(void*s,WCHAR*t,int n){return shell_get148(s,t,n,2);}
static int MS shell_icon_set148(void*self,const WCHAR*path,int index){int status=shell_set148(self,path,4);if(status)return status;lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(s){s->icon_index=index;++s->revision;}lock_leave142(&shell_link_lock148);return s?0:shell_hr148(6);}
static int MS shell_icon_get148(void*self,WCHAR*out,int capacity,int*index){if(!shell_access148(index,4,1))return(int)0x80004003u;int status=shell_get148(self,out,capacity,4);if(status)return status;lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(s)*index=s->icon_index;lock_leave142(&shell_link_lock148);return s?0:shell_hr148(6);}
static int MS shell_show_set148(void*self,int show){if(show!=1&&show!=3&&show!=7)return shell_hr148(87);lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(s){s->show=(unsigned)show;s->dirty=1;++s->revision;}lock_leave142(&shell_link_lock148);return s?0:shell_hr148(6);}
static int MS shell_show_get148(void*self,int*out){if(!shell_access148(out,4,1))return(int)0x80004003u;lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(s)*out=(int)s->show;lock_leave142(&shell_link_lock148);return s?0:shell_hr148(6);}
static int MS shell_class148(void*self,void*out){if(!shell_access148(out,16,1))return(int)0x80004003u;lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);if(s)memcpy(out,shell_clsid148,16);lock_leave142(&shell_link_lock148);return s?0:shell_hr148(6);}
static int MS shell_dirty148(void*self){lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);int status=s?(s->dirty?0:1):shell_hr148(6);lock_leave142(&shell_link_lock148);return status;}
static int MS shell_save148(void*self,const WCHAR*filename,int remember){
 /* No implicit destination authority: the existing file layer checks every save. */
 WCHAR destination[260];unsigned revision=0,status=0,bytes=0;char*remembered=0;
 if(filename){unsigned n=0;for(;n<260;++n){if(!shell_access148(filename+n,2,0))return(int)0x80004003u;destination[n]=filename[n];if(!destination[n])break;}if(n==260)return shell_hr148(206);}
 else{lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);unsigned units=260;status=s&&s->current?msit_outwide147(s->current,destination,&units):2;lock_leave142(&shell_link_lock148);if(status)return shell_hr148(status);}
 if(filename&&remember){char utf8[1040];status=msit_fromwide147(destination,utf8,sizeof(utf8));if(status)return shell_hr148(status);unsigned n=len8(utf8)+1;remembered=alloc8(n);if(!remembered)return(int)0x8007000eu;memcpy(remembered,utf8,n);}
 uint8_t*data=alloc8(4096);if(!data){if(remembered)free8(remembered);return(int)0x8007000eu;}
 lock_enter142(&shell_link_lock148);shell_link148*s=shell_find148(self);
 if(!s||!s->text[0])status=s?87:6;
 else{revision=s->revision;status=shell_link_encode148(s->text[0],s->text[1]?s->text[1]:"",s->text[2]?s->text[2]:"",s->text[3]?s->text[3]:"",s->text[4],s->icon_index,s->show,0,data,4096,&bytes);}
 lock_leave142(&shell_link_lock148);
 if(!status){HANDLE file=f_CreateFileW(destination,0x40000000u,0,0,2,0x80,0);if(file==UINT64_MAX)status=shell_file_error148();else{unsigned written=0;if(!f_WriteFile(file,data,bytes,&written,0))status=shell_file_error148();else if(written!=bytes)status=29;else if(!f_FlushFileBuffers(file))status=shell_file_error148();if(!f_CloseHandle(file)&&!status)status=shell_file_error148();}}
 free8(data);if(!status&&(!filename||remember)){lock_enter142(&shell_link_lock148);s=shell_find148(self);if(s){if(s->revision==revision)s->dirty=0;if(remembered){char*old=s->current;s->current=remembered;remembered=old;}}lock_leave142(&shell_link_lock148);}if(remembered)free8(remembered);return shell_hr148(status);
}
static void shell_tables148(void){
 if(shell_tables_ready148)return;shell_tables_ready148=1;
 for(unsigned i=0;i<21;++i)shell_link_vtable148[i]=(void*)shell_notimpl148;for(unsigned i=0;i<9;++i)shell_persist_vtable148[i]=(void*)shell_notimpl148;
 shell_link_vtable148[0]=(void*)shell_query148;shell_link_vtable148[1]=(void*)shell_addref148;shell_link_vtable148[2]=(void*)shell_release148;
 shell_link_vtable148[6]=(void*)shell_desc_get148;shell_link_vtable148[7]=(void*)shell_desc_set148;shell_link_vtable148[8]=(void*)shell_work_get148;shell_link_vtable148[9]=(void*)shell_work_set148;shell_link_vtable148[10]=(void*)shell_args_get148;shell_link_vtable148[11]=(void*)shell_args_set148;shell_link_vtable148[14]=(void*)shell_show_get148;shell_link_vtable148[15]=(void*)shell_show_set148;shell_link_vtable148[16]=(void*)shell_icon_get148;shell_link_vtable148[17]=(void*)shell_icon_set148;shell_link_vtable148[20]=(void*)shell_path_set148;
 shell_persist_vtable148[0]=(void*)shell_query148;shell_persist_vtable148[1]=(void*)shell_addref148;shell_persist_vtable148[2]=(void*)shell_release148;shell_persist_vtable148[3]=(void*)shell_class148;shell_persist_vtable148[4]=(void*)shell_dirty148;shell_persist_vtable148[6]=(void*)shell_save148;
}
static int MS f_CoCreateInstance(const void*clsid,void*outer,unsigned context,const void*iid,void**out){
 if(!shell_access148(out,8,1))return(int)0x80004003u;*out=0;if(!shell_access148(clsid,16,0)||!shell_access148(iid,16,0))return(int)0x80004003u;
 if(outer)return(int)0x80040110u;if(!(context&1u)||(context&~0x17u))return(int)0x80040154u;
 lock_enter142(&apartment_lock144);unsigned initialized=apartment_find144(tid142())!=0;lock_leave142(&apartment_lock144);if(!initialized)return(int)0x800401f0u;
 if(memcmp(clsid,shell_clsid148,16))return(int)0x80040154u;
 if(memcmp(iid,shell_iid148,16)&&memcmp(iid,unknown_iid148,16)&&memcmp(iid,persist_iid148,16)&&memcmp(iid,persist_base_iid148,16))return(int)0x80004002u;
 lock_enter142(&shell_link_lock148);unsigned slot=0;while(slot<32&&shell_links148[slot])++slot;if(slot==32){lock_leave142(&shell_link_lock148);return(int)0x8007000eu;}
 shell_link148*s=calloc8(1,sizeof(*s));if(!s){lock_leave142(&shell_link_lock148);return(int)0x8007000eu;}shell_tables148();s->link=shell_link_vtable148;s->persist=shell_persist_vtable148;s->refs=1;s->show=1;shell_links148[slot]=s;*out=(!memcmp(iid,persist_iid148,16)||!memcmp(iid,persist_base_iid148,16))?(void*)&s->persist:s;lock_leave142(&shell_link_lock148);return 0;
}
