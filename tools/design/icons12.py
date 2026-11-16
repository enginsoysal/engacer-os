"""Original MIT Engacer icon geometry; generate shared native data and SVG review."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ICONS = []
def r(x,y,w,h,radius=0,color=8): return (0,x,y,w,h,radius,color)
def l(x,y,x2,y2,width=2,color=8): return (1,x,y,x2,y2,width,color)
def add(name, shapes): ICONS.append((name,shapes))
def tile(color, shapes): return [r(1,1,30,30,7,color),*shapes]
def page(shapes): return [r(5,2,23,28,3,6),r(7,4,19,24,2,7),*shapes]
folder=[r(1,5,13,9,3,9),r(1,10,30,19,4,9),r(2,11,28,17,3,10),r(3,12,26,2,1,12)]
doc=[r(10,10,12,2,1,6),r(10,15,12,2,1,6),r(10,20,8,2,1,6)]
image=[r(7,7,18,18,2,8),r(9,9,14,14,1,1),r(18,11,3,3,2,12),l(10,21,15,15,2,8),l(15,15,22,22,2,8)]
archive=[r(5,6,22,22,3,4),r(4,4,24,6,2,12),*[r(15,10+i*3,3,2,0,8) for i in range(5)],r(14,23,5,4,1,8)]
add('unknown',page([r(10+i*5,15,3,3,2,6) for i in range(3)]))
add('files',folder)
add('editor',page([*doc,l(13,25,25,13,3,4),l(25,13,27,15,3,9)]))
add('settings',tile(2,[*[l(7,9+i*7,25,9+i*7,2) for i in range(3)],r(10,6,4,6,2),r(19,13,4,6,2),r(12,20,4,6,2)]))
add('calculator',tile(1,[r(7,6,18,6,2),*[r(7+x*7,15+y*5,4,3,1) for y in range(3) for x in range(3)]]))
add('downloads',tile(2,[l(16,6,16,21,3),l(10,15,16,21,3),l(22,15,16,21,3),l(7,25,25,25,3)]))
add('monitor',tile(3,[r(5,7,22,16,2),r(7,9,18,12,1,3),l(9,18,13,13,2),l(13,13,17,17,2),l(17,17,23,11,2),r(14,23,4,3),r(10,26,12,2,1)]))
add('terminal',tile(13,[l(7,10,13,16,2),l(13,16,7,22,2),l(16,23,24,23,2)]))
add('clock',tile(1,[r(5,5,22,22,11),r(7,7,18,18,9,1),l(16,10,16,16,2),l(16,16,21,19,2)]))
add('calendar',tile(5,[r(5,7,22,21,3),r(5,7,22,6,2,12),l(10,4,10,9,2,13),l(22,4,22,9,2,13),*[r(9+x*6,16+y*5,3,3,1,5) for y in range(2) for x in range(3)]]))
add('disks',tile(13,[r(5,6,22,20,3),r(7,8,18,10,2,13),l(8,22,19,22,2,13),r(23,21,2,2,1,2)]))
add('software',tile(3,[r(6,6,8,8,2),r(18,6,8,8,2),r(6,18,8,8,2),l(22,18,22,26,2),l(18,22,26,22,2)]))
add('recovery',tile(2,[l(9,10,23,10,3),l(23,10,23,22,3),l(23,22,9,22,3),l(9,22,9,16,3),l(5,13,9,9,3),l(9,9,13,13,3)]))
add('archives',archive)
add('images',tile(3,image))
add('screenshot',tile(2,[r(6,9,20,16,3),r(8,11,16,12,2,2),r(12,6,8,4,1),r(12,13,8,8,4),r(14,15,4,4,2,2)]))
add('media',tile(5,[l(12,8,24,16,3),l(24,16,12,24,3),l(12,24,12,8,3)]))
add('browser',tile(1,[r(4,4,24,24,12),r(6,6,20,20,10,1),r(11,5,10,22,5),r(13,7,6,18,3,1),l(5,16,27,16,2)]))
add('help',tile(3,[r(8,6,16,11,5),r(11,9,10,6,3,3),r(15,14,5,7,2),r(15,24,4,3,2)]))
add('windows_apps',tile(1,[r(5,6,16,16,2),r(7,10,12,10,1,1),r(12,13,15,14,2,12),r(14,17,11,8,1,1)]))
add('folder',folder)
add('document',page([r(11,11,10,10,2,11)]))
add('text',page(doc))
add('image_file',page([r(9,9,14,14,2,1),l(10,21,15,14,2),l(15,14,22,21,2),r(18,11,3,3,2,12)]))
add('audio_file',page([l(13,10,13,22,2,3),l(13,10,22,8,3,3),l(22,8,22,20,2,3),r(9,21,5,4,2,3),r(18,19,5,4,2,3)]))
add('archive_file',page([*[r(15,8+i*3,3,2,0,4) for i in range(5)],r(14,23,5,3,1,4)]))
add('package',tile(4,[r(5,8,22,19,3),l(7,10,16,15,2,4),l(16,15,25,10,2,4),l(16,15,16,25,2,4),l(10,6,21,6,2)]))
add('executable',page([r(9,9,15,14,2,1),r(10,12,13,10,1,7),l(12,14,15,17,2,1),l(15,17,12,20,2,1),l(17,20,21,20,2,1)]))
add('shortcut',[r(1,15,17,15,3,6),r(2,16,15,13,2,7),l(5,25,5,21,2,6),l(5,21,13,21,2,6),l(10,18,13,21,2,6),l(13,21,10,24,2,6)])
add('usb',[r(10,2,12,9,2,6),r(11,3,10,7,1,7),r(13,4,2,3,0,6),r(17,4,2,3,0,6),r(7,10,18,20,5,2),r(14,23,4,3,2)])
add('network',[r(11,3,10,9,2,1),l(16,12,16,19,2,6),l(6,19,26,19,2,6),r(2,21,9,8,2,1),r(21,21,9,8,2,1)])
add('volume',[r(3,6,26,23,4,6),r(4,7,24,21,3,7),r(6,9,20,12,2,11),r(7,24,13,2,1,6),r(24,24,2,2,1,2)])
add('back',[l(21,7,11,16,3,6),l(11,16,21,25,3,6)])
add('forward',[l(11,7,21,16,3,6),l(21,16,11,25,3,6)])
add('up',[l(7,18,16,9,3,6),l(16,9,25,18,3,6),l(16,9,16,26,3,6)])
add('copy',[r(5,4,17,20,3,6),r(7,6,13,16,2,7),r(11,10,17,20,3,6),r(13,12,13,16,2,7)])
add('cut',[r(4,20,9,9,5,6),r(6,22,5,5,3,7),r(20,20,9,9,5,6),r(22,22,5,5,3,7),l(7,5,24,24,2,6),l(25,5,8,24,2,6)])
add('paste',[r(6,5,21,25,3,6),r(8,7,17,21,2,7),r(11,2,11,8,2,2),*doc])
add('trash',[r(8,9,17,21,3,6),r(10,11,13,17,2,7),r(5,6,23,3,1,6),r(12,2,9,4,2,6),l(14,14,14,24,2,6),l(20,14,20,24,2,6)])
add('search',[r(3,3,21,21,11,6),r(6,6,15,15,8,7),l(21,21,29,29,3,6)])
add('power',tile(5,[r(6,7,20,21,10),r(9,10,14,15,7,5),r(12,5,8,8,0,5),l(16,5,16,17,3)]))
add('start',[r(3,3,26,26,7,2),l(10,9,22,9,3),l(10,16,19,16,3),l(10,23,22,23,3),l(10,9,10,23,3)])
add('home',[l(3,15,16,4,3,6),l(16,4,29,15,3,6),r(7,13,18,16,2,6),r(13,20,6,9,1,7)])
add('refresh',[l(8,8,25,8,3,6),l(25,8,25,18,3,6),l(24,24,7,24,3,6),l(7,24,7,14,3,6),l(21,4,25,8,3,6),l(25,8,21,12,3,6),l(11,20,7,24,3,6),l(7,24,11,28,3,6)])
add('save',[r(3,3,26,26,4,2),r(8,4,15,9,1),r(18,5,3,6,0,2),r(8,18,16,11,2),r(11,21,10,2,1,2),r(11,25,10,2,1,2)])
add('close',[l(7,7,25,25,3,6),l(25,7,7,25,3,6)])
add('minimize',[l(6,23,26,23,3,6)])
add('maximize',[r(5,5,22,22,2,6),r(7,7,18,18,1,7)])
add('restore',[r(10,3,19,19,2,6),r(12,5,15,15,1,7),r(3,10,19,19,2,6),r(5,12,15,15,1,7)])
add('check',[l(5,17,12,24,3,2),l(12,24,27,7,3,2)])
add('warning',tile(4,[r(14,7,4,13,2),r(14,24,4,3,2)]))
add('keyboard',[r(1,7,30,21,4,6),r(3,9,26,17,3,7),*[r(5+x*5,12+y*5,3,3,1,6) for y in range(2) for x in range(5)],r(9,23,14,2,1,6)])
add('mouse',[r(7,1,18,30,9,6),r(9,3,14,26,7,7),l(16,4,16,13,2,6),l(9,14,23,14,2,6)])
add('sound',tile(3,[r(5,13,6,8,1),l(11,13,17,8,3),l(17,8,17,25,3),l(17,25,11,21,3),l(22,12,25,16,2),l(25,16,22,21,2)]))
add('gpu',[r(2,6,28,20,3,2),r(6,9,17,14,7),r(10,12,9,8,4,2),r(26,10,2,10,1),*[r(7+i*4,26,2,4,0,4) for i in range(5)]])
add('wifi',[l(4,12,16,5,3,6),l(16,5,28,12,3,6),l(9,18,16,14,3,6),l(16,14,23,18,3,6),r(13,23,6,6,3,2)])
add('usb_hub',[r(11,11,10,10,3,2),l(16,3,16,11,2,6),l(3,16,11,16,2,6),l(21,16,29,16,2,6),l(16,21,16,29,2,6),r(12,1,8,4,1,6),r(1,12,4,8,1,6),r(27,12,4,8,1,6)])

PALETTES = [
    [0,0x245db2,0x087c71,0x684ba8,0xa44a12,0xa93855,0x17212f,0xf8fafc,0xffffff,0x946318,0xf2cb7b,0x526173,0xffe8ae,0x253d57],
    [0,0x245db2,0x087c71,0x684ba8,0xa44a12,0xa93855,0xe8edf5,0x161d27,0xffffff,0xe8bb68,0xf2cb7b,0xabb7c6,0xffe8ae,0x253d57]
]

def main():
    lines=['/* Original Engacer OS icon geometry, generated by tools/design/icons12.py. MIT. */',
           'enum ui12_icon_id { '+', '.join('ICON12_'+name.upper()+'='+str(i) for i,(name,_) in enumerate(ICONS))+', ICON12_COUNT };',
           'static const ui12_shape icon12_shapes[] = {']
    offsets=[0]
    for name,shapes in ICONS:
        assert 1<=len(shapes)<=32
        lines.append(' /* '+name+' */')
        for shape in shapes:
            assert all(0<=v<=32 for v in shape[1:6]) and 0<shape[6]<14
            lines.append(' {'+','.join(map(str,shape))+'},')
        offsets.append(offsets[-1]+len(shapes))
    lines+=['};','static const uint16_t icon12_offsets[] = {'+','.join(map(str,offsets))+'};',
            'static const uint32_t icon12_palettes[2][14] = {'+','.join('{'+','.join(hex(c) for c in p)+'}' for p in PALETTES)+'};']
    (ROOT/'include/engine/ui/icons12_data.h').write_bytes(('\n'.join(lines)+'\n').encode())
    out=ROOT/'docs/architecture/figures/m12-icons';out.mkdir(parents=True,exist_ok=True)
    for number,(name,shapes) in enumerate(ICONS):
        svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" role="img"><title>Engacer '+name.replace('_',' ')+'</title>']
        for kind,x,y,w,h,radius,color in shapes:
            fill='#'+format(PALETTES[0][color],'06x')
            svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}"/>' if not kind else f'<path d="M{x} {y}L{w} {h}" stroke="{fill}" stroke-width="{radius}" stroke-linecap="round"/>')
        (out/(name+'.svg')).write_bytes((''.join(svg)+'</svg>\n').encode())
    (out/'catalog.json').write_bytes((json.dumps(dict(license='MIT',provenance='Original Engacer OS geometric artwork; no external icon or Windows assets',coordinate_grid=32,icons=[dict(id=i,name=name,shapes=len(shapes)) for i,(name,shapes) in enumerate(ICONS)]),indent=2)+'\n').encode())
    print('Generated',len(ICONS),'original icons;',len(lines),'native data lines; no raster atlas.')

if __name__=='__main__':main()
