# Engacer OS — project instructions

## Scope and architecture

- This standalone repository is the canonical project. Never place Engacer OS sources, plans, build outputs or evidence in the unrelated BrixCanvas repository.
- The old planning copy has been moved out of BrixCanvas into this repository's ignored `tools/local/legacy-planning` archive. It is historical and must not be published or treated as current source. Use this repository root explicitly as the working directory even when the chat opens elsewhere.
- Read README.md, docs/roadmap/status.md and relevant architecture contracts before implementing changes.
- Build an independent OS and kernel. The owner priority order is M6 real product installation, M7 real desktop, then M8 original MS-DOS and Windows 1.x through Windows 11 applications. Windows is the first foreign application ecosystem; Linux, macOS and ARM remain deferred extensions. Use Engacer OS for new M10 UI/media, retaining historical Engine OS identities.
- Keep milestone implementation and evidence separate from architecture claims. Never mark runtime behavior complete based on a stub, header or host reference test.
- Record each substantial decision with how, why, alternatives, limitations and verification. Keep status and milestone documents consistent.
- All committed documentation, code comments, UI strings and new release notes must be in English. Update architecture, status, tests/evidence and user instructions together whenever behavior or scope changes.
- CPU/RAM efficiency is a primary requirement. Bound allocations/queues, share immutable code, measure peak and retained memory separately, and halt when idle instead of polling. Never equate configured guest RAM with kernel consumption or native probes with Windows compatibility.

## Product requirements

- Owner continuation, 19 November 2026: complete and test M14.1 next, including a browser download choice. Firefox is the first target; Chrome, Brave and Edge are candidates. Clearly separate downloading, installation and actual runtime compatibility. Close English docs, GitHub and the actual website before M14.2.

- Latest owner priority, 19 November 2026: record M14.0-M14.15 and complete M14.0 now. M14 is original Windows x64 installation/use/removal, M15 x86, M16 Win16/DOS. Whole-OS CPU/RAM/HDD-SSD efficiency is a core requirement throughout; M14.14 is a release candidate, M14.15 optimization blocks final release. Every stage closes its tests, English docs, GitHub and complete actual website before the next. M14.0 is static research and task/performance baseline design, not new native GUI compatibility or a new ISO. Preserve M13.13 and all prior accepted evidence. This supersedes the previously proposed next hardware priority.

- Superseding explicit owner instruction during M13.13, 18 November 2026: ninety minutes of testing is sufficient; stop waiting for the eight-hour gate and finish M13.13. The normal-path candidate has over 6,500 actually observed seconds. Preserve the original interrupted report honestly; do not call it an eight-hour or two-hour idle pass. Complete functional saved/unsaved data, independent startup, exact media, English documentation, GitHub and actual website delivery. The owner's attribution to their laptop remains an owner report, not an independently established root cause. This overrides the earlier eight-hour release requirement below and authorizes scoped closure without restarting another ninety-minute run.

- Superseding explicit owner instruction, 18 November 2026: finish M13.9 through M13.12 strictly in order now. All stability investigation, freeze reproduction, idle soaks and reset-chain diagnosis are deferred to M13.13. Stop the current diagnostic and preserve it honestly as partial. Do not reopen M13.8 or start further stability experiments before M13.13. Ordinary functional installation/startup, motion/usability checks and per-stage GitHub/docs/website publication remain required. This overrides earlier stability-first instructions below.

- Latest owner steering, 18 November 2026: continue the ordered milestone sequence and perform comprehensive stability qualification in the final M13.13 stage. The owner now also reports an installer stall at 16%, "Copying and verifying boot files", and considers a host-PC/VMware contribution possible, not established. Retain the earlier M13.8 five-minute freeze and immediate freeze after every subsequent VM reset; resetting before the initial freeze was not tested. Do not dismiss independent guest presentation failures or advertise stability before qualification.

- Owner priority, 18 November 2026: M13.8 is also reported to freeze frequently. Stability takes priority over further visual refinement. Investigate and correct the freezes now in M13.9; M13.12 remains integration qualification and new M13.13 is a blocking stability release gate before further hardware expansion. Treat current M13.8 downloads as testing-only with known freezes; scoped historical task passes are not stability qualification. M13.13 requires eight real hours of idle and active/idle use, visible responsiveness, saved/unsaved data checks, restart coverage and bounded resources; any unexpected hang/restart blocks release.

- Owner addition, 18 November 2026: M13.7 reportedly freezes after long uptime. Continue the current stage sequence while collecting an owned baseline; investigate/correct long-idle and active/idle behavior in M13.9 and repeat real-duration qualification on the exact M13.12 media. This is a blocking final acceptance item, not a presumed GPU fault or something a screensaver fixes. Add an optional lightweight, configurable native screensaver to M13.11, with safe input wake, retained desktop/documents, validated preferences and no new idle polling loop.

- Owner clarification, 18 November 2026: use the existing BrixCanvas editor and publication features for the website. Report missing platform capabilities to the owner instead of starting another BrixCanvas production-source investigation or platform change as part of the OS milestone work. Continue publishing Engacer OS code, documentation and releases to its canonical GitHub repository after each milestone.

- Owner priority, 17 November 2026: complete M13.1–M13.12 strictly in order after accepted M13.0 under docs/milestones/m13.md. Include website information architecture and same-page search design. This is the last dedicated appearance/usability sequence before hardware recognition. Close tests, English docs, GitHub and actual native Brix homepage/content/mobile/search/download checks after every stage before the next. M13.0 is design-only; M12.18 remains the native download. Preserve all accepted M12 media/evidence. Do not claim prototype search or concepts are production/native implementation.

- Owner priority, 16 November 2026: execute M12.0 through M12.18 strictly in
  order under docs/milestones/m12.md and docs/architecture/desktop-m12.md.
  Close each stage with appropriate tests, English documentation, a scoped
  GitHub delivery and fresh complete public website verification before the
  next stage. M12.0 is design only; M11.6 remains the tested ISO until new
  native media are qualified. Preserve M11FINAL artifacts and accepted evidence.
  Keep large disposable VM fixtures outside OneDrive. Earlier pending M11.6
  statements below are historical: its M11-FINAL-VM-v1 qualification is complete.

- Owner request, 16 November 2026: finish M11.5, test its actual setup/installed
  startup, publish its source/evidence/docs/site and exact release assets, then
  remove temporary local build output to reduce OneDrive storage. Verify online
  assets before deletion; preserve canonical source, Git history and evidence.
  M11.6 remains separately unqualified until its complete regression is run.

- Owner clarification during M11.4, 11 November 2026: close every remaining
  stage as a complete public delivery before proceeding: matching tests, English
  manuals, GitHub source and a visible release with matching downloadable media,
  plus complete fresh website/homepage/download readback. Commits alone are
  insufficient. Stage releases must state their actual qualification; broader
  M11.6 regression remains pending until tested. This supersedes withholding all
  M11 stage downloads until M11.6. Do not attribute the M10 controller matrix to
  an untested M11 artifact. Only remove obsolete local derived files after
  verifying canonical source/evidence and release assets are on GitHub; preserve
  active work and tests. Respect automatic approval rejections.

- Owner priority, 11 November 2026: execute M11.0 through M11.6 strictly in order.
  Close each stage with its required checks, English documentation, GitHub push
  and verified public article/homepage update before implementing the next stage.
  Follow docs/milestones/m11.md and docs/architecture/desktop-m11.md. Keep the
  M10 delivery immutable and use isolated M11 build/artifact/evidence paths.
  Design concepts are not native runtime evidence. The later M11.4 clarification
  above adds separately scoped stage releases/downloads before M11.6 full
  qualification. This priority precedes later hardware and Windows expansion.

- Owner priority, 10 November 2026: M10 implements phases 1 and 2 of the approved
  hardware program before further Windows profiles. Deliver a common bounded
  inventory/capability model and Settings → Devices, useful desktop input/display,
  writable removable USB storage with graphical transfer/safe removal/reconnect,
  and new exact-artifact VMware media/tests. Maintain honest virtual versus
  physical qualification and preserve accepted releases. The owner subsequently
  selected Engacer OS: use that brand for new M10 UI/media/docs, preserving
  historical Engine OS artifacts and internal contracts. Verify the intended
  engaceros.brixcanvas.com route before retiring the old address. This naming
  instruction supersedes the earlier Engine OS naming requirement above.
  See docs/milestones/m10.md.

- Owner priority, 9 November 2026: complete real IDE/SATA/SCSI installation and independent startup through automatic native controller support. Installer admission must use verified read/write/flush capability rather than a SATA name check. Test each implemented controller/firmware combination with shipped devices enabled. Also support reachable partially off-screen window movement with safe signed clipping. Do not label the broader hardware program universally complete from a virtual controller matrix.

- Owner-reported M9 starter failure, 9 November 2026: an enabled e1000e NIC without PCIe root ports crashed VMware. Starter qualification must retain every shipped device enabled and may add only owned observation channels. Offline tests remain separate. Drain COM1 observations while waiting for frames; test instrumentation must not stall the guest.

- Owner requirement, 8 November 2026: review every installation step for inexperienced children and older adults. Disk choices must be an obvious bounded list with whole-row hit targets, visible selection and useful disabled actions. Next must not clear/reload the entire UI. Completion requires actual installed startup, including the common retained-ISO case; a live-session desktop is insufficient. Keep novice scenario review distinct from a real human study.

- Owner priority, 9 November 2026: M9 automatic hardware support now precedes further M8 application expansion. First address stuttering VMware folder-window movement with measured graphics/input improvements and automatic supported-device binding. Do not infer complete hardware support, GPU acceleration or smoothness from an enumerated adapter or a screenshot.

- Owner requirement, 7 November 2026: appearance and convenience are first-class acceptance criteria. Review every ordinary step, error, confirmation and desktop surface for clarity, convenience, user friendliness, graphical quality and readability. Use consistent semantic typography, measured text, spacing and visual hierarchy; reject overlapping or clipped essential text, arbitrary adjacent font sizes and pixel-enlarged bitmap UI fonts. Verify the real native UI at ordinary and HiDPI resolutions, including an actual 3840x2160 framebuffer. Keep user control over suitable scaling. Do not call a browser mockup or an upscaled screenshot proof of native 4K support. Human usability studies remain distinct from the agent's design review.

- Convenience and user friendliness are acceptance requirements from the first boot. Ordinary install/repair tasks must use guided choices, clear review/cancel, readable errors and optional details; terminal syntax and placeholders are not the normal user flow.
- M6 requires a native graphical Back/Next/Finish wizard with retained customizable choices and meaningful progress. A browser mockup is design evidence only. Optional apps must be independently removable: the desktop/base cannot depend on Calculator. Resolve shared/required dependencies explicitly; never silently cascade app removal into system removal. Follow docs/architecture/components.md.
- Preserve distribution freedom through validated, versioned profiles and working custom ISO examples. Only advertise configuration choices that affect implemented behavior. Core destructive-operation guards cannot be bypassed by a theme/profile.
- Follow docs/architecture/product-principles.md; automate complete user tasks and distinguish those checks from an actual human usability study.

## GitHub publication — explicit user instruction

The owner requested an open-source project and that every update goes to GitHub.

- After each coherent completed update, run the checks appropriate to that change, inspect the diff, update status/evidence where needed, commit and push to the canonical GitHub repository before reporting completion.
- This instruction authorizes routine publication of project changes; do not repeatedly ask for permission to push.
- Never publish credentials, private accounts, proprietary installers/SDKs, unrelated project files or raw local user paths. Use public evidence with sensitive paths redacted.
- Do not use force-push or discard others' changes. Fetch and reconcile concurrent work safely.
- If a check fails, retain the honest result and fix the problem. If publication fails, report the exact failure and do not claim synchronization.
- Use codex/ prefixes for new task branches. Follow repository branch rules; the initial baseline lives on main.

## Licensing and safety

- Original project contributions use the root MIT license. Third-party components retain their own notices and require provenance/license review before inclusion.
- Run OS/storage tests against disposable images or explicitly designated test devices. Never treat the development host disk as a test target.
- Avoid global tool replacements; prefer pinned project-local tool manifests.

## Accepted release immutability

M4.5, M5, M5.1, M6, M7, M7.1, M7.2, M7.3, M7.4, M7.5, M8, the M9-GFX-VM-v1 delivery and the M91-STARTER-v1 correction and the M92-STORAGE-VM-v1 delivery accepted evidence, tags and release binaries are historical proof. Do not rerun a development build/test into their frozen output paths or rewrite accepted hashes. Use a new follow-up prefix/evidence directory; reproduce a historical release only in a separate checkout.

M9.2 known/unqualified QEMU reports are preserved as failures, not successful startup qualification. Future work must not rewrite them into historical passes. Never rebuild media/maps while guest tests read those artifacts; freeze source and all build outputs through qualification. Use a new revision/artifact/evidence prefix for subsequent work.


M10 hardware phases 1 and 2 are accepted within M10-DEVICES-VM-v1. Its ISO, exact VMware ZIP, manifests and evidence are immutable after publication. New work must use a new milestone/revision and preserve these bytes. The canonical product/repository/site are Engacer OS, enginsoysal/engacer-os and engaceros.brixcanvas.com. Legacy internal identifiers and historical artifacts remain stable.

M11.0 design and M11.1/M11.2/M11.3/M11.4/M11.5 native evidence and STAGE1/STAGE2/STAGE3/STAGE4/STAGE5
artifacts are accepted stage records, separate from final M11 qualification.
Preserve their bytes and evidence after their publication gates. Subsequent
stages use FINAL or later distinct output prefixes; never rebuild STAGE1/STAGE2/STAGE3/STAGE4/STAGE5 in place.
During M11 the public homepage led with its current progress and matching separately
scoped stage release. M12 now takes precedence. Preserve M10 as historical qualification. Keep the index ordered by
reader task, with current installation/use before internals and historical guides.

M11.6 FINAL and M12.0 design/publication evidence are accepted records. Preserve
M11FINAL media and the original M12.0 SVGs/design archives. New native work uses
M12STAGE<n> artifacts and evidence/M12/<n>. build/m12 is an owned junction to
external local scratch storage; never place sparse VM fixtures in OneDrive.

M12.1 M12-STAGE1-VM-v1 and its public delivery are accepted. Preserve its stage
media, source stamp and evidence/M12/1; use M12STAGE2 or later for new work.

M12.2 M12-STAGE2-VM-v1 and its complete public delivery are accepted. Preserve
M12STAGE2 bytes, source stamp and evidence/M12/2. Use stage3 or later for new work.
Carry the open BIOS/AHCI observation into final M12.18 qualification.

M12.3 M12-STAGE3-VM-v1 and its complete public delivery are accepted. Preserve
M12STAGE3 media, source stamp and evidence/M12/3. New work uses stage4 or later.
Retain the tested caption-capture hover suppression and the recoverable per-user
desktop reference preference; the earlier BIOS/AHCI observation remains open.

M12.4 M12-STAGE4-VM-v1 and complete public delivery are accepted. Preserve
M12STAGE4 media, source stamp and evidence/M12/4. New work uses stage5 or later.
Retain owner guards across caption, keyboard and system-menu routes. Carry
shared-menu footer fitting to M12.14 and cursor-versus-hit HiDPI isolation to
M12.16; the BIOS/AHCI observation remains open for M12.18.

M12.5 M12-STAGE5-VM-v1 and complete public delivery are accepted. Preserve
M12STAGE5 media, source stamp and evidence/M12/5. Use stage6 or later for new
work. Retain generation-bound USB history, explicit replacement selection and
the guarded Files dispatch before the generic application handler. Existing
M12.14/M12.16/M12.18 carry-forward observations remain open.

M12.6 M12-STAGE6-VM-v1 and complete public delivery are accepted. Preserve
M12STAGE6 media, source stamp and evidence/M12/6. New work uses stage7 or later.
Retain full-name tip owner/row guards, source-bound ordering and generation-bound
USB navigation. Carry the named M12.14/M12.16/M12.18 observations forward.

M12.7 M12-STAGE7-VM-v1 and complete public delivery are accepted. Preserve
M12STAGE7 media, source stamp and evidence/M12/7. New work uses stage8 or later.
Retain cooperative transfer/provider ownership guards, bounded FAT metadata
cache and the compressed installer validation/recovery contract. The build must
refuse a live fixed-address ELF crossing the named firmware 8-MiB boundary.
Carry menu/conflict feedback to M12.14, cursor isolation to M12.16 and the earlier
BIOS/AHCI stress observation to M12.18. Future publication must resolve matching
drafts by release ID when tag lookup returns 404, never recreate/replace them.

M12.8 M12-STAGE8-VM-v1 and complete public delivery are accepted. Preserve
M12STAGE8 media, source stamp and evidence/M12/8. New work uses stage9 or later.
Retain checked existing-page IPC loading, array-free Tab, picker owner/shortcut
and display-size guards. M12.14 must qualify background transfer conflict-review
admission/arbitration alongside prior menu feedback. M12.16 must isolate the
cursor observation and reconcile explicit scale limits with compact startup
modes; 1280x1024 refused 200%, while actual 150%/4K/200% passed separately.
Keep the earlier BIOS/AHCI stress observation open for M12.18.


M14.0 research and M14.1 M14-STAGE1-VM-v1 native/public delivery are accepted within their recorded scopes. Preserve M14STAGE1 media, tags and native evidence. New native work uses M14STAGE2 or later and evidence/M14/2 or later. Firefox is a verified installer download only, not a working modern browser. M14.2 remains separately authorized work; do not infer completed threads, TLS or Windows GUI from this loader stage.
