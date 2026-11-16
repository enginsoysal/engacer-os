"""Generate original M12.0 concepts, explicitly distinct from native evidence."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/architecture/figures/m12'
INK='#17212f';MUTED='#526173';ACCENT='#087c71';LINE='#ccd4df'
def rect(x,y,w,h,fill='#ffffff',r=8,stroke=None):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'
def text(x,y,label,size=16,color=INK,weight=400):
 return f'<text x="{x}" y="{y}" font-family="Inter,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(label)}</text>'
def line(x,y,xx,yy,color=LINE):return f'<path d="M{x} {y} L{xx} {yy}" stroke="{color}" stroke-width="1.5" fill="none"/>'
def icon(x,y,kind,size=32):
 shapes={
 'folder':'<path d="M3 10V7q0-3 3-3h8l4 5h9q3 0 3 3v14q0 3-3 3H6q-3 0-3-3Z" fill="#dbac49"/><path d="M3 13h27v13q0 3-3 3H6q-3 0-3-3Z" fill="#f2ce78"/>',
 'calculator':'<rect x="5" y="2" width="23" height="29" rx="4" fill="#377fa0"/><path d="M9 6h15v6H9Z" fill="#e4f6fa"/><path d="M9 17h4m5 0h5M9 22h4m5 0h5M9 27h4m5 0h5" stroke="#ffffff" stroke-width="2.5"/>',
 'clock':'<circle cx="16" cy="16" r="14" fill="#5377b5"/><circle cx="16" cy="16" r="10" fill="#ffffff"/><path d="M16 8v9l6 3" stroke="#17212f" stroke-width="2" fill="none"/>',
 'calendar':'<rect x="3" y="5" width="27" height="25" rx="4" fill="#ffffff" stroke="#bf665c"/><path d="M3 11V8q0-3 3-3h21q3 0 3 3v4H3" fill="#bf665c"/><path d="M10 2v6m13-6v6M8 17h4m5 0h4M8 23h4m5 0h4" stroke="#963f35" stroke-width="2"/>',
 'terminal':'<rect x="2" y="4" width="29" height="24" rx="4" fill="#27364a"/><path d="m7 11 5 5-5 5m9 0h8" stroke="#e8edf5" stroke-width="2" fill="none"/>',
 'editor':'<rect x="6" y="2" width="22" height="29" rx="3" fill="#ffffff" stroke="#6993ae"/><path d="M11 9h12m-12 6h12m-12 6h9m-9 5h7" stroke="#6993ae" stroke-width="2"/>',
 'settings':'<path d="M5 8h24M5 16h24M5 24h24" stroke="#087c71" stroke-width="3"/><circle cx="12" cy="8" r="4" fill="#087c71"/><circle cx="22" cy="16" r="4" fill="#087c71"/><circle cx="13" cy="24" r="4" fill="#087c71"/>',
 'usb':'<path d="M12 2h9v9h5v15q0 5-5 5h-9q-5 0-5-5V11h5Z" fill="#7c92a6"/><path d="M15 4v5m4-5v5" stroke="#ffffff" stroke-width="2"/>',
 'archive':'<rect x="3" y="5" width="27" height="24" rx="4" fill="#9c78ad"/><path d="M15 5v24" stroke="#ead8f4" stroke-width="4" stroke-dasharray="3 2"/>',
 'start':'<path d="M3 3h12v12H3Zm15 0h12v12H18ZM3 18h12v12H3Zm15 0h12v12H18Z" fill="#087c71"/>'}
 return f'<g transform="translate({x} {y}) scale({size/32})">'+shapes.get(kind,shapes['folder'])+'</g>'
def button(x,y,w,label,primary=False):
 return rect(x,y,w,36,ACCENT if primary else '#ffffff',6,LINE)+text(x+12,y+24,label,14,'#ffffff' if primary else INK)
def base(title):
 return '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="800" viewBox="0 0 1280 800" role="img"><title>'+escape(title)+'</title>'+rect(0,0,1280,800,'#dce9ec',0)+'<path d="M0 590Q430 210 850 500T1280 280V800H0Z" fill="#c8dde2"/>'+text(30,56,'Engacer OS',24,INK,600)+rect(748,18,510,32,'#ffffff',6)+text(761,39,'M12.0 DESIGN CONCEPT — NOT A VM CAPTURE',14,MUTED,600)
def taskbar():
 s=rect(0,744,1280,56,'#f8fafc',0)+line(0,744,1280,744)
 for i,name in enumerate(('start','folder','editor','terminal','settings')):
  x=28+i*60
  if i==1:s+=rect(x-8,751,48,43,'#e0ebe8',6)+rect(x+4,793,24,3,ACCENT,1)
  s+=icon(x,757,name,28)
 return s+text(1070,769,'Device status',12,MUTED)+text(1190,769,'10:30',14)+text(1155,790,'16 Nov 2026',12,MUTED)
def frame(title='Documents — Files',path='Home  /  Documents',usb=False,empty=False):
 s=rect(126,108,1024,592,'#ffffff',10,LINE)+rect(127,109,1022,42,'#f0f4f7',9)
 s+=icon(143,119,'folder',22)+text(176,136,title,15)+text(1020,135,'—     □     ×',18)
 s+=button(142,164,42,'←')+button(190,164,42,'→')+button(238,164,42,'↑')+rect(292,164,600,36,'#f8fafc',6,LINE)+text(306,188,path,14)+rect(904,164,230,36,'#f8fafc',6,LINE)+text(918,188,'Search this location',14,MUTED)
 action_color='#788797' if empty else INK
 limited_color='#788797' if usb else action_color
 s+=text(148,232,'＋ New',14,limited_color)+text(250,232,'Cut',14,limited_color)+text(312,232,'Copy',14,action_color)+text(385,232,'Paste',14,action_color)+text(462,232,'Rename',14,limited_color)+text(566,232,'View ▾',14)+text(670,232,'Sort ▾',14)+text(1068,232,'⋯',21)
 s+=line(142,248,1134,248)+rect(127,249,207,410,'#f8fafc',0)+line(334,249,334,660)
 for i,label in enumerate(('Home','Desktop','Documents','Downloads','Pictures','This device','USB drives','Recycle Bin')):
  yy=268+i*43
  if i==(6 if usb else 2):s+=rect(135,yy-4,190,36,'#d9efe9',5)
  s+=icon(146,yy+2,'usb' if i==6 else 'folder',20)+text(178,yy+18,label,14)
 return s+line(142,660,1134,660)
def files(empty=False):
 s=frame('USB drives — Files' if empty else 'Work — Files','This device  /  USB drives' if empty else 'USB drive  /  Work',True,empty)
 if empty:
  s+=icon(705,340,'usb',60)+text(605,445,'No USB drive connected',21,INK,600)+text(557,479,'Connect a drive to browse its files.',16,MUTED)+button(685,509,110,'Refresh',True)
  s+=text(354,686,'Back returns to Documents. Navigation stays available.',14,MUTED)
 else:
  s+=text(360,280,'Name',14,MUTED)+text(865,280,'Type',14,MUTED)+text(1052,280,'Size',14,MUTED)
  for i,(label,kind) in enumerate((('Projects','folder'),('Readme.txt','editor'),('Tools.zip','archive'))):
   yy=303+i*54
   if i==1:s+=rect(350,yy-1,784,44,'#d9efe9',4)
   s+=icon(361,yy+6,kind,28)+text(406,yy+27,label)+text(865,yy+27,'Folder' if i==0 else 'File',14,MUTED)+text(1052,yy+27,'—' if i==0 else '2 KiB',14,MUTED)
  s+=text(354,686,'3 items · 1 selected · USB actions follow provider capabilities',14,MUTED)
 return s
def start():
 s=rect(300,124,680,588,'#f8fafc',12,LINE)+rect(328,151,624,40,'#ffffff',6,LINE)+text(347,177,'Search apps and pinned folders',16,MUTED)
 s+=text(333,232,'Pinned',21,INK,600)+button(830,207,122,'All apps  →')
 names=(('folder','Files'),('calculator','Calculator'),('calendar','Calendar'),('clock','Clock'),('editor','Text Editor'),('terminal','Terminal'),('archive','Archives'),('settings','Settings'))
 for i,(kind,label) in enumerate(names):
  x=350+(i%4)*155;y=266+(i//4)*124;s+=icon(x+26,y,kind,48)+text(x+2,y+79,label,14)
 s+=line(326,570,954,570)+text(337,607,'Categories',16,INK,600)+text(337,640,'Accessories    System    Media    Development',14,MUTED)+text(337,687,'Owner',14)+button(824,660,128,'Power  ▾')
 return s
def settings():
 s=rect(126,108,1024,592,'#ffffff',10,LINE)+rect(127,109,1022,42,'#f0f4f7',9)
 s+=icon(143,119,'settings',22)+text(176,136,'Appearance — Settings',15)+text(1020,135,'—     □     ×',18)
 s+=rect(127,151,207,508,'#f8fafc',0)+line(334,151,334,660)
 s+=text(148,192,'Settings',21,INK,600)
 for i,label in enumerate(('System','Devices','Personalization','Apps','Accessibility','Recovery')):
  yy=235+i*46
  if i==2:s+=rect(135,yy-24,190,36,'#d9efe9',5)
  s+=text(148,yy,label,14)
 s+=text(365,199,'Settings  /  Personalization',14,MUTED)+text(365,269,'Make it yours',28,INK,600)
 for i,(name,color) in enumerate((('Light','#f8fafc'),('Dark','#202732'),('High contrast','#000000'))):
  x=365+i*250;s+=rect(x,324,225,130,color,8,LINE)+text(x,481,name,16)
 s+=text(365,534,'Display size',16)+button(365,551,150,'Auto')+button(527,551,150,'150%')+text(365,629,'Reduced motion and solid surfaces remain available.',14,MUTED)
 return s
def transfer():
 s=frame()+rect(474,300,580,257,'#ffffff',10,LINE)+text(500,342,'Copying 3 items to USB drive',21,INK,600)+text(500,379,'Destination: USB drive / Work',16,MUTED)+rect(500,407,528,8,'#e8edf2',4)+rect(500,407,304,8,ACCENT,4)+text(500,445,'Confirmed completed work · keep the drive connected',14,MUTED)+button(898,489,130,'Cancel')
 return s
def setup():
 s=rect(196,118,888,596,'#ffffff',12,LINE)+rect(196,118,220,596,'#203544',12)+text(220,165,'Engacer OS',24,'#ffffff',600)
 for i,label in enumerate(('Welcome','Keyboard / size','Choose a disk','Your apps','Your style','Review','Installing','Ready')):
  if i==2:s+=rect(208,267,196,38,'#365765',6)
  s+=text(221,218+i*41,f'{i+1}  {label}',14,'#e8edf5')
 s+=text(451,164,'STEP 3 OF 8',14,MUTED)+text(451,222,'Choose an installation disk',28,INK,600)+text(451,257,'Select a row. Review all changes before installation.',14,MUTED)
 s+=rect(451,291,596,210,'#f8fafc',7,LINE)+rect(460,332,578,66,'#d9efe9',5,ACCENT)+text(477,359,'●   Disk 1',16)+text(522,383,'Supported writable disk · 20 GiB',14,MUTED)
 s+=button(451,523,140,'Disk tools…')+text(451,608,'Erasure always requires a separate explicit review.',14,MUTED)+button(451,653,106,'Back')+button(917,653,130,'Next',True)
 return s
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 for name,body in [('overview',start()),('files-usb',files()),('usb-empty',files(True)),('settings',settings()),('transfer',transfer()),('setup',setup())]:
  svg=base('Engacer OS M12.0 '+name+' — design only')+body+taskbar()+'</svg>'
  (OUT/(name+'.svg')).write_bytes(svg.encode())
 print('Generated six original, explicitly labelled M12.0 SVG concepts.')
if __name__=='__main__':main()
