"""Run the original environment regression against app-private temporary storage."""
from pathlib import Path

directory = Path(__file__).resolve().parent
observer = directory / "environment143_native.py"
source = observer.read_text(encoding="utf-8")
source = source.replace("EngacerOS-M14STAGE3", "EngacerOS-M14STAGE10")
source = source.replace("from apps_native3 import task", """import capture14
from thread_native2 import task
import os
os.environ['ENGACER12_IMAGE']='EngacerOS-M14STAGE10'
t.ui.IMAGE12=t.ui.IMAGE11='EngacerOS-M14STAGE10'
capture14.bind(t.ui)""")
source = source.replace("stage3/environment-native", "stage10/private-temp-native")
source = source.replace("stage3/apps/results.json", "stage10/compact/results.json")
source = source.replace("m143-path-apps", "m141-stage10-compact")
source = source.replace("m143-environment", "m1410-private-temp")
source = source.replace("M14.3 development", "M14.10 development")
needle = " mounted=StoppedDisk(disk,library())"
assert source.count(needle) == 1
source = source.replace(needle, """ boot=ui.guest(work/'prepare',disk,media='installed',ready='M7_DESKTOP_READY',ram=128)
 ui.s.normal_boot(boot)
 with boot as g:
  p=ui.Pointer(g);p.drain();c.key(g,'esc');t.close_all(g,p);t.launch(g,p,'windows apps',19)
  p.desktop(12001,True);task(g,p,12003)
""" + needle)
needle = "   report['temporary_files_remaining']=remaining;"
assert source.count(needle) == 1
source = source.replace(needle, """   principal=hashlib.sha256(b'/Users/Owner').hexdigest()[:32]
   path='/Applications/Windows/{23170F69-40C1-2702-2606-000001000000}/.Engacer/Temp/'+principal
   entries=f.entries(g);assert entries[path]['kind']==2
   assert not any(p.startswith(path+'/') for p in entries)
   report['private_temporary_directory']=path
""" + needle)
exec(compile(source, str(observer), "exec"), {"__file__": __file__, "__name__": "__main__"})
