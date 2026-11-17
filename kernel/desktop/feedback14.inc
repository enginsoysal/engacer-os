/* A bounded, dismissible message; no worker, retained surface or idle timer. */
static unsigned feedback_visible14(void){return shell_notice[0]&&!launcher&&!context11&&!switch_open11&&!guide_open11&&!file_dialog_state11.mode&&!tray_open12&&!dragging&&!file_drag11;}
static i11_target feedback_target14(int x,int y){
 if(!feedback_visible14())return(i11_target){0,0,0};
 int width=model.width>512?480:(int)model.width-32,left=(int)model.width-width-16;
 if(x<left||x>=left+width||y<16||y>=132)return(i11_target){0,0,0};
 return(i11_target){0,x>=left+width-108&&x<left+width-12&&y>=24&&y<60?60002:60004,I11_BUTTON};
}
static void feedback_draw14(void){
 if(!feedback_visible14())return;
 int width=model.width>512?480:(int)model.width-32,x=(int)model.width-width-16,y=16;
 ui73_shadow(x,y,width,116);ui73_round(x,y,width,116,10,paper());
 text(x+16,y+12,"Engacer OS",1,ink());button(0,x+width-108,y+8,96,"Dismiss",60002,0);
 ui73_paragraph(x+16,y+56,width-32,2,shell_notice,ink());
}
