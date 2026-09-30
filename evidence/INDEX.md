# Evidence index

These are actual runs against the four EEM Word documents using local `mlx-community/gemma-4-e2b-it-4bit`, snapshot `238767527555cb75a05732a84dff5d6ba0dd6809`. The saved runtime forces local model loading and has no cloud fallback. **The second offline recording is reviewed and accepted for the demonstration requirement.** Start with the [movie, timestamped review, four offline ask cards and mode checks](offline/20260930T042106Z/REVIEW.md). The initial runs listed below predate that attempt.

All authored explanations are in English. Quoted source passages and historical model outputs retain their original language to preserve evidence.

## Four standalone ask tests

### Test 1

**Question:** According to the notes, should someone buying a commodity in the future hedge with long or short futures?

**Actual answer:** If there is future exposure to buying a commodity, one should hedge with long futures [S2]. This is done to mitigate the risk of a price rise [S2].

**Assessment:** Supported: Final paragraphs 53–54; Quiz 1 paragraph 28 also retrieved.

[Exact passages and citations](runs/20260929T234135-ask-1.md) · [Settings and measurements](runs/20260929T234135-ask-1.json)

Generation: 1.40 seconds.

### Test 2

**Question:** According to the notes, why can a natural monopoly lose money when the regulated price equals marginal cost?

**Actual answer:** When the regulated price equals marginal cost, the firm cannot cover its fixed costs [S3]. This results in a loss because the profit is less than zero, specifically equal to the negative of the fixed cost [S3].

**Assessment:** Supported by the cost model in Quiz 2 paragraphs 38–43.

[Exact passages and citations](runs/20260929T234135-ask-2.md) · [Settings and measurements](runs/20260929T234135-ask-2.json)

Generation: 1.30 seconds.

### Test 3

**Question:** According to the notes, which three aspects of electricity value are ignored by LCOE?

**Actual answer:** LCOE ignores time, location, and dispatchability [S1]. This means all electricity is treated as equally valuable [S1]. The limitation states that LCOE ignores time, location, and dispatchability [S2].

**Assessment:** Supported: time, location and dispatchability. Minor repetition retained.

[Exact passages and citations](runs/20260929T234135-ask-3.md) · [Settings and measurements](runs/20260929T234135-ask-3.json)

Generation: 1.25 seconds.

### Test 4

**Question:** What is the exact date and classroom for the EEM final exam?

**Actual answer:** Insufficient evidence in the indexed sources. The provided evidence does not contain the exact date and classroom for the EEM final exam.

**Assessment:** Correct abstention: no source supplies the exact date or classroom.

[Exact passages and citations](runs/20260929T234135-ask-4.md) · [Settings and measurements](runs/20260929T234135-ask-4.json)

Generation: 0.81 seconds.

## Conversation and mode boundaries

| Check | Saved actual output | Assessment |
|---|---|---|
| “What can we do?” | [Capability chat](runs/20260929T234135-chat-1.md) | Conversational; no retrieval |
| “What can you help me with?” | [Second capability chat](runs/20260929T234135-chat-2.md) | Commands explained; no retrieval |
| Study plan | [Plan](runs/20260929T234135-chat-3.md) | Uses chat mode |
| “Make that shorter” | [Follow-up](runs/20260929T234135-chat-4.md) | Uses preceding conversation |
| Hypothetical budget | [Drafting](runs/20260929T234135-chat-5.md) | Chat-only premise |
| Ask/history separation | [Standalone ask](runs/20260929T234135-ask-isolation.md) | Does not adopt the hypothetical budget as evidence |
| Raw retrieval | [Search](runs/20260929T234135-search.md) | Original passages, no generated answer |
| Notes in chat | [Targeted rerun](runs/20260929T234453-chat-notes.md) | Claims have nearby source labels after prompt correction |
| Optional bilingual check | [Targeted rerun](runs/20260929T234453-ask-chinese.md) | Improved terminology; original output retained |
| Re-ingestion | [Run](runs/20260929T234135-reingestion.md) | No duplicate topic pages |

## Ingestion, provenance and review

- [Twelve-topic ingestion](runs/20260929T234040-37e7a7.md) and [full ingestion transcript](ingestion-transcript.txt).
- [Initial evaluation transcript](evaluation-transcript.txt), [follow-up transcript](followup-rerun.txt), and [latest record manifest](latest-evaluation.json).
- [Source-faithfulness review](REVIEW.md) and [wiki corrections](wiki-review.json). Initial failures remain in the saved records.
- [Original file hashes](../documents.json), [extraction report](extraction-report.json), and [source catalog](../vault/Source%20Catalog.md).
- [Device snapshot](device-transcript.txt), [model manifest](model-manifest.json), [unit tests](unit-tests.txt), and [vault validation](vault-validation.json).
- [Obsidian walkthrough status](obsidian/README.md) and [remaining submission steps](../SUBMISSION.md).

The coding assistant compared material answer claims with the supplied sources. The regenerated wiki drafts have also been source-reviewed; see [post-offline review](post-offline-review.json). Owner review remains welcome. Structural citation validation alone does not establish semantic correctness.
