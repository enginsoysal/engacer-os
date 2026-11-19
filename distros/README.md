# Distribution recipes

## Current M14 desktop recipes

Use `engacer-desktop-m14.json` as the schema-3 starting profile and follow the [current distribution-building guide](../docs/handbook/distributions.md). It explains the matching qualified tag, separate custom checkout, scratch storage outside OneDrive, actual M14 builder entry point, optional app ownership and independent custom-media tests. Changing identity or theme does not implement unsupported Windows APIs or hardware drivers.

## Historical M5.1 examples

The remaining commands and limited fields describe the old M5.1 tools. They are not the current desktop recipe. The retained Forge profile is an old example identity, not a rename of Engacer OS.

`engineos.json` builds the standard M5.1 release. `forge.json` builds a working example with different branding, accent and an additional selected data package. Both keep guided setup and mandatory disk safety checks.

```powershell
python tools/build/m51.py --profile distros/forge.json --validate-only
python tools/build/m51.py --profile distros/forge.json
```

Output goes to `dist/profiles/<id>/`. Use unique profile IDs. The original kernel, live/installed system and ISO/USB media are actually built; the profile is not a screenshot/theme mockup. The standard build also copies its official artifacts to `dist/EngineOS-M51*`.

Only the documented branding and data-package fields are supported by that historical builder. No desktop, executable package manager or install hook is implied. [Complete recipe tutorial and limits](../docs/handbook/distributions.md), [product principles](../docs/architecture/product-principles.md), [MIT license](../LICENSE).
