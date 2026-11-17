# M12.17 bounded motion and performance

M12-STAGE17-VM-v1 native qualification passes. Complete public delivery passes: twenty downloads, 399 pages and 2,797 HTTP links, native homepage Save and desktop/mobile/manual/download/search/archive verification. M12.18 follows in order.

## Covered shadow interiors

Rounded translucent shadow layers deliberately leave an interior hole because
an opaque window surface covers it. M12.16 still visited every interior pixel
before skipping its blend. M12.17 jumps directly to that interior span's end on
middle rows, capped by the current clipped right edge. Both edge spans keep the
same antialias samples and alpha arithmetic. Opaque surfaces keep their existing
path. Legacy non-M12 compilation retains its previous iteration behavior.

The change uses one local unsigned counter. It adds no persistent state, worker,
framebuffer, timer, per-window surface or idle scan. Dirty bounds and row-level
audio pumping remain outside the optimized inner loop and retain their cadence.

## Feedback rather than compulsory animation

Controls and window actions remain immediate. Reduced motion retains its
independent saved choice and removes shadows, hover washes and pressed icon/text
nudges. The compositor has no timed animation engine; this stage does not invent
one merely to animate decoration. Escape cancels an in-progress move and restores
the prior rectangle. Input ownership, saved documents and the eight-window bound
remain authoritative while rendering changes.

## Verification boundary

A host probe extracts the exact round-raster function from immutable M12.16 and
the current production file, renaming it and counting visits without replacing
its raster algorithm. It compares 3,073 clipped/signed/scale/alpha cases and real
4K-sized shadow layers, exact resulting pixels, guard bytes, blend calls, dirty
bounds and audio-pump cadence. CPU times in this host probe are not native FPS.

Matching native media separately install, start without ISO, pass complete
keyboard/accessibility/persistence tasks, render the five light/dark/contrast
profiles and preserve cancelled moves. Default-effect motion must compare the
actual cached viewport against an independently forced full repaint at 100%,
150% and physical 4K/200%, including partially off-screen windows. Peak/retained
pages, paint counters, cached-copy activity and all-CPU idle halt are separate
observations. BIOS, enabled-device VMware, original decoder and compressed boot
repair retain their own exact-artifact checks. Earlier results do not qualify
new bytes. Final controller/application qualification remains M12.18.
