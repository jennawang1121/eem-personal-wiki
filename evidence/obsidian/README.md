# Obsidian walkthrough — completed

Verified in the real Obsidian 1.13.7 application on September 29, 2026 (America/Los_Angeles). All screenshots are direct app captures, with no rendered mockups or image edits.

| Evidence | What it shows |
|---|---|
| [Note](note-final.png) | Natural Monopoly Regulation: matching title/path, source references with paragraph ranges, and meaningful related links |
| [Index](index-final.png) | All twelve topics grouped under Energy, Environment, Markets and Regulation |
| [Graph](graph-final.png) | All twelve curated topic nodes and their connections; filter `path:wiki/`, Attachments off |
| [Graph settings](graph.png) | The actual filter and Attachments switch before zoom/pan adjustments |
| [Reading copy](source-trace.png) | Quiz 2 verbatim text, paragraph locators, preserved figures, and original-file link |
| [Word original](original-opened.png) | The Quiz 2 original opened by following the source link |

## Observed navigation

1. Opened `index.md` in reading view and followed its Natural Monopoly Regulation link.
2. Followed the related Tax and Price Controls link; verified the note content and heading changed.
3. Followed its Quiz 2 text-and-figures link; verified `sources/EEM Quiz 2 Cheat Sheet.md` and the preserved diagrams.
4. Followed “Open unchanged Word original.” Microsoft Word opened the exact `personal-wiki/vault/raw/EEM Quiz 2 Cheat Sheet.docx` path, confirmed in its accessibility window URL. No save or edit was performed.
5. Opened graph view, applied `path:wiki/`, confirmed Attachments off, and adjusted the view until the twelve labels were readable. Settings were closed for the final capture.

This UI walkthrough complements the separate full filesystem validation of all 95 wiki links and source hashes. The previous interrupted status and captures are preserved below for provenance; they do not describe the final state.

---

## Historical interrupted status

# Obsidian walkthrough status

Status: incomplete. The CLI is available again and an actual [note screenshot](note.png) has been saved. Remaining screenshot types and full navigation are still pending.

## Observed

- Obsidian 1.13.7 is installed and the project `vault/` is open.
- Desktop permissions were granted.
- The English EEM Study Wiki index was visible in reading view, with Energy, Environment, Markets and Regulation groups and descriptive links.
- Following Natural Monopoly Regulation changed the outer window title, but subsequent screenshots and accessibility content still showed the index. A fresh app connection and a computer-use session reset did not resolve the stale content. One attempt returned `noWindowsAvailable`.
- An earlier Obsidian CLI call did not execute because the automatic approval-review service had reached its usage limit. A subsequent authorized attempt succeeded and saved the note screenshot. Native UI control remains intermittent (`noWindowsAvailable` on a later scroll).

The title change alone is not counted as a successful navigation check. Filesystem validation separately confirms 95 unambiguous wiki links, source paths and unchanged re-ingestion.

## Capture when desktop control is working

1. Open `index`, then Natural Monopoly Regulation. Capture its short filename, matching heading, source references and related links; use two frames if needed for readability.
2. Follow Tax and Price Controls, then its Quiz 2 reading-copy link, then the original Word link. Confirm the source catalog also opens the correct evidence.
3. Capture the topic-organized index or file list.
4. Open graph view, use `path:wiki/`, hide Attachments, and adjust zoom until note labels and connections are readable. Record the actual filter in the final screenshot caption.
5. Save real screenshots here as `note.png`, `index.png`, `graph.png` and, if useful, `source-trace.png`. Add links to the README only after those files exist and are inspected.

Do not replace missing Obsidian screenshots with a rendered mockup or mark these steps complete without observing the result.
