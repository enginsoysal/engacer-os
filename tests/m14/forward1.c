/* Keep a relocatable forwarding-only DLL without exporting leaf functions. */
static void anchor(void){}
void* volatile relocation_anchor=&anchor;
