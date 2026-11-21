# Original Windows installers in M14.8

**Development guide. M14.8 is not yet a qualified download.** Continue using
the [qualified M14.7 guide](windows-m147.md) with M14.7 media. This page describes
the new candidate workflow; final native and public delivery gates remain open.

## Choose and review an installer

1. Put the unchanged original installer in your Engacer OS Downloads folder.
2. Open Start, search for **Windows Apps**, and open it.
3. Choose **Choose installer...**, open Downloads, select the file and choose Open.
4. Choose **Review installer**. This reads its identity without installing it.
5. Read the result. A supported profile enables installation; unknown installers
   remain review-only. Renaming a file does not enable compatibility.
6. Choose **Install app** and read the confirmation, including destination and
   original command-line arguments. Back cancels before execution.

If the source changes, select and review the original again. Confirmation never
silently grants unrestricted access to the rest of the system.

## Original EXE installer workflow

The first candidate profile uses unchanged [SumatraPDF 3.6.1 x64 from its
official download](https://www.sumatrapdfreader.org/dl/rel/3.6.1/SumatraPDF-3.6.1-64-install.exe):
`SumatraPDF-3.6.1-64-install.exe`, 11,075,960 bytes, SHA-256
`1eee71cccd2ea6e94d5bcea54ee2f759844da3e1a0ee2f6045035b1d17b94381`.

After confirming, use the original installer window and choose Install. Keep
the reviewed default destination, `C:\Program Files\SumatraPDF`; other paths
are outside this profile's grant. Installation creates real original program
files and native shortcuts. When the original window says installation has
finished, close that window with its title-bar X. Wait for Windows Apps to
verify the result and report completion.

**Start SumatraPDF is the original reader launch button, not a finish button.**
The reader itself is not a qualified task in this installer milestone. Closing
the installer does not assert that its reader, preview extension or PDF filter
can be used yet. The fallback decorative font also differs from Windows.

## Remove and reinstall

Open Windows Apps, choose Installed apps, select the product and choose Remove
app. Read and confirm the removal request. Use the original uninstaller window;
after it reports completion, close it and wait for native verification. The
unchanged installed program supplies its own uninstaller and helper chain.

Modified or extra product files block this bounded EXE removal profile instead
of authorizing their silent deletion. Personal documents remain outside the
product grant. Keep interrupted EXE records for inspection: automatic EXE
rollback/recovery is not qualified. The existing MSI recovery instructions apply
to supported MSI transactions, not to arbitrary interrupted EXE programs.

To reinstall, select the unchanged original download, review and confirm again.
Do not manually delete protected inventory records to bypass a conflict.

## Existing supported MSI tasks

The [M14.7 walkthrough](windows-m147.md) describes the original 7-Zip and
Notepad++ MSI profiles. In Windows Apps, Run 7-Zip console runs its console program;
Open file manager opens the qualified graphical preview. Installing Notepad++
does not qualify using its editor. Browser choices download an installer;
Firefox browsing is not qualified yet.

## Scope and efficiency

Original Windows instructions execute natively through Engacer OS compatibility
APIs and its own kernel. There is no embedded Windows guest. A named test profile
is evidence of particular tasks, not the product scope: the approved broader
program targets the full x64 application landscape.

The broker rechecks source identity, inherits immutable grants to its permitted
helpers, waits for descendants without busy polling and independently verifies
completion. Buffers, handles and temporary work are bounded. Actual measured
peaks and retained memory must accompany final acceptance; configured VM RAM
does not measure OS consumption. Whole-system optimization remains M14.16.

[M14.8 implementation and current evidence](../milestones/m14-8.md) Â·
[Approved M14.9-M14.16 plan](../milestones/m14-consolidated.md)
