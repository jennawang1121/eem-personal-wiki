# EEM evidence review

All observations below refer to actual local Gemma outputs and the four supplied EEM documents. Original Word files are unchanged. This is a source-faithfulness review by the coding assistant; it is not an independent textbook accuracy audit or a claim of instructor approval.

## Four fixed research questions

1. **Future commodity purchase:** Gemma answers long futures and links this to fear of a price increase. Quiz 1 paragraph 28 and Final paragraphs 53–54 support the claims. The cited S2 passage is the Final sheet, while retrieval also includes the expected Quiz 1 evidence.
2. **Natural monopoly at marginal-cost pricing:** Gemma says fixed costs are not recovered and profit equals minus fixed cost. The cited Quiz 2 paragraphs 38–43 include the stated model C = F + cQ and the result. This is the notes' model, not an unrestricted claim about all businesses.
3. **LCOE limitations:** Gemma names time, location and dispatchability, and says electricity is treated as equally valuable. Both cited source ranges support this. The answer repeats the list once, a minor concision issue preserved in the actual output.
4. **Exam date and classroom:** The sources do not supply either detail. Gemma reports insufficient evidence even though retrieval finds exam-related text.

Each test's expected original excerpt was found in retrieved context. Each research answer passed label validation; the answer content was separately compared against the original evidence. The JSON files preserve all source labels and exact output.

## Mode checks

Both capability prompts avoided retrieval and gave a conversational explanation. A suggested three-step study plan was followed by “make that shorter,” which condensed the preceding plan. The hypothetical $999 project budget stayed within chat; standalone ask reported insufficient evidence.

Search returned original passages without loading the model. Explicit `/notes` retrieved LCOE evidence. Its first answer included a final factual statement without a nearby citation; the persona was tightened and that check rerun. The rerun cites both the three limitations and the statement about market-price inputs. Both versions are retained.

The first Chinese answer used an imprecise translation of dispatchability; the prompt now supplies the more precise Chinese technical term. The Chinese rerun uses that term and cites [S1, S2]. Grouped citations are parsed and tested so an invalid label cannot hide within a group.

## Wiki review and corrections

Gemma produced twelve topic drafts. The original generation responses remain in the ingestion JSON, and pre-review page versions are in `previous-pages/`. Reviewed pages correct the following observed problems:

- Futures and Hedging incorrectly described hedge size as an amount of currency; the source's example is 530,000 MMBTU short.
- Natural Monopoly Regulation reversed the relationship between consumer surplus and the maximum fixed fee; it now follows the source.
- Carbon Markets merged “fuel switching” and “price usually increases” into a nonexistent “fuel switching price.” The phrases are now separated.
- Energy Efficiency introduced “maintenance,” which was absent from the landlord investment example; this was removed.
- Auction pay/receive wording, capacity/capacity-factor wording, rebound headings, and gas-price/build-cost wording differ across the originals. Reviewed notes preserve those distinctions.
- Abbreviated formulas and example assumptions are attributed to the notes rather than presented as universally established results.
- A formatting bug rendered paragraph-range lists as wiki links. Ranges now use plain text, so no numeric graph nodes are created.

The originals themselves were not corrected. These observed failures show why ingestion needs review even when the four ask tests pass.

## Extraction and images

All text in document.xml is read in paragraph order, including table cells and inline text formulas. The Final sheet uses tables for its column layout; all 172 table paragraphs are extracted. Paragraph numbers are not page numbers. Four reading copies provide exact paragraph text and all 22 original embedded images. Images are preserved unchanged and not indexed; no OCR is claimed. Questions requiring figure-only values remain outside the verified scope.

The full Quiz 2 and Final pages were rendered and inspected, and all embedded-image thumbnails were inspected. The raw documents were not edited or re-exported. See extraction and vault-validation reports for structural checks.

## Post-offline review

All twelve pages regenerated in the accepted offline run were compared again with their mapped original source paragraphs. The repeated hedge-unit, tariff, carbon phrase and landlord-example errors were corrected; source disagreements were preserved. Additional wording distinguishes an individual price-taking firm from a market, and attributes the tax-slope formula to the notes rather than independently endorsing its convention. Current pages are marked reviewed. Exact regenerated drafts are preserved in `post-offline-drafts/`, with source ranges and before/after hashes in [post-offline-review.json](post-offline-review.json). Re-ingestion preserves the reviewed bytes.

## Submission status

Public sharing was explicitly authorized. The [accepted offline recording](offline/20260930T042106Z/REVIEW.md) and source review are complete. The remaining app walkthrough and publication status are tracked in [SUBMISSION.md](../SUBMISSION.md).
