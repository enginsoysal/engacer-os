"""Add a disk-only restart to every retained owned common-dialog assertion."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def editor_pixels(g,p,content,out):
    from PIL import Image,ImageDraw,ImageFont
    from window144_native import ui,c,f
    c.key(g,'end')
    c.shot(g,'unicode-save-after-independent-start')
    image=Image.open(out/'unicode-save-after-independent-start.png').convert('RGB')
    assert image.size==(1280,800)and c.flag(g,'scale73')==2
    x,y,_,_=f.model(g)[1]
    actual=image.crop((x+24,y+126,x+24+260,y+126+24))
    font=ImageFont.truetype(str(ROOT/'third_party/inter/Inter.ttf'),16)
    font.set_variation_by_axes([16,400])
    alpha=Image.new('L',(260,24));draw=ImageDraw.Draw(alpha);pen=0
    label=content.removesuffix('\r\n')
    for char in label:
        draw.text((pen,font.getmetrics()[0]),char,font=font,fill=255,anchor='ls')
        pen+=round(font.getlength(char))
    expected=Image.merge('RGB',tuple(alpha.point(lambda a,ch=channel:(ch*a+255*(255-a)+127)//255)for channel in (25,40,56)))
    actual.save(out/'actual-editor-first-line.png');expected.save(out/'expected-editor-first-line.png')
    assert actual.tobytes()==expected.tobytes(),'Native editor scalar/CRLF pixels differ from fresh Inter reference'
    return dict(passed=True,text=label,exact_rgb_sha256=hashlib.sha256(actual.tobytes()).hexdigest(),checked_pixels=260*24,physical_font_size=16,crlf_does_not_paint_extra_glyph=True)

def derive(source):
    source=source.replace("stage6/picker-native'", "stage6/picker-restart-native'")
    source=source.replace("'m146-picker-native'", "'m146-picker-restart-native'")
    before="  assert ui.s.s.document(disk,source_path,8192)==payload.encode();"
    assert source.count(before)==1
    restart="""  reboot=ui.guest(work/'disk-only-reopen',disk,media='installed',ready='M7_DESKTOP_READY',ram=128);ui.s.normal_boot(reboot)
  with reboot as g:
   p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);editor=t.launch(g,p,'text editor',2)
   assert t.app_view(g).length==0
   p.desktop(54000,True);p.desktop(54016,True)
   index=f.entries(g)[target_path]['index']
   for _ in range(128):
    if any(row[5]==55000+index for row in f.controls(g)):break
    p.desktop(54023,True)
   else:raise AssertionError('Saved Unicode destination unavailable after independent start')
   p.desktop(55000+index,True);c.key(g,'ret')
   wait_for(g,lambda:bytes(t.app_view(g).text)==final.encode())
   assert not t.app_view(g).dirty
   report['editor_body_pixels']=editor_pixels146(g,p,final,out)
   p.desktop(49002,True)
   report['independent_start_reopened_unicode_path_and_bytes']=True
"""
    return source.replace(before,restart+before)

def main():
    canonical=ROOT/'tests/m14/picker146_run.py'
    raw=canonical.read_bytes();source=derive(raw.decode())
    namespace={'__file__':str(canonical),'__name__':'picker_restart146_derived','editor_pixels146':editor_pixels}
    exec(compile(source,str(canonical),'exec'),namespace)
    namespace['main']()
    out=ROOT/'build/m14-native/stage6/picker-restart-native'
    report={'canonical_path':'tests/m14/picker146_run.py','canonical_sha256':hashlib.sha256(raw).hexdigest(),'executed_sha256':hashlib.sha256(source.encode()).hexdigest(),'adapter_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'All retained common-dialog assertions plus actual disk-only startup and native reopening of the Windows-saved Unicode path/content'}
    (out/'observer.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())

if __name__=='__main__':main()
