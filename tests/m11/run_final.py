"""Run dependent native tests in order; failures stop the selected lane."""
import argparse,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LANES={
 'files':[['files.py'],['file_preferences.py'],['drag_cancel.py'],['selection.py']],
 'start':[['start.py'],['start_controls.py']],
 'windows':[['windows.py'],['window_keys.py'],['window_motion.py']],
 'setup':[['setup.py','--profile','ordinary'],['setup.py','--profile','150'],['setup_packages.py'],['setup.py','--profile','4k'],['setup_safety.py']],
 'hardware':[['hardware.py'],['hardware.py','--ram','64'],['hardware.py','--firmware','bios'],['hardware.py','--resolution','3840x2160','--hub'],['hardware.py','--large-usb'],['usb_negative.py'],['usb_quota.py'],['known_boot.py']],
}
a=argparse.ArgumentParser();a.add_argument('lane',choices=LANES);args=a.parse_args()
env=os.environ.copy();env['ENGACER11_IMAGE']='EngacerOS-M11FINAL'
if args.lane=='setup':env.pop('ENGACER11_DISMISS_GUIDE',None)
else:env['ENGACER11_DISMISS_GUIDE']='1'
out=ROOT/'build/m11/lanes';out.mkdir(parents=True,exist_ok=True)
for command in LANES[args.lane]:
 label='-'.join(command).replace('.py','');print('Starting',args.lane,label,flush=True)
 with (out/(label+'.log')).open('w',encoding='utf-8') as log:
  run=subprocess.run([sys.executable,str(ROOT/'tests/m11'/command[0]),*command[1:]],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
 print('Finished',label,'exit',run.returncode,flush=True)
 if run.returncode:raise SystemExit(run.returncode)
