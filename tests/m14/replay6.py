"""Replay canonical scenarios on isolated M14.6 media without editing accepted tests.

Stage identities, owned output/VM names and the documented menu-coordinate
oracle change. The controls fixture uses a separately recorded SDK message-ID
correction while retaining every assertion. Original/transformed observer and
fixture hashes are recorded; accepted earlier-stage bytes remain unchanged.
"""
import hashlib, importlib.abc, importlib.util, json, os, re, sys, traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRECTORY = ROOT / 'tests/m14'
REPLACEMENTS = [('EngacerOS-M14STAGE4', 'EngacerOS-M14STAGE6'), ('M14-STAGE4-VM-v1', 'M14-STAGE6-VM-v1'), ('m14stage4', 'm14stage6'), ('evidence/M14/4', 'evidence/M14/6'), ('stage4', 'stage6'), ('M14.4', 'M14.6'), ('0.14.4', '0.14.6'), ('m144-', 'm146-'), ('EngacerOS-M14STAGE5', 'EngacerOS-M14STAGE6'), ('M14-STAGE5-VM-v1', 'M14-STAGE6-VM-v1'), ('m14stage5', 'm14stage6'), ('evidence/M14/5', 'evidence/M14/6'), ('stage5', 'stage6'), ('M14.5', 'M14.6'), ('0.14.5', '0.14.6'), ('m145-', 'm146-')]

observed = {}


class ReplayLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path=None, target=None):
        if '.' in fullname or fullname == 'replay6':
            return None
        source = DIRECTORY / (fullname + '.py')
        if source.is_file():
            return importlib.util.spec_from_loader(fullname, self, origin=str(source))
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        source = DIRECTORY / (module.__name__ + '.py')
        raw = source.read_bytes()
        text = raw.decode('utf-8')
        for before, after in REPLACEMENTS:
            text = text.replace(before, after)
        # The stable copied view's former reserved word now reports menu height.
        # Keep the accepted observer intact; adjust its screen-coordinate oracle.
        if module.__name__ == 'original_window_trace4':
            before='title=wide(56,312),class_name=wide(312,440)'
            assert before in text
            text=text.replace(before,"menu_height=struct.unpack_from('<I',raw,452)[0],"+before)
        if module.__name__ in ('original_window_trace4','original_menu145_run'):
            before="pointers=struct.unpack('<32Q',ui.memory(g,ui.symbol('ui_windows144',installed=True)[0],256))"
            assert text.count(before)==1
            text=text.replace(before,"slots=ui.symbol('ui_windows144',installed=True);assert slots[1]==128*8;pointers=struct.unpack('<128Q',ui.memory(g,slots[0],slots[1]))")
        if module.__name__ == 'dialog145_build':
            before='104:template(count=32),105:template(count=31)'
            assert text.count(before)==1
            text=text.replace(before,'104:template(count=128),105:template(count=127)')
        if module.__name__ == 'dialog145_host':
            for before,after in [('capacity=400','capacity=1600'),('values[1]<=31','values[1]<=127'),('control_quota=31','control_quota=127')]:
                assert text.count(before)==1
                text=text.replace(before,after)
        if module.__name__ == 'original144_run':
            before="node['bounds'][1]+40;scale="
            assert before in text
            text=text.replace(before,"node['bounds'][1]+40+node.get('menu_height',0);scale=")
        if module.__name__ == 'vmware4':
            before='assert stage==4'
            assert text.count(before)==1
            text=text.replace(before,'assert stage==6')
        if module.__name__ == 'controls144_run':
            assert 'from controls144_build import build' in text
            text=text.replace('from controls144_build import build','from controls145_build import build')
        observed[source.relative_to(ROOT).as_posix()] = {
            'canonical_sha256': hashlib.sha256(raw).hexdigest(),
            'executed_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
        }
        module.__file__ = str(source)
        exec(compile(text, str(source), 'exec'), module.__dict__)
        # Earlier regression adapters read their canonical helpers themselves.
        # Their own receipts must include these same additional stage mappings.
        if module.__name__ in ('runtime_regressions4', 'files_regressions4'):
            module.REPLACEMENTS.extend(REPLACEMENTS)


def main():
    assert len(sys.argv) >= 2 and re.fullmatch(r'[a-z][a-z0-9_]*', sys.argv[1])
    name, arguments = sys.argv[1], sys.argv[2:]
    assert not (ROOT / 'evidence/M14/6/publication-results.json').exists()
    meta = json.loads((ROOT / 'dist/m14stage6-build-manifest.json').read_text(encoding='utf-8'))
    assert meta['qualification_scope'] == 'M14-STAGE6-VM-v1'
    os.environ['ENGACER12_IMAGE'] = 'EngacerOS-M14STAGE6'
    sys.path.insert(0, str(DIRECTORY))
    sys.meta_path.insert(0, ReplayLoader())
    sys.argv = [str(DIRECTORY / (name + '.py')), *arguments]
    receipt = dict(passed=False, stage='M14.6', build_id=meta['build_id'],
                   target=name, arguments=arguments, replacements=REPLACEMENTS)
    try:
        module = __import__(name)
        module.main()
        receipt['passed'] = True
    except BaseException:
        receipt['error'] = traceback.format_exc()
        raise
    finally:
        receipt['observer_sources'] = observed
        receipt['adapter_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        out = ROOT / 'build/m14-native/stage6/replay-observers'
        out.mkdir(parents=True, exist_ok=True)
        suffix = '-'.join(re.sub('[^a-zA-Z0-9_-]', '', a) for a in arguments)
        (out / (name + ('-' + suffix if suffix else '') + '.json')).write_bytes(
            (json.dumps(receipt, indent=2) + '\n').encode('utf-8'))


if __name__ == '__main__':
    main()
