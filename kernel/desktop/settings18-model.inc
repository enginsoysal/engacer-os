/* Preflight physical dimensions before the renderer mutates its active scale. */
static unsigned settings_scale_fits18(unsigned choice){
 unsigned width=ui73_width(),height=ui73_height();unsigned units=choice?choice:width>=3840&&height>=2000?4:width>=2560&&height>=1400?3:2;
 return units>=2&&units<=4&&width*2/units>=800&&height*2/units>=660;
}
static void settings_restore_scale18(void){
 if(settings_scale_fits18(ui73_scale_choice())||!settings_scale_fits18(0))return;
 const os_boot_info_v0*changed=ui73_set_scale(0);if(!changed)return;display=changed;model.width=changed->framebuffer_width;model.height=changed->framebuffer_height;
 /* Reuse the existing warning reason: 1 unreadable record, 2 safe scale fallback. */
 if(!settings_invalid13)settings_invalid13=2;
}
static const char*settings_names18[]={"Appearance","Display","Mouse and keyboard","System","Accessibility"};
static const char*settings_details18[]={"Accent, light or dark, wallpaper and restore defaults","Display size, scale, automatic scaling, 100%, 150% and 200%","Double-click speed and keyboard layout","Devices, apps, applications, Start, taskbar and quick settings","High contrast, reduced motion and keyboard navigation"};
static const char*settings_keywords18[]={"color colour theme dark mode light mode background reset restore defaults","scale scaling display size zoom text size automatic","mouse keyboard typing double click double-click speed input layout dvorak qwerty","devices hardware network status sound audio volume apps applications software installed start menu taskbar quick settings","accessibility high contrast reduced motion keyboard navigation"};
static settings_search_record18*settings_query18(uint64_t token){
 desktop_window*w=desktop_lookup(&model,token);if(!w||w->app!=SETTINGS)return 0;
 settings_search_record18*q=&settings_search18[w-model.windows];if(q->owner!=token){memset(q,0,sizeof(*q));q->owner=token;}return q;
}
static unsigned settings_match18(unsigned page,const char*query){
 const char*texts[]={settings_names18[page],settings_details18[page],settings_keywords18[page]};unsigned wanted=length(query);
 for(unsigned t=0;t<3;++t)for(unsigned at=0;texts[t][at];++at){unsigned i=0;while(i<wanted&&texts[t][at+i]&&lower11((uint8_t)texts[t][at+i])==lower11((uint8_t)query[i]))++i;if(i==wanted)return 1;}return !wanted;
}
static void settings_search_clear18(uint64_t token){settings_search_record18*q=settings_query18(token);if(q){q->query[0]=0;q->cursor=q->anchor=q->active=0;}control_active=0;}
static unsigned settings_search_action18(uint64_t token,unsigned command){
 settings_search_record18*q=settings_query18(token);if(!q)return 0;
 if(command==S18_SEARCH){q->active=control_active=1;focused_control_window=token;focused_action=S18_SEARCH;whole();return 1;}
 if(command==S18_CLEAR){settings_search_clear18(token);whole();return 1;}
 if(command>=S18_RESULT&&command<S18_RESULT+5){unsigned page=command-S18_RESULT;if(!q->query[0]||!settings_match18(page,q->query))return 1;settings_search_clear18(token);settings_action13(token,S13_APPEARANCE+page);return 1;}return 0;
}
static void settings_search_draw18(desktop_window*w,uint64_t token,int x,int y,int width){
 settings_search_record18*q=settings_query18(token);ui12_palette p=desktop_palette16();desktop_rect field={x,y,width-128,40};unsigned focused=q->active&&control_active&&focused_control_window==token&&focused_action==S18_SEARCH;
 file_text_field11(field,q->query,q->cursor,q->anchor,focused,0);if(!q->query[0])ui73_fit(x+12,y+10,width-152,"Find a setting (Ctrl+F)",UI12_BODY,p.muted);
 access_capture16(token,S18_SEARCH,"Find a supported setting",2);file_control11(token,field,S18_SEARCH);settings_button13(token,x+width-120,y+2,120,"Clear search",S18_CLEAR,0,q->query[0]!=0);(void)w;
}
static void settings_search_results18(uint64_t token,int x,int top,int width){
 settings_search_record18*q=settings_query18(token);ui12_palette p=desktop_palette16();unsigned row=0;
 for(unsigned page=0;page<5;++page)if(settings_match18(page,q->query)){
  int y=top+(int)row*52;unsigned command=S18_RESULT+page,state=component_state12(token,command);ui12_style style=ui12_control_style(p,state,0);unsigned inset=(state&UI12_FOCUS)?3:1;
  ui73_round(x,y,width,48,6,style.border);ui73_round(x+inset,y+inset,width-2*inset,48-2*inset,6-inset,style.fill);
  ui73_fit(x+12,y+4,width-24,settings_names18[page],UI12_BODY,style.ink);ui73_fit(x+12,y+27,width-24,settings_details18[page],UI12_SECONDARY,p.muted);
  access_capture16(token,command,settings_names18[page],1);file_control11(token,(desktop_rect){x,y,width,48},command);++row;
 }
 if(!row){ui73_fit(x,top,width,"No supported settings match.",UI12_SECTION,p.ink);ui73_paragraph(x,top+40,width,3,"Try a shorter word such as dark, scale, keyboard, applications or contrast. Clear search to browse all categories. Your current choices are unchanged.",p.muted);}
 else ui73_fit(x,top+(int)row*52,width,"Choose a category to see its supported controls.",UI12_SECONDARY,p.muted);
}
static unsigned settings_search_key18(int key){
 if(launcher||context11||switch_open11||guide_open11||file_dialog_state11.mode||model.focused>=DESKTOP_WINDOWS)return 0;desktop_window*w=&model.windows[model.focused];if(!w->live||w->minimized||w->app!=SETTINGS)return 0;uint64_t token=desktop_token(&model,model.focused);settings_search_record18*q=settings_query18(token);
 if(key==6){apps[model.focused].hardware_view10=apps[model.focused].offset=0;settings_search_action18(token,S18_SEARCH);return 1;}
 if(!q->active||!control_active||focused_control_window!=token||focused_action!=S18_SEARCH||(input11_modifiers()&4))return 0;
 if(key==9||key==136){q->active=0;return 0;}
 if(key==27){if(q->query[0]){q->query[0]=0;q->cursor=q->anchor=0;}else{q->active=0;control_active=0;}whole();return 1;}
 if(key==10){if(q->query[0])for(unsigned page=0;page<5;++page)if(settings_match18(page,q->query)){settings_search_action18(token,S18_RESULT+page);return 1;}return 1;}
 if(file_text_capacity11(q->query,sizeof(q->query),&q->cursor,&q->anchor,key)){whole();return 1;}return 0;
}
