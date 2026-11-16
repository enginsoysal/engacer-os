"""Qualify only matching M12.1 source, media, native tests and fixed resources."""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'build/m12/stage1'
OUT=ROOT/'evidence/M12/1'

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_bytes((json.dumps(value,indent=2)+'\n').encode())

def git_inputs(records):
    paths=list(records)
    raw=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=''.join('HEAD:'+p+'\n' for p in paths).encode(),capture_output=True,check=True).stdout
    at=0
    for path in paths:
        end=raw.index(b'\n',at);header=raw[at:end].split()
        assert len(header)==3 and header[1]==b'blob',path
        size=int(header[2]);body=raw[end+1:end+1+size];at=end+size+2
        assert hashlib.sha256(body).hexdigest()==records[path],('Git source differs',path)
        assert sha(ROOT/path)==records[path],('Working source differs',path)

def desktop_state(path):
    text=path.read_text();sections={}
    for section in ('bss','data'):
        found=re.findall(r'^\s*[0-9a-f]+\s+[0-9a-f]+\s+([0-9a-f]+)\s+\d+\s+.*kernel_desktop_session-kernel.o:\(\.'+section+r'\)$',text,re.M)
        assert len(found)==1,(section,found);sections[section]=int(found[0],16)
    return dict(bytes=sum(sections.values()),sections=sections,map_sha256=sha(path))

def copy_report(source,dest):
    dest.mkdir(parents=True,exist_ok=True)
    for file in source.iterdir():
        if file.is_file() and file.suffix in ('.json','.png','.log'):
            if file.suffix=='.png':shutil.copyfile(file,dest/file.name)
            else:(dest/file.name).write_bytes(file.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))

def main():
    meta=load(ROOT/'dist/m12stage1-build-manifest.json')
    starter=load(ROOT/'dist/m12stage1-starter-manifest.json')
    native=load(WORK/'components/results.json');bios=load(WORK/'bios/results.json')
    vmware=load(WORK/'vmware-results/results.json');motion=load(WORK/'motion/results.json')
    host=load(WORK/'host-results.json')
    assert meta['build_revision']=='stage1' and meta['release_version']=='0.12.1'
    assert meta['qualification_scope']=='M12-STAGE1-VM-v1'
    assert all(r['passed'] for r in (starter,native,bios,vmware,motion,host))
    iso=meta['artifacts']['EngacerOS-M12STAGE1.iso']['sha256']
    for report in (starter,native,bios,vmware,motion):assert report['build_id']==meta['build_id']
    for report in (native,bios,vmware,motion):assert report['iso_sha256']==iso
    assert vmware['starter_sha256']==starter['sha256']==sha(ROOT/'dist'/starter['archive'])
    assert vmware['existing_vm_inventory_unchanged'] and len(vmware['checks'])>=3
    assert len(native['checks'])>=13 and len(bios['checks'])==3
    assert native['retained_page_delta']==0
    assert native['setup_full_paints_before_install'][0]==native['setup_full_paints_before_install'][1]
    assert [p['physical'] for p in native['display_profiles']]==[[1920,1200],[3840,2160]]
    assert [p['physical'] for p in motion['profiles']]==[[1280,800],[1920,1200],[3840,2160]]
    for profile in motion['profiles']:
        assert profile['managed_bytes_before']==profile['managed_bytes_after']
        assert profile['all_cpus_halted_when_idle'] and profile['idle_paints_unchanged'] and profile['cached_copy_frames']>0
        assert len(profile['comparisons'])==4 and all(c['cached_equals_full_viewport'] for c in profile['comparisons'])
    for name,width,height in [('installed-desktop',1280,800),('native-150',1920,1200),('native-4k',3840,2160)]:
        capture=load(WORK/f'components/{name}-capture.json');assert (capture['width'],capture['height'])==(width,height)
    git_inputs(meta['source_sha256']);git_inputs(host['source_sha256'])
    for folder in ('boot','kernel','include','runtime','user'):
        assert {p.relative_to(ROOT).as_posix() for p in (ROOT/folder).rglob('*') if p.is_file()}<=meta['source_sha256'].keys()
    for name,record in meta['artifacts'].items():assert sha(ROOT/'dist'/name)==record['sha256']
    baseline=load(ROOT/'evidence/M11/6/resources.json')['fixed_desktop']['FINAL']
    current=desktop_state(ROOT/'dist/EngacerOS-M12STAGE1-installed-kernel.map')
    extra=current['bytes']-baseline['bytes'];assert 0<=extra<256*1024
    font=load(ROOT/'build/m12/font73-manifest.json')
    assert font['coverage_bytes']==251248 and font['header_sha256']==load(ROOT/'third_party/inter/raster-lock12.json')['header_sha256']
    assert host['font_coverage_delta_bytes']==-19662 and host['m11_raster_lock_unchanged']
    preserved=load(ROOT/'evidence/M12/0/preserved-baseline.json')
    for record in preserved['artifacts']:assert sha(ROOT/'dist'/record['name'])==record['sha256']
    OUT.mkdir(parents=True,exist_ok=True)
    for name,source in [('native','components'),('bios','bios'),('vmware','vmware-results'),('motion','motion')]:copy_report(WORK/source,OUT/name)
    shutil.copyfile(WORK/'vmware-results/shared-components.png',OUT/'feature.png')
    shutil.copyfile(ROOT/'dist/m12stage1-build-manifest.json',OUT/'candidate-manifest.json')
    shutil.copyfile(ROOT/'dist/m12stage1-starter-manifest.json',OUT/'starter-manifest.json')
    shutil.copyfile(WORK/'host-results.json',OUT/'host-results.json')
    diagnostics=OUT/'diagnostics';diagnostics.mkdir(exist_ok=True)
    for file in (WORK/'diagnostics').iterdir():
        if file.is_file() and file.suffix in ('.json','.txt'):(diagnostics/file.name).write_bytes(file.read_bytes().replace(str(ROOT).encode(),b'<project-root>'))
    resources=dict(passed=True,scope='Fixed desktop state and font masks are separate from the complete kernel, installer bundle, firmware and shared framebuffers; configured RAM is not consumption',baseline=baseline,current=current,added_fixed_desktop_bytes=extra,budget_bytes=256*1024,font=font,font_coverage_delta_bytes=-19662,native=native['display_profiles'],motion=motion['profiles'])
    write(OUT/'resources.json',resources)
    harness={p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'tests/m12').iterdir() if p.suffix in ('.py','.c')}
    write(OUT/'acceptance-results.json',dict(passed=True,stage='M12.1',version='0.12.1',qualification='M12-STAGE1-VM-v1',build_id=meta['build_id'],iso_sha256=iso,vmware_zip_sha256=starter['sha256'],source_inputs_verified=len(meta['source_sha256']),artifacts_verified=len(meta['artifacts'])+1,native_checks=native['checks'],bios_checks=bios['checks'],vmware_checks=vmware['checks'],cached_full_comparisons=12,resources='resources.json',harness_sha256=harness,feature_sha256=sha(OUT/'feature.png'),limits=['Named stage-specific virtual profiles only; full controller/device/original-app regression remains M12.18','No new physical/ARM, vendor GPU 3D or general DOS/Windows compatibility qualification','Agent scenario and visual review; not a human usability study','Build/source qualification is separate from GitHub release and native Brix homepage publication']))
    print('PASS: matching M12.1 native/BIOS/VMware/motion/source/resource acceptance. Fixed desktop growth:',extra)

if __name__=='__main__':main()
