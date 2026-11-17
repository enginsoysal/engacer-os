"""Create UTF-8 release notes with immutable canonical source links."""
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
from urllib.parse import quote, unquote, urlsplit

ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',type=int,required=True);parser.add_argument('--ref',default='HEAD');args=parser.parse_args()
    assert 1<=args.stage<=12
    ref=subprocess.check_output(['git','rev-parse',args.ref+'^{commit}'],cwd=ROOT).decode('ascii').strip()
    path=f'docs/releases/m13{args.stage}-v0.13.{args.stage}.md'
    source=subprocess.check_output(['git','show',ref+':'+path],cwd=ROOT).decode('utf-8')
    files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',ref],cwd=ROOT).decode('utf-8').splitlines())
    def link(match):
        label,target=match.groups();target=target.removeprefix('<').removesuffix('>')
        if target.startswith('#') or urlsplit(target).scheme:return match.group(0)
        parts=urlsplit(target);assert not parts.netloc
        resolved=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(parts.path)))
        assert resolved in files and not resolved.startswith('../'),resolved
        origin='https://raw.githubusercontent.com/enginsoysal/engacer-os/' if label.startswith('!') else 'https://github.com/enginsoysal/engacer-os/blob/'
        url=origin+ref+'/'+quote(resolved,safe='/')
        if parts.query:url+='?'+parts.query
        if parts.fragment:url+='#'+parts.fragment
        return label+'('+url+')'
    text=re.sub(r'(!?\[[^\]]*\])\(([^)]+)\)',link,source).replace('\r\n','\n')
    assert not any(marker in text for marker in ('\u00e2\u20ac','\u00c3\u2014','\ufffd'))
    out=ROOT/f'build/m13/stage{args.stage}';out.mkdir(parents=True,exist_ok=True)
    data=text.encode('utf-8');(out/'release-notes.md').write_bytes(data)
    (out/'release-notes.json').write_bytes((json.dumps(dict(stage=f'M13.{args.stage}',source_commit=ref,source_path=path,encoding='UTF-8',sha256=hashlib.sha256(data).hexdigest()),indent=2)+'\n').encode())
    print(f'Prepared canonical UTF-8 M13.{args.stage} notes at source '+ref)

if __name__=='__main__':main()
