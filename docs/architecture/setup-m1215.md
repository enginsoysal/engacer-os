# M12.15 setup and first use

M12-STAGE15-VM-v1 native qualification passes. [Complete public delivery](../../evidence/M12/15/publication-results.json) passes. M12.16 follows in order.

## Shared visual language

The native installer uses the desktop component palette, semantic typography,
measured labels and original application icons. Body and secondary controls use
16-pixel logical text. Selected accents choose a contrasting foreground from
luminance rather than assuming white is readable. No browser runtime, external
UI framework or additional framebuffer cache is introduced. Reusing the native
component functions avoids a second typography/palette implementation and the
RAM cost of a browser-based installer. Compact pages remove decorative previews
instead of shrinking essential text or hiding the actual choices.

## Responsive guided choices

The ordinary eight steps retain Welcome, Keyboard / size, Choose a disk, Your
apps, Your style, Review, Installing and Ready. The simple wizard targets a
logical 800 by 600 workspace; compact pages omit decorative previews rather
than essential choices. Advanced partition tools retain their existing logical
1024 by 768 admission limit. This distinction must remain explicit in testing
and the manual. Smaller workspaces offer automatic sizing instead of drawing
unsigned out-of-bounds controls.

The outer setup frame persists while content changes. Existing frame counters
and native pixel captures must verify Next and Back without a full-screen
reload. Keyboard focus follows the primary action when the actual step changes.

## Preserve destructive-operation ownership

The renderer reuses the existing action IDs, controller capability checks,
partition operations and separate whole-disk Review consent. Selecting a disk
never writes it. Back clears destructive consent where required. Installation
must copy and read back the actual system and then start the installed desktop;
a live desktop or a success label alone does not qualify the installation.
Recovery has four explicitly named steps and preserves personal files.

## First use and distribution independence

The bounded first-start card belongs to the base desktop. Its Files, Start,
Appearance and dismissal actions do not require optional Calculator or Editor
packages. Its colours follow the saved theme. The optional packaged quickstart
uses the current navigation and Apply and save / Cancel vocabulary, stays below
the existing editor text limit and describes actual provider limitations.
Application management lives inside required Settings, using its existing bounded
package view and backend. The optional Software launcher is not a dependency.
Returning from management uses Back to the remembered Settings category.
The alternative of forcing Software into every package profile would weaken
optional-app independence. Reusing the existing Settings package view keeps
management available without changing package IDs or backend admission. This
fix follows a real No optional apps test that exposed the previous launch
dependency; the earlier candidate results are retained as diagnostics.
Distribution profiles retain their validated app masks, branding, appearance
and guide preferences; visual customization cannot bypass disk safety.

## Qualification scope

Real guest journeys must cover all ordinary pages, compact and HiDPI layouts,
Back and cancellation, exact pre-install disk preservation, partition changes,
write failure and recovery, first use and independent no-ISO startup. Resource
retention, idle halt, enabled-device VMware, BIOS and cached/full rendering
remain required. Automated scenario review is separate from a human usability
study. No universal hardware or expanded Windows compatibility follows.
