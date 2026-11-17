# M12.13 development observation

`split-preview-observer.json` is a failed development probe, not native
qualification. The pinned compiler split the private preview record into six
scalar symbols instead of retaining one addressable 32-byte symbol. The
observer now reads those actual field symbols through the established
read-only helper. Production source and media stayed unchanged.

The repeated smoke and full native journeys have their own matching reports,
captures, independent disk-byte checks and resource observations. No guest
memory was modified to manufacture a result. The final qualifier names its
successful groups separately and preserves this failed observation.
