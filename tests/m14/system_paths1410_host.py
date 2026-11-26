"""Run the path-policy regression with per-app system DLL views."""
from pathlib import Path

source = Path(__file__).with_name("helper_paths147_host.py").read_text(encoding="utf-8")
source = source.replace("stage7/helper-path-host", "stage10/helper-path-host")
source = source.replace("custom=entries):", "custom=entries,product=b'/Applications/Windows/App'):")
source = source.replace("b'/Applications/Windows/App',b'C:", "product,b'C:")
start = source.index("        for leaf in ['other.exe'")
end = source.index("    assert call(", source.index("assert call(", start) + 1)
source = source[:start] + r"""        for app in ('App', 'Other'):
            product = ('/Applications/Windows/' + app).encode()
            code,native,_ = call('C:\\Windows\\' + directory + '\\common.dll',product=product)
            assert code == 0 and native == product.decode() + '/System/' + directory + '/common.dll'
        assert call('C:\\Windows\\' + directory + '\\xcopy.exe:stream')[0] == 50
""" + source[end:]
exec(compile(source, __file__, "exec"))
