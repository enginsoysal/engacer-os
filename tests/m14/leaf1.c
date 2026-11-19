/* Application-local DLL fixture with an actual base relocation. */
__declspec(dllexport) int value(void){return 42;}
__declspec(dllexport) int delayed(void){return 42;}
typedef unsigned long long U;
__declspec(dllimport) U GetStdHandle(unsigned);
__declspec(dllimport) int WriteFile(U,const void*,unsigned,unsigned*,void*);
int dllentry(void*base,unsigned reason,void*reserved){
    (void)base;(void)reserved;
    static const char attach[]="M141_DLL_ATTACH\n",detach[]="M141_DLL_DETACH\n";
    unsigned wrote;
    if(reason<=1)WriteFile(GetStdHandle((unsigned)-11),reason?attach:detach,16,&wrote,0);
    return 1;
}
void* volatile relocation_anchor=&value;
