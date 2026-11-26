# M14.9 implementation handoff

## Acceptance scenarios

| Scenario | Expected outcome | Owner |
| --- | --- | --- |
| Standalone and nested setup | Ordinary Install creates one fresh bundle identity. Each approved nested operation inherits that identity through broker and restart. | M14.10, M14.12 |
| Late required .NET request | Failure identifies the requesting app, runtime family, target version when known and architecture. The user reviews the dependency source and target before setting up. | M14.11, M14.14 |
| Separately downloaded installer | Normal Install stays primary. Advanced asks for an existing app. Right-click starts with its selected app identity. Both use the same reviewed transaction as automatic assistance. | M14.12, M14.14 |
| Incompatible component and cancellation | Wrong architecture or version has a distinct failure. Cancellation performs no publication and preserves the previously installed generation. | M14.10–M14.12 |
| Removed target or reused path | The broker checks current AppId, user and generation before work and at publication. A replacement at the same path cannot inherit the old authority. | M14.10, M14.12 |
| Cross-app paths, links and stale handles | Exercise ordinary, aliased and renamed paths and surviving handles. B stays unreadable and unwritable without its own grant. An injected owner claim cannot authorize access. | M14.10 |
| Same service name | A and B resolve to separate owned service instances. Stopping A leaves B able to perform its actual task. | M14.11 |
| Two copies of the same library | Install A and B from two fixtures with identical dependency bytes and Windows-visible names. Verify distinct backing objects, registry values and actual calls. Update, repair and remove A, then boot and repeat B's task. Include conflicting library versions and simultaneous execution. | M14.10–M14.15 |
| Ambiguous legacy reference | Preserve the source data. Require attributable ownership or a clean install. Verify cancellation and interrupted migration recover the prior state. | M14.12 |
| Architecture variants | M14.10 exercises necessary x86 helpers of x64 apps. M15 extends standalone x86. M16 exercises Win16 and DOS drive/configuration isolation and the applicable execution mode. | M14.10, M15, M16 |

## Legacy inputs

M14.8 EXE bookkeeping lives under `/Data/Windows/<owner-hash>/EXE/<product>.bin`
and identifies the original reviewed source and product root. The MSI transaction
implementation checks the product's `.EngacerMSI/transaction.bin`, `product.bin`
and a protected completion record. Treat these records as provenance inputs.
Preserve the old records until migration has verified the copied bytes and
new private registrations. An incomplete legacy transaction requires its own
recovery or a clean reinstall before import. Preserve unattributed shared
registrations and personal documents.

## Release and resource boundaries

The [v1 contract](windows-app-contract-v1.md) sets record and graph limits.
Apply the [M14 measurement protocol](windows-m14.md) to the first equivalent
working lifecycle and freeze that measurement before optimization. M14.9's lab
validates the schema and records Windows behavior. Native isolation, retention
and performance measurements belong to the implementing milestones.

The [Windows reference](windows-behavior-reference-m149.md) records published
contracts, observed cases and the questions that require a specific guest.
The decision to use published behavior first applies to M14.9 closure.
Windows 7, 8, 8.1, 10 and 11 remain distinct reference profiles for tests
that depend on version differences. Record the exact build when measured.
