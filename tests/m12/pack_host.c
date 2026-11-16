#define _CRT_SECURE_NO_WARNINGS
#include <engine/install/pack12.h>
#include <stdio.h>
#include <string.h>
int main(int argc,char**argv){
    if(argc!=3)return 2;
    FILE*in=fopen(argv[1],"rb"),*out=fopen(argv[2],"wb");if(!in||!out)return 3;
    uint8_t source[8192],guarded[4096+32];uint32_t count;
    if(fread(&count,4,1,in)!=1)return 4;
    for(unsigned i=0;i<count;++i){
        uint32_t size;if(fread(&size,4,1,in)!=1||size>sizeof(source)||fread(source,1,size,in)!=size)return 5;
        memset(guarded,0xa5,sizeof(guarded));
        uint32_t valid=pack12_decode(source,size,guarded+16);
        for(unsigned j=0;j<16;++j)if(guarded[j]!=0xa5||guarded[4112+j]!=0xa5)return 6;
        if(fwrite(&valid,4,1,out)!=1||fwrite(guarded+16,1,4096,out)!=4096)return 7;
    }
    /* Record-level impossible flags and inconsistent length metadata. */
    uint8_t h[2]={1,0};
    if(pack12_size(0xc0000000u,h,2)||pack12_size(0x40000000u,h,2)||pack12_size(0,h,4095))return 8;
    h[0]=0;h[1]=16;if(pack12_size(0x40000000u,h,4098))return 9;
    if(pack12_decode(0,1,guarded)||pack12_decode(source,0,guarded)||pack12_decode(source,1,0))return 10;
    fclose(in);fclose(out);return 0;
}
