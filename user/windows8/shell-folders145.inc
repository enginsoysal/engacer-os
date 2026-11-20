/* Physical user folders retain the existing checked file-provider grants. */
static int MS f_SHGetSpecialFolderPathW(HANDLE owner,WCHAR*out,int folder,int create){
 (void)owner;if(!out){last8(87);return 0;}out[0]=0;const WCHAR*tail;
 switch(folder){case 5:tail=u"Documents";break;case 16:tail=u"Desktop";break;case 13:tail=u"Music";break;case 14:tail=u"Videos";break;case 39:tail=u"Pictures";break;case 40:tail=u"";break;default:last8(50);return 0;}
 WCHAR path[260];unsigned length=f_GetEnvironmentVariableW(u"USERPROFILE",path,260);if(!length)return 0;if(length>=260){last8(206);return 0;}unsigned suffix=wlen8(tail);if(suffix){if(length+suffix+1>=260){last8(206);return 0;}path[length++]='\\';memcpy(path+length,tail,(suffix+1)*2);}
 unsigned attributes=f_GetFileAttributesW(path);if(attributes==UINT32_MAX){unsigned error=f_GetLastError();if(!create||(error!=2&&error!=3))return 0;if(!f_CreateDirectoryW(path,0))return 0;attributes=f_GetFileAttributesW(path);if(attributes==UINT32_MAX)return 0;}
 if(!(attributes&16)){last8(267);return 0;}widecopy8(out,path,260);return 1;
}
