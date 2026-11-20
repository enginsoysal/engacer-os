/* No change-notification service is advertised: return its documented failure. */
static HANDLE MS f_FindFirstChangeNotificationW(const WCHAR*path,int subtree,unsigned filter){
 (void)subtree;if(!path||!filter||(filter&~0x17fu)){last8(87);return UINT64_MAX;}
 unsigned attributes=f_GetFileAttributesW(path);if(attributes==UINT32_MAX)return UINT64_MAX;
 if(!(attributes&16)){last8(267);return UINT64_MAX;}last8(50);return UINT64_MAX;
}
