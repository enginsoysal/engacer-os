/* Independent accessibility choices; the appearance ABI remains unchanged. */
enum {ACCESS_CONTRAST16=60010,ACCESS_MOTION16,ACCESS_DEFAULTS16,ACCESS_HELP_CLOSE16=60020,ACCESS_HELP_BODY16};
static unsigned access_flags16,access_invalid16,access_region16,access_help16;
typedef struct {uint64_t owner;unsigned action,role;char label[80];} access_semantic16;
static access_semantic16 access_focus16,access_help_item16;
static void action(uint64_t,unsigned);
static void open_target11(i11_target);
static void desktop_select11(unsigned,unsigned,unsigned);
static void access_load16(void);
static unsigned access_action16(uint64_t,unsigned);
static unsigned access_key16(int);
static void access_draw16(void);
static i11_target access_target16(int,int);
static ui12_palette desktop_palette16(void){return ui12_theme((access_flags16&1)?2:preferences.dark,preferences.accent);}
static void access_capture16(uint64_t owner_id,unsigned command,const char*name,unsigned role){
 if(!control_active||focused_control_window!=owner_id||focused_action!=command)return;
 access_focus16.owner=owner_id;access_focus16.action=command;access_focus16.role=(command==ACCESS_CONTRAST16||command==ACCESS_MOTION16)?4:(command==S11_SEARCH||command==40026||command==54018||command==54019)?2:role;
 unsigned n=0;while(name[n]&&n<sizeof(access_focus16.label)-1){access_focus16.label[n]=name[n];++n;}access_focus16.label[n]=0;
}
_Static_assert(sizeof(access_focus16)+sizeof(access_help_item16)+sizeof(access_flags16)+sizeof(access_invalid16)+sizeof(access_region16)+sizeof(access_help16)<=224,"bounded accessibility state");
