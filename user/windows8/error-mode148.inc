/* Process-wide policy in the shared startup page, inherited explicitly by the
 * child broker. AMD64 does not enable an alignment-fixup emulation mode. */
static unsigned MS f_GetErrorMode(void){return __atomic_load_n(&job8->error_mode148,__ATOMIC_ACQUIRE);}
static unsigned MS f_SetErrorMode(unsigned mode){if(mode&~0x8007u)fail8("This Windows error-mode bit is not supported.");return __atomic_exchange_n(&job8->error_mode148,mode&~4u,__ATOMIC_ACQ_REL);}
