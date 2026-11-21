/* Native process entry; the reusable installer itself is loaded lazily. */
__declspec(dllimport) unsigned EngacerMsiRun147(void);
__declspec(dllimport) void ExitProcess(unsigned);
void entry(void);void *volatile anchor147=&entry;
void entry(void){unsigned status=EngacerMsiRun147();ExitProcess(status);}
