/* One bounded app group per pin/running identity; never a per-window surface. */
#include <engine/ui/taskbar12.h>
_Static_assert(T12_APPS==S11_APPS,"taskbar/catalogue identity bound");
static char taskbar_labels12[DESKTOP_WINDOWS][96];
static unsigned taskbar_overflow_page12;
_Static_assert(sizeof(taskbar_labels12)+sizeof(taskbar_overflow_page12)<1024,"bounded shared taskbar menu state");
static unsigned taskbar_apps12(unsigned *list){
 unsigned count=0;
 for(unsigned i=0;i<start_preferences11.tasks;++i){unsigned app=start_preferences11.task[i];if(app7_available(app))taskbar12_add(list,&count,app);}
 for(unsigned i=0;i<model.count;++i)taskbar12_add(list,&count,model.windows[model.order[i]].app);
 return count;
}
static unsigned taskbar_windows12(unsigned app,unsigned *shown,uint64_t *window){
 unsigned count=0;if(shown)*shown=0;if(window)*window=0;
 for(unsigned i=0;i<model.count;++i){unsigned slot=model.order[i];desktop_window*w=&model.windows[slot];if(w->app!=app)continue;++count;if(shown&&!w->minimized)*shown=1;if(window)*window=desktop_token(&model,slot);}
 return count;
}
static void taskbar_choose12(unsigned app){
 start_menu_begin11(0,pointer_x,pointer_y);
 for(unsigned i=0;i<model.count;++i){unsigned slot=model.order[i];desktop_window*w=&model.windows[slot];if(w->app!=app)continue;
  char number[24];decimal(number,slot+1);char*label=taskbar_labels12[slot];copy(label,number,96);append(label,". ",96);if(w->minimized)append(label,"[min] ",96);if(w->app==EDITOR&&apps[slot].view.dirty)append(label,"[unsaved] ",96);
  const char*path=apps[slot].path;append(label,(w->app==FILES||w->app==EDITOR)&&path[0]?file_basename11(path):titles[app],96);
  start_window_menu11[slot]=desktop_token(&model,slot);file_menu_add11(label,S11_WINDOW+slot,1);
 }
 file_menu_add11("Open new window",S11_APP+app,app7_available(app));copy(file_menu_reason11,"Choose a window. Its number identifies this live window slot.",128);file_menu_fit11();
}
static void taskbar_more12(unsigned reset){
 unsigned list[T12_APPS],count=taskbar_apps12(list),visible=taskbar12_visible(model.width,count),hidden=count-visible;
 if(!hidden){context11=0;copy(shell_notice,"All pinned and running apps are already visible on the taskbar.",96);whole();return;}
 if(reset)taskbar_overflow_page12=0;unsigned size=hidden<=12?12:10;
 if(taskbar_overflow_page12*size>=hidden)taskbar_overflow_page12=0;
 unsigned first=visible+taskbar_overflow_page12*size;start_menu_begin11(0,pointer_x,pointer_y);
 for(unsigned i=first;i<count&&i<first+size;++i)file_menu_add11(titles[list[i]],S11_TASK_OPEN+list[i],1);
 if(taskbar_overflow_page12)file_menu_add11("Previous apps",S11_TASK_PREV,1);
 if(first+size<count)file_menu_add11("Next apps",S11_TASK_NEXT,1);
 copy(file_menu_reason11,"Pinned and running apps. Select an app to open or choose its windows.",128);file_menu_fit11();
}
static void taskbar_draw12(int bar){
 unsigned list[T12_APPS],count=taskbar_apps12(list),visible=taskbar12_visible(model.width,count),more=visible<count;
 int clock=model.width>=1000?180:0,total=112+(int)visible*140+(more?108:0),x=start_preferences11.centered?((int)model.width-clock-total)/2:16;if(x<16)x=16;
 icon_button12(0,x,bar+15,100,"Start",0,launcher,ICON12_START);x+=112;
 for(unsigned i=0;i<visible;++i){unsigned app=list[i],shown=0,windows=taskbar_windows12(app,&shown,0);desktop_window*focused=model.focused<DESKTOP_WINDOWS?&model.windows[model.focused]:0;
  unsigned active=model.count&&focused&&focused->app==app&&!focused->minimized&&!desktop_focus11&&!launcher;
  button(0,x,bar+15,132,"",S11_TASK_OPEN+app,active);unsigned state=component_state12(0,S11_TASK_OPEN+app);ui12_style style=ui12_control_style(ui12_theme(preferences.dark,preferences.accent),state,active);
  ui12_icon(app,x+10,bar+21+!!(state&UI12_PRESSED),24,preferences.dark);ui73_fit(x+42,bar+23+!!(state&UI12_PRESSED),windows>1?58:82,titles[app],1,style.ink);
  if(windows>1){char number[24];decimal(number,windows);ui73_round(x+105,bar+23,20,21,5,preferences.dark?0x334954:0xe0e8ec);ui73_fit(x+111,bar+26,14,number,5,ink());}
  if(windows){int length=active?72:shown?28:8;rectangle((desktop_rect){x+(132-length)/2,bar+54,length,3},active?preferences.accent:0xb6cbd1);if(!shown)rectangle((desktop_rect){x+74,bar+54,8,3},0xb6cbd1);}
  x+=140;
 }
 if(more)button(0,x,bar+15,100,"More apps",S11_MORE_PINS,0);if(clock)task_clock74(bar);
}
