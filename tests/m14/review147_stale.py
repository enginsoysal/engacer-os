"""Ordinary native Terminal write invalidates a previously confirmed MSI review."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
 source=ROOT/'tests/m14/review147_native.py';raw=source.read_bytes();text=raw.decode();before="    report['checks']=['Chooser opens with MSI filter; cancel preserves previous selection'"
 after="""    package=packages[0];path='/Users/Owner/Downloads/'+package.name;p.desktop(12013,True);p.desktop(54017,True);row=f.entries(g)[path]['index']
    for _ in range(128):
     if any(r[5]==55000+row for r in f.controls(g)):break
     p.desktop(54023,True)
    else:raise AssertionError('Reviewed MSI is not reachable')
    p.desktop(55000+row,True);p.desktop(54011,True);task(g,p,12000);assert state()[1]==1 and state()[4]==1;p.desktop(12001,True);assert any(r[5]==12003 for r in f.controls(g))
    terminal=t.launch(g,p,'terminal',7);c.type_text(g,'write '+path+' Changed reviewed installer');c.key(g,'ret');p.drain();assert b'Write status: 0' in bytes(t.app_view(g).text);p.desktop(49002,True);t.focus(g,p,front);p.drain();assert state()[1]==0
    at=len(g.log())
    if any(r[5]==12003 for r in f.controls(g)):p.desktop(12003,True)
    assert not c.flag(g,'w8_active') and 'M8_CPL3_CREATED'not in g.log()[at:];assert ui.s.s.document(disk,path,4096)==b'Changed reviewed installer';assert not any(k.startswith('/Applications/Windows/')for k in f.entries(g));c.shot(g,'changed-source-refusal');report['changed_source_blocks_confirmation']=True
    report['checks']=['Chooser opens with MSI filter; cancel preserves previous selection'"""
 replacements=[('stage7/review-native','stage7/review-stale-native'),('m147-review-native','m147-review-stale-native'),(before,after)]
 for a,b in replacements:assert text.count(a)==1,(a,text.count(a));text=text.replace(a,b)
 out=ROOT/'build/m14-native/stage7/review-stale-native';out.mkdir(parents=True,exist_ok=True);(out/'observer.json').write_bytes((json.dumps(dict(canonical_sha256=hashlib.sha256(raw).hexdigest(),executed_sha256=hashlib.sha256(text.encode()).hexdigest(),replacements=replacements),indent=2)+'\n').encode());namespace={'__file__':str(source),'__name__':'review147_stale'};exec(compile(text,str(source),'exec'),namespace);namespace['main']()
if __name__=='__main__':main()
