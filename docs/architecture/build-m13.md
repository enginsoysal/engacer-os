# Isolated M13 build workspace

Use the canonical standalone checkout and the existing pinned project toolchain. This recipe describes the current Windows development host; Linux/macOS build hosts are not qualified by it. Never put OS source or media in BrixCanvas.

Prepare the external scratch directory once, then build the next authorized stage:

```powershell
pwsh -NoProfile -File tools/build/prepare-m13.ps1
python tools/build/m13.py --stage 1
```

The preparation script creates `build/m13-native` as a junction to LocalAppData `EngacerOS/Build/m13`. It never deletes or replaces an existing path. Keep the final directory named `m13`: retained font/package generators dispatch on this isolated build identity. The separate `build/m13` folder contains small reports and design metadata. Large VM fixtures and raw framebuffer observations stay in external owned workspaces.

This keeps generated images out of OneDrive while preserving historical M12 and design-only M13.0 output. Native debug-prefix mapping and release privacy checks prevent external host paths from entering published artifacts. An unexpected existing junction/directory is refused rather than moved or erased.

`m13.py` checks the preceding stage's publication receipt and the profile version before compiling. Published media are immutable: use the next stage or a separately identified development revision after closure. Data-only distribution choices remain in `distros/engacer-desktop-m13.json` under the existing validated schema.

A successful build is not runtime qualification. Run the matching native/profile and exact VMware tests, inspect physical framebuffer captures, verify committed input digests, then publish matching English guides, source, release assets and the actual BrixCanvas website before the next stage. Complete M13.12 regression is separate from each scoped preview.
