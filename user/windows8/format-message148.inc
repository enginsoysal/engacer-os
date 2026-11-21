/* Bounded English system-message profile; unsupported IDs fail explicitly. */
static unsigned MS f_FormatMessageA(unsigned flags,const void*source,unsigned code,unsigned language,void*out,unsigned capacity,void*arguments){
 (void)source;(void)arguments;
 if(!(flags&0x1000u)||(flags&~0x1300u)){last8(50);return 0;}
 if(language&&language!=0x400&&language!=0x409){last8(1815);return 0;}
 const char*message=0;switch(code){
 case 0:message="The operation completed successfully.\r\n";break;
 case 2:message="The system cannot find the file specified.\r\n";break;
 case 3:message="The system cannot find the path specified.\r\n";break;
 case 5:message="Access is denied.\r\n";break;
 case 6:message="The handle is invalid.\r\n";break;
 case 8:case 14:message="Not enough memory resources are available to complete this operation.\r\n";break;
 case 19:message="The media is write protected.\r\n";break;
 case 29:case 30:case 1117:message="The request could not be performed because of an I/O device error.\r\n";break;
 case 32:message="The process cannot access the file because it is being used by another process.\r\n";break;
 case 33:message="The process cannot access the file because another process has locked a portion of the file.\r\n";break;
 case 38:message="Reached the end of the file.\r\n";break;
 case 50:message="The request is not supported.\r\n";break;
 case 80:case 183:message="The file already exists.\r\n";break;
 case 87:message="The parameter is incorrect.\r\n";break;
 case 112:message="There is not enough space on the disk.\r\n";break;
 case 122:message="The data area passed to a system call is too small.\r\n";break;
 case 145:message="The directory is not empty.\r\n";break;
 case 223:message="The file size exceeds the supported limit.\r\n";break;
 case 998:message="Invalid access to memory location.\r\n";break;
 default:last8(317);return 0;}
 unsigned bytes=len8(message)+1;if(!(flags&0x100)&&capacity<bytes){last8(122);return 0;}if(!out||sys8(W8_SYS_ACCESS,(uint64_t)(uintptr_t)out,flags&0x100?8:bytes,2,0,0)){last8(998);return 0;}
 if(flags&0x100){if(capacity>65536){last8(8);return 0;}unsigned size=capacity>bytes?capacity:bytes;char*text=alloc8(size);if(!text){last8(8);return 0;}memcpy(text,message,bytes);*(char**)out=text;}
 else{if(capacity<bytes){last8(122);return 0;}memcpy(out,message,bytes);}return bytes-1;
}
