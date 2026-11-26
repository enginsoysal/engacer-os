# M14.9 environment contract v1

## Identity and durable records

The native package broker creates a random 128-bit AppId when a standalone install is reviewed. It binds that ID to the OS user ID and generation. Generations increase on replacement and never wrap or reuse an old authority. Only the broker publishes a generation. The kernel attaches that identity to each process and passes it to authorized children and broker calls. File handles and object handles retain the resolved owner and generation. A stale handle cannot act on a replacement bundle.

The [v1 record schema](windows-app-records-v1.schema.json) defines manifest, transaction and activation event shapes. Persist the manifest and journal under the protected .Engacer directory. Authority stays in a kernel object, with a transaction ID, owner, operation, source hash, permitted rights and expiry. A serialized record never grants rights. After reboot the broker verifies the durable journal and current identity before issuing fresh authority. A cancelled or deleted target invalidates outstanding authority.

The resolver validates unique component IDs, existing graph edges, acyclicity and depth at most 32 before staging. A single app may reuse its own dependency; identical requirements in two apps resolve to physically separate copies. Default ceilings are 256 components, 64 direct edges per component, 1 MiB per serialized record and 64 queued activation events per app. On overflow reject graph changes or count dropped events. Validate overhead against measured workloads in M14.10 and later. Limits are design inputs.

## Ownership and handoff

| Resource | Storage and lifecycle | Enforcement milestone |
| --- | --- | --- |
| Program files, private DLLs, temp and user preferences | App root under Program, Dependencies, System and Profiles. Loader resolves only that app's approved paths. | M14.10 |
| Registry | Registry under app root. HKLM software is app-owned, HKCU also binds the user, HKCR resolves that app's user classes over its machine classes. Explicit 32/64 views are tested by key family. | M14.10 |
| Named objects and handles | Kernel scoped to app identity, granting principal and generation. Last owner closes or broker cleans up. | M14.10 |
| Runtime assemblies, COM and services | Private files and registrations, activation routed through the app context. Stop only owned instances. | M14.11 |
| Install journal and shortcut references | Protected app journal, rebuildable OS shell index keyed by AppId. Stage, verify and publish or recover the prior generation. | M14.12 |
| Device resources and personal documents | OS owned. App access derives from a scoped grant, with revocation on teardown. | M14.10 and M14.13 |

Resolve Program Files, Windows, System32, SysWOW64 and AppData through the app namespace. The resolver selects architecture and profile from verified process identity. Win16 and DOS may use private drive roots and configuration files in the same bundle format. Preflight graph and storage costs before any mutation. Refuse cross-owner links and handles when resolving the target object, including after rename.

## Install decisions and errors

Reviewed flows into staging, verification and commit pending, then committed. Cancellation or failure before publication goes through rollback pending to rolled back. If durable readback cannot establish either outcome, retain the journal as needs attention. The broker decides whether to finish publication or restore the previous generation after verifying the journal and stored bytes.

An ordinary install starts with a fresh AppId. Automatic assistance starts with a specific app and necessary unresolved request. Right-click Add dependency supplies the existing AppId before source selection. A standalone installer offers target selection under collapsed Advanced options. All dependency routes review the target and exact source before staging. Nested helpers inherit context. A late .NET error can request a version review. Optional lookups, wrong architecture and access denials receive distinct diagnostics. Cancellation and a removed target must leave existing components intact.

## Migration and acceptance

M14.8 EXE ownership data in the protected Data/Windows record and the product path are migration inputs. Legacy MSI product and journal records may identify files, registry preimages and integrations. Only independently attributable entries can be staged into one new bundle. Compare source and destination bytes and keep the previous installation recoverable until verified. Unknown shared registrations remain untouched and lead to a clean reinstall route.

Run A and B with separate physical copies of the same component, record bytes, registry and actual work, update and remove A, then cold-start B and repeat the original task. Also exercise conflicting dependency versions, stale tickets after removal, cross-owner path and handle resolution, interrupted commits and optional activation probes. M14.10 through M14.15 supply native evidence. Quantify duplication, peak and retained memory, CPU, I/O and restart costs under the existing M14 protocol.
