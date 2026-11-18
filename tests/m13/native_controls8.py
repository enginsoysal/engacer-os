"""Run the unchanged ordinary-input gallery journey with the M13.8 observer."""
import importlib.util
from pathlib import Path
import observer8

spec = importlib.util.spec_from_file_location('native_controls_stage8',
                                             Path(__file__).with_name('native_controls.py'))
journey = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journey)
assert journey.args.stage >= 8 and not journey.args.baseline
observer8.bind(journey.ui)
journey.main()
