/* Logical compatibility namespace already used by MSI system-folder properties
 * and the guarded cmd/xcopy aliases; this does not grant writes or add DLLs. */
static unsigned MS f_GetSystemDirectoryW(WCHAR*out,unsigned capacity){
 static const WCHAR path[]=u"C:\\Windows\\System32";
 unsigned length=(unsigned)(sizeof(path)/sizeof(path[0]))-1;
 if(capacity<=length)return length+1;
 if(!out){last8(87);return 0;}
 memcpy(out,path,sizeof(path));return length;
}
