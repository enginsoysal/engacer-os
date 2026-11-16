"""Exercise public-release immutability and interrupted-draft admission without HTTP."""
import copy,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];spec=importlib.util.spec_from_file_location('publish12',ROOT/'tools/release/publish12.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main():
    rows=[dict(name=f'asset-{n}',size=n+1,sha256=f'{n:064x}') for n in range(20)]
    draft=dict(draft=True,prerelease=False,target_commitish='a'*40,body='English notes\r\n',assets=[])
    check=lambda r,d=True:m.check_release(r,rows,'a'*40,'English notes\n',d)
    assert len(check(draft))==20
    assets=[dict(name=r['name'],size=r['size'],digest='sha256:'+r['sha256']) for r in rows]
    draft['assets']=assets[:7];assert len(check(draft))==13
    draft['assets']=assets;assert check(draft)==[]
    public=copy.deepcopy(draft);public['draft']=False;assert check(public,False)==[]
    cases=[]
    for key,value in [('draft',False),('prerelease',True),('target_commitish','b'*40),('body','Changed notes')]:
        changed=copy.deepcopy(draft);changed[key]=value;cases.append(changed)
    for key,value in [('size',100),('digest','sha256:'+'f'*64),('name','unrelated-asset')]:
        changed=copy.deepcopy(draft);changed['assets'][0][key]=value;cases.append(changed)
    changed=copy.deepcopy(draft);changed['assets'].append(changed['assets'][0]);cases.append(changed)
    for changed in cases:
        try:check(changed)
        except AssertionError:pass
        else:raise AssertionError('Unsafe release was admitted')
    incomplete=copy.deepcopy(public);incomplete['assets'].pop()
    try:check(incomplete,False)
    except AssertionError:pass
    else:raise AssertionError('Incomplete public release was accepted')
    tag='m128-v0.12.8';base='repos/enginsoysal/engacer-os/releases';calls=[]
    listed=dict(id=128,tag_name=tag,**draft)
    def request(path,**options):
        calls.append((path,options))
        if path==base+'/tags/'+tag:return None
        if path==base+'?per_page=100':return [[dict(id=1,tag_name='unrelated')],[listed]]
        if path==base+'/128':return copy.deepcopy(listed)
        raise AssertionError('Unexpected API route')
    assert m.lookup_release(tag,request)==listed
    assert calls[1][1]==dict(paginate=True) and calls[2][0].endswith('/128')
    assert m.lookup_release(tag,lambda path,**kwargs:None if '/tags/' in path else [[]]) is None
    def denied(path,**kwargs):raise RuntimeError('HTTP 403; absence is not established')
    try:m.lookup_release(tag,denied)
    except RuntimeError:pass
    else:raise AssertionError('Lookup failure was interpreted as a missing release')
    def duplicate(path,**kwargs):return None if '/tags/' in path else [[listed],[listed]]
    try:m.lookup_release(tag,duplicate)
    except AssertionError:pass
    else:raise AssertionError('Duplicate draft identity was admitted')
    def changed(path,**kwargs):
        if '/tags/' in path:return None
        if '?per_page=' in path:return [[listed]]
        return dict(listed,id=129)
    try:m.lookup_release(tag,changed)
    except AssertionError:pass
    else:raise AssertionError('Changed draft identity was admitted')
    public_lookup=dict(listed,draft=False)
    assert m.lookup_release(tag,lambda path,**kwargs:public_lookup)==public_lookup
    try:m.check_release(public_lookup,rows,'a'*40,'English notes\n',True)
    except AssertionError:pass
    else:raise AssertionError('Direct public lookup became a mutable draft')
    print('PASS: matching empty/partial/full drafts and public readback; nine unsafe release cases and six tag/draft lookup cases checked without HTTP or mutation.')
if __name__=='__main__':main()
