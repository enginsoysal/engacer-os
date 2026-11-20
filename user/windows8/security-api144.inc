/* No LSA policy service or machine-account rights exist in this profile. */
static int MS f_LsaOpenPolicy(const void*system,void*attributes,unsigned access,HANDLE*out){(void)system;(void)attributes;(void)access;if(!out)return(int)0xc000000du;*out=0;return(int)0xc00000bbu;}
static int MS f_LsaClose(HANDLE policy){(void)policy;return(int)0xc0000008u;}
static int MS f_LsaAddAccountRights(HANDLE policy,const void*sid,const void*rights,unsigned count){(void)policy;(void)sid;(void)rights;(void)count;return(int)0xc0000008u;}
static int MS f_LookupAccountNameW(const WCHAR*system,const WCHAR*name,void*sid,unsigned*sid_bytes,WCHAR*domain,unsigned*domain_units,unsigned*use){(void)system;(void)name;(void)sid;(void)domain;if(sid_bytes)*sid_bytes=0;if(domain_units)*domain_units=0;if(use)*use=0;last8(50);return 0;}
static int MS f_GetUserNameW(WCHAR*out,unsigned*capacity){if(!capacity){last8(87);return 0;}const char*name=job8->user_root;for(unsigned i=0;job8->user_root[i];++i)if(job8->user_root[i]=='/')name=job8->user_root+i+1;WCHAR wide[128];int n=utf8_to16(name,wide,128);if(n<0){last8(1113);return 0;}unsigned required=(unsigned)n+1,old=*capacity;*capacity=required;if(!out||old<required){last8(122);return 0;}memcpy(out,wide,required*2);return 1;}

/* No shell namespace service exists yet. Optional icon queries must receive a
 * typed failure, never a fabricated PIDL or success pointer. */
static int32_t MS f_SHGetSpecialFolderLocation(HANDLE owner,int folder,void**out){(void)owner;(void)folder;if(!out)return(int32_t)0x80070057u;*out=0;return(int32_t)0x80004001u;}


