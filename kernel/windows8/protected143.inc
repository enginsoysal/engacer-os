/* Internal namespaces use trusted principal identities, never environment values. */
static void protected_hash143(const char*text,char*out){uint8_t hash[32];static const char hex[]="0123456789abcdef";engine_sha256(text,length8(text),hash);for(unsigned i=0;i<16;++i){out[i*2]=hex[hash[i]>>4];out[i*2+1]=hex[hash[i]&15];}out[32]=0;}
static void protected_root143(const char*kind,char*out){char hash[33];protected_hash143(input8.user_root,hash);copy8(out,"/Data/Windows/",256);path_append143(out,hash,256);path_append143(out,"/",256);path_append143(out,kind,256);}
static unsigned protected_mkdir143(const char*path){const v6_entry*entry=find8(path);if(entry)return entry->kind==2?0:13;return v6_mkdir(m6_volume(),path)?1117:0;}
static unsigned protected_prepare143(const char*directory){char path[256];copy8(path,directory,256);for(unsigned i=1;path[i];++i)if(path[i]=='/'){path[i]=0;unsigned error=protected_mkdir143(path);path[i]='/';if(error)return error;}return protected_mkdir143(path);}
