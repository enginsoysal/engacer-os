/* Optional first-start card. Only base Files/Settings and shell Start are used. */
static void guide_path11(char *path){copy(path,"/System/Settings/firstboot11-",256);append(path,owner.user,256);append(path,".bin",256);}
static void guide_load11(void){unsigned saved[3],bytes=0;char path[256];guide_path11(path);
 guide_open11=owner.guide&&!v6_verify(m6_volume(),path)&&!v6_read(m6_volume(),path,0,saved,sizeof(saved),&bytes)&&bytes==sizeof(saved)&&saved[0]==0x47313145&&saved[1]==1&&saved[2]==0;
 if(guide_open11){control_active=1;focused_control_window=0;focused_action=46000;serial_text("M115_FIRST_START_GUIDE\n");}
}
static void guide_action11(unsigned command){if(!guide_open11||command<46000||command>46003)return;unsigned saved[3]={0x47313145,1,1};char path[256];guide_path11(path);
 if(v6_put(m6_volume(),path,sizeof(saved),memory_source,saved)||v6_verify(m6_volume(),path))copy(shell_notice,"Guide closed for this session. Saving failed; it may return after restart.",sizeof(shell_notice));
 guide_open11=0;control_active=0;i11_cancel(&interaction11);
 if(command==46001){unsigned found=0;for(unsigned i=0;i<model.count;++i){unsigned slot=model.order[i];if(model.windows[slot].app==FILES){uint64_t token=desktop_token(&model,slot);desktop_minimize(&model,token,0);desktop_focus(&model,token);found=1;break;}}if(!found)launch(FILES,0);}
 else if(command==46002)start_open11();else if(command==46003)launch(SETTINGS,0);whole();serial_text("M115_GUIDE_DISMISSED\n");
}
static unsigned guide_key11(int key){if(!guide_open11||launcher||context11||file_dialog_state11.mode||!control_active||focused_control_window||focused_action<46000||focused_action>46003)return 0;
 if(key==27){guide_action11(46000);return 1;}if(key==10||key==32){guide_action11(focused_action);return 1;}
 if(key==9||key==136){focused_action=46000+(focused_action-46000+(key==9?1:3))%4;whole();return 1;}return 0;
}
static void guide_draw11(void){if(!guide_open11)return;
#ifdef ENGINE_M12
 int w=680,h=400,x=((int)model.width-w)/2,y=((int)model.height-60-h)/2;guide_bounds11=(desktop_rect){x,y,w,h};ui12_palette p=ui12_theme(preferences.dark,preferences.accent);ui73_shadow(x,y,w,h);ui73_round(x,y,w,h,12,p.paper);ui73_fit(x+28,y+26,w-56,"Welcome to Engacer OS",UI12_HEADING,p.ink);
 ui73_paragraph(x+28,y+82,w-56,2,"Your installed desktop is ready. Click a file once to select it; double-click or press Enter to open. Right-click for its actions.",p.ink);
 ui73_paragraph(x+28,y+148,w-56,2,"Start finds apps and pinned folders. Files keeps Back, Up and Places visible, including USB. No terminal command is needed.",p.muted);
 ui73_paragraph(x+28,y+214,w-56,2,"Preview your appearance in Settings. Apply and save keeps it; Cancel preview restores it. Optional apps stay independent of your files.",p.muted);
 button(0,x+28,y+288,200,"Explore Files",46001,0);button(0,x+240,y+288,200,"Open Start",46002,0);button(0,x+452,y+288,200,"Appearance",46003,0);button(0,x+432,y+344,220,"Go to my desktop",46000,1);
#else
int w=600,h=350,x=((int)model.width-w)/2,y=((int)model.height-60-h)/2;guide_bounds11=(desktop_rect){x,y,w,h};
 ui73_shadow(x,y,w,h);ui73_round(x,y,w,h,14,0xf8fafb);ui73_fit(x+28,y+26,w-56,"Welcome home",4,0x193746);
 ui73_paragraph(x+28,y+84,w-56,2,"Your installed desktop is ready. Click a file once to select it; double-click to open. Right-click for more choices.",0x506976);
 ui73_paragraph(x+28,y+166,w-56,2,"Start finds your apps. Files opens your folders. Settings changes the look and feel. You can explore at your own pace.",0x506976);
 button(0,x+28,y+254,166,"Explore Files",46001,0);button(0,x+204,y+254,166,"Open Start",46002,0);button(0,x+380,y+254,190,"Appearance",46003,0);
 button(0,x+350,y+304,220,"Go to my desktop",46000,1);
#endif
}
