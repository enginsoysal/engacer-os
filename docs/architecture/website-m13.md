# M13 documentation portal and search contract

Owner-approved direction, 17 November 2026. M13.0 includes an actual task-first index/homepage update plus a search prototype and an explicit production capability assessment. This is the BrixCanvas-hosted Engacer website, not replacement hosting.

## Reader navigation

The central Git-tracked `website/brix/portal.json` owns section order, curated current guide paths, reader-facing labels and archive policy. Use six entries: Start here, Install, Use Engacer OS, Customize, Project & development, Downloads. The archive is clearly secondary. Display current download M12.18 independently from design program M13.0. Publication dates and lexical filename ordering never decide the reader route.

Each section contains a short ordered list with task titles rather than milestone numbers. Installation precedes everyday use; implementation internals and historical releases are separate. Preserve all existing article URLs and historical identity. The archive sorts numeric milestone identities naturally and remains discoverable; no mass article deletion or rewriting accepted OS evidence.

Current guides retain honest release/scope labels. A curated link to an M12 guide does not claim it describes an unbuilt M13 desktop. As native stages qualify, update the index and release-specific manuals together. Downloads always select qualified OS media, not the newest design prerelease.

## Target reader layout

Desktop: header plus bounded category sidebar, article, local table of contents for long guides and explicit Previous/Next within a curated task route. Mobile: Browse documentation drawer, readable article width, no horizontal page overflow. Home offers Download, Install and Read the guide. Recommended content is task-related, not randomly chosen from old milestones.

The current production article renderer supplies chronological Previous/Next and related posts; the content publisher cannot replace those renderer controls simply by changing Markdown. Until a scoped BrixCanvas template extension is implemented, put explicit ordered task-route links in generated portal content and do not claim renderer-side sidebar/chronological controls are fixed. Do not deploy unrelated shared-platform changes under an Engacer content update.

## Same-page search target

- A header search control and Ctrl+K open a labelled modal search panel without changing the current URL or scroll position.
- Results are grouped by Guides, Troubleshooting, Downloads and Development. Current curated guides rank before archived history. Include archived documentation is an explicit opt-in.
- Arrow keys select, Enter opens, Escape closes and returns focus to the opener; Tab remains inside the open dialog. Pointer and narrow mobile layouts work. Clear query, loading, no-result and failure states have useful actions.
- Match titles, task aliases and headings first; bound result count and work. Do not download every article body per keystroke or expose site/editor credentials. Search data comes from the same public manifest and canonical source commit.
- Preserve `/search` as an accessible fallback/deep link; it is not the desired primary interaction.

## Actual BrixCanvas capability assessment

The authenticated native editor exposes a Search Brix with a text field and Search submit button. Its preview and the currently published site have been inspected; these observations do not demonstrate an accessible result overlay, archive filtering or Ctrl+K. The existing content API publishes articles/settings and does not by itself add arbitrary renderer behavior.

M13.0 therefore delivers an interactive offline prototype with the required states and a visible pending production-overlay item. The tracked implementation target is M13.1. Production implementation must either use a verified supported native search mode or a narrowly scoped BrixCanvas component/template extension with schema, ownership, keyboard/focus, ranking, mobile, failure and cross-site regression tests. Preserve ordinary fallback search until the replacement actually passes. No browser-injected JavaScript or external-hosted replacement is a production solution.

## Migration and verification

1. Inventory every generated source article and classify current, technical reference or historical; fail on duplicate/unknown curated references.
2. Generate the short ordered main index and separate complete archive; preserve unique reachability of old articles.
3. Publish canonical docs from GitHub, wait for verified sync, then refresh/edit/save the actual native homepage.
4. Verify fresh homepage, current install/use/customize/project routes, all article retention, natural archive order, exact source links, current ISO/VMware hashes, mobile layout and existing fallback search.
5. Test the offline overlay prototype separately; record it as design evidence. Keep production overlay/sidebar renderer work visibly pending until real public interaction tests pass.

The continuing website gate applies after every M13 submilestone. A successful Git push alone never closes it. Native OS changes, content publication, portal template behavior and human usability remain separate claims.
