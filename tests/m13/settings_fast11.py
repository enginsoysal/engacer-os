"""Run the unchanged Settings task with the grouped fresh-read observer."""
import os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
os.environ['ENGACER12_IMAGE']='EngacerOS-M13STAGE11'
sys.path.insert(0,str(ROOT/'tests/m12'))
import ui
original_pointer=ui.Pointer
import settings_search11 as journey
import observe20
journey.observer['functional_barrier']=observe20.bind(journey.ui,original_pointer)
journey.main()
