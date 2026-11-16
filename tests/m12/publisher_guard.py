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
    print('PASS: matching empty/partial/full drafts and public readback; nine unsafe visibility/source/body/asset/public cases rejected without HTTP.')
if __name__=='__main__':main()
