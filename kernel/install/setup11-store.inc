/* Commit versioned preferences before publishing an installed activation record. */
static unsigned setup_put11(const char *path,const void *value,unsigned size){
 return v6_put(&volume,path,size,source_memory,(void*)value)||v6_verify(&volume,path);
}
static void setup_path11(char *out,const char *prefix,const char *user){
 unsigned n=0;while(*prefix)out[n++]=*prefix++;while(*user)out[n++]=*user++;memcpy(out+n,".bin",5);
}
static unsigned setup_store11(const m6_preferences*p){
 const setup_options11 *s=setup_choices11();char path[128];
 unsigned keyboard[2]={0x30314c4b,s->layout};
 appearance_record11 a={0x41313145,1,p->accent,s->dark,s->scale,s->wallpaper,s->pattern,0,{{0}}};
 unsigned guide[3]={0x47313145,1,!p->guide};
 if(setup_put11("/System/Settings/keyboard10.bin",keyboard,sizeof(keyboard)))return B_IO;
 setup_path11(path,"/System/Settings/appearance11-",p->user);
 if(setup_put11(path,&a,sizeof(a)))return B_IO;
 setup_path11(path,"/System/Settings/firstboot11-",p->user);
 return setup_put11(path,guide,sizeof(guide))?B_IO:B_OK;
}
