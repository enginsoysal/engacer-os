"""Reuse ordinary-input guest primitives with isolated M12 artifact identities."""
import importlib.util
import os
from pathlib import Path

os.environ['ENGACER11_IMAGE'] = os.environ.get('ENGACER12_IMAGE','EngacerOS-M12STAGE1')
spec = importlib.util.spec_from_file_location('shared_m11_ui',Path(__file__).resolve().parents[1]/'m11/ui.py')
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
globals().update({k:v for k,v in vars(shared).items() if not k.startswith('__')})
IMAGE12 = IMAGE11
iso_path12 = iso_path11
manifest_path12 = manifest_path11
