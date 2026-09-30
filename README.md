# Fern — EEM Study Wiki

A personal study wiki built from my four EEM cheat sheets, with a CLI and harness that connects **local Gemma** to original-source retrieval. It supports conversational **chat**, standalone factual **ask**, raw **search**, **ingest**, and **help**. No training, remote search, hosted embeddings or cloud fallback is used.

**Current result:** four unchanged Word sources, twelve reviewed topic pages, 28 original-text passages, and 22 preserved images. Three answerable questions return grounded answers; an unsupported exam-schedule question returns insufficient evidence. Eleven code tests pass. These are real local model results.

**Submission preparation:** the [offline recording and review](evidence/offline/20260930T042106Z/REVIEW.md), [required Obsidian screenshots and navigation checks](evidence/obsidian/README.md), and [resumed verification](evidence/resume-verification.json) are complete. The [public repository](https://github.com/jennawang1121/eem-personal-wiki) is published and [anonymous access verified](evidence/public-access-verification.json). **Only course portal submission remains pending.**

## Quick start

On this Mac, double-click [chat.command](chat.command) to chat, or run these commands in Terminal:

```sh
cd "/Users/wangjenna/Documents/ChatGPT/AgenticAI_Class 2/personal-wiki"
./wiki --help
./wiki chat
./wiki search "natural monopoly marginal cost fixed cost"
./wiki ask "According to the notes, what are the limitations of LCOE?" --mode local
```

Use `chat` to discuss study plans and revise previous answers. `/notes QUESTION` forces retrieval, `/reset` clears conversation, and `/exit` quits. `ask` ignores chat history; `search` displays sources only.

Open **this project's `vault/` folder** as the Obsidian vault, not the whole course folder. Start at [index.md](vault/index.md) or the [reading guide](vault/Reading%20Guide.md).

## Evidence and code entry points

- [Evidence index with all four ask cards](evidence/INDEX.md), [full initial EEM transcript](evidence/evaluation-transcript.txt), [targeted follow-up rerun](evidence/followup-rerun.txt), [source and answer review](evidence/REVIEW.md).
- [CLI/harness](wiki.py), [offline DOCX extractor](source_io.py), [launcher](wiki), [evaluation runner](evaluate.py), [fixed expectations](evals/questions.json).
- [Source catalog](vault/Source%20Catalog.md), [source mappings](sources.json), [original file hashes](documents.json), [extraction report](evidence/extraction-report.json).
- [Eleven code tests](evidence/unit-tests.txt), [vault validation](evidence/vault-validation.json), [re-ingestion record](evidence/reingestion-final.txt), [reusable verification](verify_project.py).

`[[wikilinks]]` work in Obsidian. GitHub readers can follow the ordinary folder/file links here to inspect the same Markdown.

## Data and wiki design

The user selected these four existing study notes. They were copied byte-for-byte to `vault/raw/`; none was corrected or re-exported.

| Original | Main content | Reading copy with exact text and figures |
|---|---|---|
| [Quiz 1](vault/raw/EEM%20Quiz%201%20Cheat%20Sheet.docx) | Markets, monopoly, auctions, hedging, storage | [Quiz 1 text](vault/sources/EEM%20Quiz%201%20Cheat%20Sheet.md) |
| [Quiz 2](vault/raw/EEM%20Quiz%202%20Cheat%20Sheet.docx) | Natural monopoly, regulation, taxes, vertical markups | [Quiz 2 text](vault/sources/EEM%20Quiz%202%20Cheat%20Sheet.md) |
| [Quiz 3](vault/raw/EEM%20Quiz%203%20Cheat%20Sheet.docx) | Carbon policy, electricity, externalities, LCOE | [Quiz 3 text](vault/sources/EEM%20Quiz%203%20Cheat%20Sheet.md) |
| [Final sheet](vault/raw/EEM_Final_Cheat_Sheet.docx) | Integrated review, comparisons and examples | [Final text](vault/sources/EEM_Final_Cheat_Sheet.md) |

Topics are grouped into **Markets, Regulation, Energy and Environment**. Short filenames such as `Natural Monopoly Regulation.md` match their first headings. Overlapping Quiz and Final content is combined into the same subject page rather than generating duplicates. Each page links to its originals, paragraph ranges, reading copies, and relevant related topics. Machine fingerprints stay in properties, not filenames.

The extractor reads every body paragraph, including table-cell paragraphs, in OOXML document order. The Final sheet uses tables for its columns; all 172 table paragraphs are read. Locators are **paragraph numbers, not page numbers**, and match the reading copies. Text and inline text formulas remain as extracted; table relationships are conveyed through their ordered header/cell text. Complex tables can lose spatial meaning, so source views remain important.

All **22 embedded images are preserved unchanged** in `vault/attachments/` and displayed in reading copies. They are **not OCRed or supplied to Gemma**. Figure-only questions cannot be reliably answered by this version. Four source files still count as four original documents, not 22 extra sources. Topic summaries, prompts, chat logs and answer keys are excluded from retrieval.

## Setup from a fresh copy

Tested on Apple Silicon and Python 3.12.14. While online:

```sh
cd personal-wiki
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-tested.txt
.venv/bin/python download_model.py
./wiki --help
./wiki doctor
./wiki ingest vault/raw
./wiki search "natural monopoly marginal cost fixed cost"
./wiki ask "According to the notes, which three aspects of electricity value are ignored by LCOE?" --mode local
./wiki chat
.venv/bin/python -m unittest -v
.venv/bin/python verify_project.py
.venv/bin/python evaluate.py
```

The complete tested dependency list is in `requirements-tested.txt`; direct dependencies are in `requirements.txt`. Downloads occur only in the explicit setup script, which pins the model snapshot. The runtime forces Hugging Face and Transformers offline settings and loads a local path.

On the existing Mac, the launcher reuses `../local-chatbot/.venv/` and `../local-chatbot/model/` if the new project's own environment/model are absent. For direct Python commands here, use `../local-chatbot/.venv/bin/python`. A fresh copy uses its own `.venv/` and `model/` and does not require the earlier project. `WIKI_MODEL_PATH` may point to the **same documented snapshot** elsewhere; recorded model identity assumes this snapshot. The saved [manifest](evidence/model-manifest.json) lets a reader check the actual model/config/tokenizer hashes.

Search, extraction, indexing and help use Python's standard library; they do not require Gemma or a running server. Inference needs MLX and a usable Metal device. Missing models, stale indexes, overlong prompts and inference errors are reported and saved; there is no cloud fallback.

## Ingestion and review

```sh
./wiki ingest vault/raw
# Compare a summary with the originals, edit any misleading claims, then:
./wiki review "Natural Monopoly Regulation"
# Unchanged inputs preserve existing reviewed pages:
./wiki ingest vault/raw
# Rebuild source retrieval without a model call:
./wiki index
# Deliberately regenerate; old pages are backed up and review resets:
./wiki ingest vault/raw --regenerate
```

To add sources, copy an unchanged DOCX/Markdown/text file into `vault/raw/`, add its metadata in `documents.json`, and map subject ranges in `sources.json`. Ranges select original paragraphs for ingestion; they contain no expected test answers. The source index also retains unmapped text, so nothing silently disappears from search. PDF parsing/OCR is not implemented.

Fingerprints include source hashes, topic mappings and ingestion instructions. Unchanged re-ingestion preserves edits without calling Gemma, including after a fresh copy without `.state/`, using the fingerprint stored in the Markdown. Changed inputs or `--regenerate` back up existing pages under `evidence/previous-pages/`, then create drafts marked pending. Indexes live outside the vault in `.state/`. Topic renaming/merging is a deliberate metadata/link migration; automatic topic discovery is not claimed.

The twelve pages were generated by Gemma and then compared against originals by the coding assistant. Corrections and the completed post-offline review are documented in the [review record](evidence/REVIEW.md) and [page-by-page manifest](evidence/post-offline-review.json); owner review is still encouraged. Original Gemma summaries and pre-review pages remain available rather than being replaced with fabricated successful outputs.

## Device, model and measurements

This MacBook Air has an **Apple M4, 10 CPU cores, 10 GPU cores and 16 GB unified memory**, running macOS 27.0 (26A428). CPU and GPU share memory; there is no separate dedicated VRAM. At the saved snapshot, free disk was 169 GiB. Free plus speculative memory pages represented about 0.108 GB, with another 3.85 GB marked inactive and potentially reclaimable; macOS does not report a single guaranteed available-memory value in this snapshot. See [device snapshot](evidence/device-transcript.txt) for Python version, current free disk and raw memory-page counters. `vm_stat` free/inactive/compressed categories are not a guarantee of memory available to a model. Disk storage is not working memory.

| Setting | Exact value |
|---|---|
| Local model | `mlx-community/gemma-4-e2b-it-4bit` |
| Base model | `google/gemma-4-E2B-it` |
| Download snapshot | `238767527555cb75a05732a84dff5d6ba0dd6809` |
| Model-card source revision | `70af34e20bd4b7a91f0de6b22675850c43922a03` |
| Quantization | MLX affine 4-bit, group size 64; not GGUF Q4_0 |
| Weight file | 3,550,670,554 bytes |
| Runtime | MLX 0.32.2, MLX-LM 0.31.3, Transformers 5.17.0 |
| Generation | Thinking disabled; ask/ingest temperature 0, chat 0.3 |
| Limits | 6,000 prompt tokens; 350 answer tokens; 480 ingestion tokens; 2,500 words per topic input |

E2B/E4B describe effective parameter counts and still have embedding-memory overhead. Google's Q4_0 reference loading estimates are about 2.9 GB for E2B, 4.5 GB for E4B and 14.4 GB for 26B A4B. MoE activates about 4B parameters per token but needs all 26B weights loaded for fast routing. Those estimates are not the exact MLX-file size or total application memory. E2B was already local and was sufficient for this small verified corpus; no claim is made that larger models were tested or would necessarily improve it.

References: [Google model/memory guide](https://ai.google.dev/gemma/docs/core), [Google MLX integration](https://ai.google.dev/gemma/docs/integrations/mlx), [model conversion/download](https://huggingface.co/mlx-community/gemma-4-e2b-it-4bit).

Generating twelve EEM topic drafts took **42.60 seconds** including initialization. Model loading took **2.16 seconds**; individual draft generation took 2.01–4.20 seconds. Peak MLX allocation reached **3.28 GB**, while process peak RSS was **1.18 GB**. These counters account for different memory and must not be added or treated as interchangeable. Four ask generations took **1.40, 1.30, 1.25 and 0.81 seconds**, with peak MLX allocation up to **3.33 GB**. Generation timings exclude model loading; warm calls reuse the model. All measured values are saved in the actual run JSON.

## Architecture and one command trace

`./wiki ask "…LCOE…"` enters `main()` in `wiki.py`. The harness selects ask, checks source/index fingerprints, retrieves the top three original passages and loads `prompts/wiki-instructions.md`. It builds a fresh evidence-and-question prompt with [S1] labels, applies Gemma's chat template and calls MLX. It validates citation labels, prints the answer and source locations, then saves the exact response, retrieved passages, model settings and measurements.

- **Model:** Gemma generates text from the prompt. It does not read files or manage tools itself.
- **Retrieval tool:** BM25 over original DOCX text/Markdown, returning text and provenance; no model needed.
- **RAG:** supplies that retrieved evidence to Gemma at answer time; no retraining occurs.
- **Harness:** our connecting code controls modes, conversation, tool use, prompts, citations, errors and evidence.
- **CLI:** the terminal commands that select these behaviors.

Original passages are split within the mapped subject ranges, targeting 160 words with one-paragraph overlap. A long paragraph stays intact for source fidelity. NFKC normalization helps match styled Unicode text. A small explicit Chinese-to-English topic dictionary supports terms such as natural monopoly and hedging; it is not multilingual semantic retrieval. The same original text is returned, not normalized or paraphrased evidence.

Chat loads `prompts/persona.md` and retains the last four user/assistant pairs. Explicit notes/EEM subject references can trigger retrieval; hypothetical/drafting requests normally skip it, and `/notes` overrides routing. Ask receives neither history nor persona. Search stops after retrieval. Conversation is saved as labeled evidence but never promoted to original source material.

Citation validation detects unknown labels, including grouped labels such as [S1, S2], and rejects factual answers with no citation. This is structural validation, **not semantic proof or a guarantee that every sentence is cited**. Human source comparison remains necessary. If validation fails, the raw output is retained alongside a clear displayed failure. Saved drafts and logs remain outside the vault's searchable sources.

## Observed limitations and improvements

Gemma's first wiki drafts included real errors: hedge size became a currency amount, a two-part-tariff explanation reversed how consumer surplus sets the fee, and two adjacent carbon-policy phrases became “fuel switching price.” These were corrected against the originals and documented. The original source material itself also contains abbreviated or conflicting wording; the reviewed notes preserve those differences.

The first note-based chat answer left its last claim without a nearby citation. Citation instructions were tightened and that check rerun; both outputs remain. Chinese terminology and grouped citation parsing were also improved and checked. Passing four questions does not imply broad accuracy.

Next improvements would be a larger paraphrase/abstention benchmark, stricter claim-level citation checks, and locally verified OCR for image-only material. A local embedding model is an option if keyword retrieval misses paraphrases, but would require a new download, memory measurement and offline demonstration.

## Offline demonstration — reviewed and recorded

The [second recording](evidence/offline/20260930T042106Z/offline-demo.mov) and [review with timestamps, stills and offline evidence cards](evidence/offline/20260930T042106Z/REVIEW.md) document the complete local demonstration. The first take remains documented as a presentation failure; its movie is not included. The instructions below reproduce the successful run.

See the [step-by-step recording guide](OFFLINE-RECORDING.md). Finish all setup downloads first. Quit the CLI, turn off Wi-Fi and disconnect Ethernet/hotspots, then start a recording showing disconnected network state and Terminal. Double-click [offline-demo.command](offline-demo.command) or run:

```sh
./offline-demo.command
```

The prepared script records help, device information, local Word ingestion/regeneration, all four fixed EEM questions, capability chat, drafting/follow-up, raw search, ask/history isolation and re-ingestion. Every command starts a new CLI process. It saves terminal output and `scutil --nwi` network information under `evidence/offline/<timestamp>/`. The script does not disconnect the computer or automatically certify disconnection. Pair it with an actual screen recording/screenshots, then review the results and newly generated pages. Reconnect afterward.

## Obsidian demonstration — verified

The vault was opened in Obsidian 1.13.7. The actual walkthrough followed **index → Natural Monopoly Regulation → Tax and Price Controls → Quiz 2 reading copy → unchanged Word original**. Word opened the exact `vault/raw/EEM Quiz 2 Cheat Sheet.docx` file. No original content was edited.

- [Open note with source references and related links](evidence/obsidian/note-final.png)
- [Topic-organized index](evidence/obsidian/index-final.png)
- [Graph of all twelve topic pages](evidence/obsidian/graph-final.png): `path:wiki/`, Attachments off
- [Source text and preserved figures](evidence/obsidian/source-trace.png) and [original opened in Word](evidence/obsidian/original-opened.png)

The [walkthrough record](evidence/obsidian/README.md) documents what was observed. Earlier screenshots remain available. The [fresh-copy check](evidence/resume-verification.json) reconfirmed 11 tests, 95 unambiguous wiki links, all original hashes and image bytes, full indexed text coverage, and unchanged re-ingestion without rerunning Gemma or the completed offline demonstration.

## Submission status

- [x] Local Gemma, own CLI/harness, four unchanged originals and twelve reviewed linked pages.
- [x] Three answerable questions, one insufficient-evidence case, chat/search checks, Chinese check and exact saved outputs.
- [x] Source extraction, source hashes, link checks, code tests and no-duplicate re-ingestion.
- [x] Obsidian screenshots and actual navigation check.
- [x] Physical offline recording and review of its actual outputs.
- [x] Review the wiki drafts regenerated during the offline run.
- [x] Owner confirmed public sharing of all four EEM documents and embedded figures.
- [x] Dedicated public repository published; anonymous access and all 265 initially published files verified.
- [ ] Submit the public repository URL through the course portal (portal URL still needed).

All authored project documentation is in English. Original bilingual source excerpts and exact model outputs are preserved as evidence, not translated replacements.

The owner-approved EEM submission is published at [jennawang1121/eem-personal-wiki](https://github.com/jennawang1121/eem-personal-wiki). See the [recovery audit](evidence/RESUME-AUDIT.md) for the completed requirement map. The earlier AI-learning corpus is backed up outside this project under `../archive/personal-wiki-ai-learning-20260929/` and is not part of the EEM submission.
