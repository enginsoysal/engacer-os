/* A bounded, dismissible message; no worker, retained surface or idle timer. */
static unsigned feedback_visible14(void){return shell_notice[0]&&!launcher&&!context11&&!switch_open11&&!guide_open11&&!file_dialog_state11.mode&&!tray_open12&&!dragging&&!file_drag11;}
/* Try each side above intersecting captions; at most eight upward steps. */
static desktop_rect feedback_bounds18(void){
 int width=model.width>512?480:(int)model.width-32,bottom=(int)model.height-60-132;
 for(unsigned side=0;side<2;++side){int x=side?16:(int)model.width-width-16,y=bottom;
  for(unsigned step=0;step<=DESKTOP_WINDOWS&&y>=8;++step){int next=y;
   for(unsigned i=0;i<DESKTOP_WINDOWS;++i){desktop_window*w=&model.windows[i];if(!w->live||w->minimized)continue;desktop_rect r=w->bounds;
    if(x<r.x+r.width&&x+width>r.x&&y<r.y+40&&y+116>r.y&&r.y-124<next)next=r.y-124;
   }if(next==y)return(desktop_rect){x,y,width,116};y=next;
  }
 }
 /* Crowded arrangements still preserve the focused caption and Dismiss. */
 int x=(int)model.width-width-16,y=bottom;if(model.focused<DESKTOP_WINDOWS){desktop_window*w=&model.windows[model.focused];desktop_rect r=w->bounds;if(w->live&&!w->minimized&&x<r.x+r.width&&x+width>r.x&&y<r.y+40&&y+116>r.y)y=r.y>=132?r.y-124:r.y+48;}
 return(desktop_rect){x,y,width,116};
}
static i11_target feedback_target14(int x,int y){
 if(!feedback_visible14())return(i11_target){0,0,0};
 desktop_rect r=feedback_bounds18();int width=r.width,left=r.x;
 if(x<left||x>=left+width||y<r.y||y>=r.y+r.height)return(i11_target){0,0,0};
 return(i11_target){0,x>=left+width-108&&x<left+width-12&&y>=r.y+8&&y<r.y+44?60002:60004,I11_BUTTON};
}
static void feedback_draw14(void){
 if(!feedback_visible14())return;
 desktop_rect r=feedback_bounds18();int width=r.width,x=r.x,y=r.y;
 desktop_shadow16(x,y,width,116);if(access_flags16&1){ui73_round(x,y,width,116,10,ink());ui73_round(x+2,y+2,width-4,112,8,paper());}else ui73_round(x,y,width,116,10,paper());
 text(x+16,y+12,"Engacer OS",1,ink());button(0,x+width-108,y+8,96,"Dismiss",60002,0);
 ui73_paragraph(x+16,y+56,width-32,2,shell_notice,ink());
}
