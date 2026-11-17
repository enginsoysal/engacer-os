"""Generate original, explicitly design-only M13 SVG concepts. No native claim."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/architecture/figures/m13'
INK='#192838';MUTED='#556777';TEAL='#087e78';LINE='#d7e0e8'

def rect(x,y,w,h,fill='white',r=10,stroke='none'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
def text(x,y,s,size=16,fill=INK,weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}">{escape(s)}</text>'
def button(x,y,w,label,primary=False):
    return rect(x,y,w,44,TEAL if primary else 'white',8,TEAL if primary else LINE)+text(x+18,y+28,label,16,'white' if primary else INK,600)
def base(title):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="960" viewBox="0 0 1440 960" role="img" aria-label="'+escape(title)+'"><style>text{font-family:Inter,Arial,sans-serif}</style>'+rect(0,0,1440,960,'#eaf0f6',0)+text(36,38,'ENGACER OS / M13.0 ORIGINAL DESIGN CONCEPT',14,TEAL,700)+text(36,68,title,22,INK,600)+text(36,935,'DESIGN ONLY · Proposed layout and sample content · Not a native OS screenshot',14,MUTED)
def frame(title):
    return rect(80,110,1280,760,'white',16,LINE)+rect(80,110,1280,54,'#f7f9fc',16)+text(104,144,'E  '+title,18,INK,600)+text(1230,144,'—    □    ×',20)
def setup(disks=False):
    s=base('Choose where it belongs' if disks else 'A clear beginning')+frame('Engacer OS Setup')
    s+=rect(80,164,256,706,'#eef4f7',0)
    for i,label in enumerate(['Welcome','Keyboard & display','Choose a disk','Your preferences','Review','Install']):
        y=218+i*62
        if i==(2 if disks else 0):s+=rect(96,y-27,224,46,'#d9eeeb',8)
        s+=text(116,y,f'{i+1}  {label}',16,TEAL if i==(2 if disks else 0) else MUTED,600)
    if disks:
        s+=text(384,232,'Where would you like to install?',30,INK,600)+text(384,266,'Choose a disk. Nothing changes until you confirm Install.',16,MUTED)
        s+=rect(384,308,920,76,'#e0f2ed',10,TEAL)+text(410,340,'●  Virtual hard disk',18,INK,600)+text(435,366,'20 GB · Available for installation',15,MUTED)+text(1200,350,'20 GB',18)
        s+=text(384,430,'Installation method',20,INK,600)+rect(384,454,920,100,'#f6f9fc',10,LINE)+text(408,485,'●  Use this entire disk',18,INK,600)+text(434,518,'Creates the required partitions. Existing data on this disk will be erased.',16,MUTED)
        s+=button(384,580,204,'Advanced disk tools')+text(384,662,'You will review the exact disk and erase warning before installation.',16,MUTED)
    else:
        s+=text(384,252,'Make yourself at home.',36,INK,600)+text(384,300,'A familiar desktop. Your choices. A clean start.',19,MUTED)
        for i,(title,detail) in enumerate([('Simple to begin','Recommended settings are ready for you.'),('Make it yours','Change the look now, or later in Settings.'),('You stay in control','Review your disk before anything is erased.')]):
            y=380+i*102;s+=rect(384,y-28,48,48,'#d9eeeb',12)+text(400,y+3,'✓',22,TEAL,600)+text(452,y,title,20,INK,600)+text(452,y+30,detail,16,MUTED)
    s+=rect(336,778,1024,92,'#f7f9fc',0)+button(376,802,120,'Back')+text(530,830,'Step '+('3' if disks else '1')+' of 6',15,MUTED)+button(1168,802,144,'Next →',True)
    return s+'</svg>'
def desktop(kind='desktop'):
    title={'desktop':'Files, with room for your files','start':'Your apps, one familiar place','settings':'Clear choices, safe previews'}[kind]
    s=base(title)+rect(40,100,1360,792,'#163745',18)
    s+='<path d="M40 640 Q430 140 920 480 T1400 250 V892 H40Z" fill="#206073" opacity=".6"/><path d="M40 730 Q600 330 1400 650 V892 H40Z" fill="#287a85" opacity=".5"/>'
    for i,label in enumerate(['My files','Documents','Recycle Bin']):
        y=148+i*118;s+=rect(82,y,42,35,'#f2cf7a',6)+text(66,y+62,label,15,'white')
    if kind=='desktop':
        s+=rect(236,176,1100,620,'white',12,LINE)+rect(236,176,1100,42,'#f4f7fa',12)+text(256,204,'▰  Documents — Files',17,INK,600)+text(1216,204,'—   □   ×',18)
        s+=text(258,254,'‹     ›     ↑',24,MUTED)+rect(386,230,734,38,'#f3f6fa',7)+text(402,255,'Home   /   Documents',16)+text(1150,254,'Search this folder',14,MUTED)
        s+=text(258,304,'New folder     Copy     Paste     Rename     Delete',15)+text(1132,304,'View ▾   Sort ▾',15)
        s+=rect(236,324,208,430,'#f6f9fc',0)
        for i,label in enumerate(['Home','Desktop','Documents','Downloads','System drive','USB drives']):
            y=362+i*48
            if i==2:s+=rect(248,y-26,184,38,'#d9eeeb',7)
            s+=text(264,y,label,16,TEAL if i==2 else MUTED)
        s+=text(472,357,'Name',14,MUTED)+text(1060,357,'Type',14,MUTED)+text(1210,357,'Size',14,MUTED)
        for i,label in enumerate(['Projects','Pictures','Notes.txt','Welcome.pdf']):
            y=402+i*54
            if i==0:s+=rect(458,y-28,852,44,'#e3f1ee',6)
            s+=rect(474,y-19,24,20,'#f2cf7a' if i<2 else '#d6e6f3',3)+text(514,y,label,16)+text(1060,y,'Folder' if i<2 else 'Document',15,MUTED)+text(1210,y,'—' if i<2 else 'Sample',14,MUTED)
        s+=text(258,780,'4 items · 1 selected',14,MUTED)
    elif kind=='start':
        s+=rect(272,208,640,610,'#f8fafc',16,LINE)+rect(302,238,580,44,'white',8,LINE)+text(320,266,'Search apps and settings',16,MUTED)
        s+=text(304,328,'Pinned',18,INK,600)+button(752,300,130,'All apps →')
        for i,label in enumerate(['Files','Settings','Terminal','Calculator','Text Editor','Clock','Calendar','Archives']):
            x=346+(i%4)*144;y=386+(i//4)*120;s+=rect(x,y,46,46,['#e7bb62',TEAL,'#284361','#5279b1'][i%4],12)+text(x+12,y+30,['▰','⚙','>_','＋'][i%4],21,'white',600)+text(x-10,y+73,label,15)
        s+=rect(272,738,640,80,'#edf2f7',0)+text(304,786,'●  Local user',16)+text(790,786,'Power ⏻',16)
    else:
        s+=rect(236,176,1100,620,'white',12,LINE)+text(264,212,'Settings',20,INK,600)+text(1216,212,'—   □   ×',18)+rect(256,240,222,40,'#f3f6fa',8)+text(270,266,'Search settings',15,MUTED)
        for i,label in enumerate(['Appearance','Display','Devices','Apps','About']):
            y=330+i*58
            if i==0:s+=rect(252,y-27,230,42,'#d9eeeb',8)
            s+=text(274,y,label,16,TEAL if i==0 else MUTED)
        s+=text(528,282,'Appearance',30,INK,600)+text(528,320,'Make this desktop feel like yours.',17,MUTED)
        for i,(a,b) in enumerate([('Theme','Light   /   Dark   /   High contrast'),('Accent color','Teal'),('Taskbar alignment','Left   /   Center'),('Density','Comfortable   /   Compact')]):
            y=374+i*77;s+=rect(516,y-30,786,62,'#f6f9fc',8)+text(538,y,a,17,INK,600)+text(886,y,b,15,MUTED)
        s+=text(528,712,'Preview changes before saving. You can always restore defaults.',15,MUTED)+button(528,736,150,'Restore defaults')+button(1000,736,130,'Cancel')+button(1148,736,150,'Apply',True)
    s+=rect(40,836,1360,56,'#102a37',0)+button(58,842,108,'E  Start',True)
    for i,label in enumerate(['▰  Files','>_  Terminal','⚙  Settings']):s+=text(200+i*160,871,label,16,'#edf6fb')
    s+=text(1230,862,'12:00',15,'white')+text(1200,882,'Design sample',12,'#bbd1dc')
    return s+'</svg>'
def portal():
    s=base('Documentation that starts with your task')+frame('Engacer OS · Documentation')+rect(80,164,1280,70,'#102a37',0)+text(108,208,'E_ ENGACER OS',20,'white',700)+button(1180,178,146,'Search  Ctrl+K')
    for x,label in [(600,'Start here'),(706,'Install'),(782,'Use'),(840,'Customize'),(962,'Downloads')]:s+=text(x,207,label,17,'white')
    s+=rect(80,234,244,636,'#f3f6fa',0)
    for i,label in enumerate(['Start here','Install','Use Engacer OS','Customize','Project & development','Archive']):
        y=292+i*55
        if i==0:s+=rect(96,y-27,210,42,'#d9eeeb',8)
        s+=text(110,y,label,16,TEAL if i==0 else MUTED)
    s+=text(370,290,'Documentation / Start here',14,MUTED)+text(370,346,'What would you like to do?',32,INK,600)+text(370,384,'Current release: M12.18 · Design program: M13.0',16,MUTED)
    for i,(a,b) in enumerate([('Install Engacer OS','Download, choose a disk, install and restart.'),('Use your desktop','Apps, windows, folders and USB drives.'),('Make it yours','Appearance, preferences and your own distro.')]):
        y=432+i*112;s+=rect(370,y,920,92,'#f6f9fc',10,LINE)+text(396,y+34,a,20,INK,600)+text(396,y+65,b,16,MUTED)+text(1240,y+52,'→',24,TEAL)
    s+=text(370,810,'Historical milestones are available separately in the ordered archive.',16,MUTED)
    return s+'</svg>'

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    designs={'setup':setup(),'disks':setup(True),'desktop':desktop(),'start':desktop('start'),'settings':desktop('settings'),'portal':portal()}
    for name,data in designs.items():(OUT/(name+'.svg')).write_text(data,encoding='utf-8')
    print('Generated six original design-only SVGs')
if __name__=='__main__':main()
