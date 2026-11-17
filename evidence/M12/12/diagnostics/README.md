# M12.12 development observations

These records are not accepted native passes. The final acceptance report
names the matching successful journeys separately. Production media stayed
frozen while the observation harness was corrected.

- `ambiguous-observer-symbol.json`: distinguish the 640-byte storage registry
  from another private table with the same C symbol name; read all sixteen
  40-byte records and retain their actual index.
- `qemu-auto-removed-drive-backend.json`: QEMU removed the original `-drive`
  backend with its USB device. Reattachment now creates an explicit new backend
  for the unchanged owned source before adding the new device.
- `optional-caption-observation.json`: the immediate caption assertion ran
  before the requested Clock caption was available. The repeated journey waits
  for the exact live generation's real registered caption, then clicks it.
- `transfer-not-yet-started.json`: nonblocking injection did not wait for the
  initial pointer move/input queue. The corrected helper drains the initial
  move while idle, then uses nonblocking edges while copying.
- `exclusive-fixture-refusal.json`: exclusive creation correctly refused an
  already existing USB fixture. Each repetition now receives a fresh owned
  scratch directory; older fixtures are preserved.
- `busy-before-completed-repaint.png`: the provider changed before the paused
  capture's completed repaint. The final busy capture waits for a subsequent
  completed native repaint while the real transfer is still active.
- `historical-helper-invocation.json`: a legacy helper ignored `--help` and
  reran only into ignored historical scratch. Accepted source, evidence, tags
  and media were unchanged. A closed-stage entry guard prevents repetition;
  current BIOS qualification uses the explicit stage-aware helper.

No failure is relabeled as a successful test. The final report binds its own
actual source, media, guest input, provider state, captures and resource checks.
