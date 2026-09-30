# Offline demonstration — accepted take 2

**The recording and matching logs support the assignment’s offline demonstration requirements. This is an assistant review against the assignment, not an instructor grade or confirmation that the entire submission is complete.

[Watch the submission movie](offline-demo.mov) · [Terminal transcript](terminal.txt) · [Network snapshot](network-state.txt) · [Provenance and hashes](review-manifest.json)

## What is visible

| Approximate movie time | Evidence | Assessment |
|---|---|---|
| 00:15–00:20 | Wi-Fi switch visibly OFF before the Return prompt is released | Clear visual disconnection; launch snapshot also reports no IPv4/IPv6 states and Not Reachable |
| 00:45 onward | Help, doctor, local model identifier and fresh ingestion command | Original CLI runs after disconnection; model is `mlx-community/gemma-4-e2b-it-4bit` |
| 01:20–01:40 | Ingestion output, original-source search and four ask tests | Actual command sequence, citations and source paths visible; complete passages retained in evidence cards |
| 01:40–01:55 | Capability chat, study plan, shorter follow-up, hypothetical budget and standalone ask | Chat uses history; ask refuses to treat the hypothetical budget as source evidence |
| 01:55–02:05 | Re-ingestion result and Finished message | Twelve topic pages preserved without duplicate regeneration; script reaches completion |

Terminal stays in front during the required sequence. Text is readable at the original 2940 × 1912 resolution; pause or open the linked stills/transcript for comfortable reading. No narration is required, and the original has no audio track. Chat inputs are piped by the demonstration script: they are visible in the printed command and individual evidence cards, although each `You:` line itself is blank in the terminal transcript.

## Actual questions and source review

1. [Future commodity purchase](../../runs/20260930T042151-82f50e.md): long futures to prepare for a price rise. Cited Final-sheet passage explicitly supports both claims.
2. [Natural monopoly](../../runs/20260930T042154-6ee8b7.md): marginal-cost pricing does not recover fixed cost in the supplied model, yielding profit −F. Cited Quiz 2 paragraphs 38–43 support the explanation.
3. [LCOE](../../runs/20260930T042158-5f3866.md): time, location and dispatchability are ignored. Both cited passages support the answer. Minor repetition remains in the actual output.
4. [Exam schedule](../../runs/20260930T042201-7496a3.md): insufficient evidence for the exact date and classroom. This is the expected result.

[Raw search](../../runs/20260930T042147-afc108.md) returns original passages. [First capability chat](../../runs/20260930T042206-f5788e.md) and [second capability chat](../../runs/20260930T042209-8ccb5b.md) respond conversationally without unnecessary citations. The [plan](../../runs/20260930T042212-de2399.md) is shortened in the [follow-up](../../runs/20260930T042214-d84bb2.md). The [hypothetical budget](../../runs/20260930T042215-e7c9fb.md) remains chat context: [standalone ask](../../runs/20260930T042218-6259c6.md) returns insufficient evidence.

[Initial regeneration](../../runs/20260930T042146-86891c.md) uses the local model. [Final re-ingestion](../../runs/20260930T042218-e78d6c.md) preserves all twelve pages. The saved transcript contains no traceback and matches the recorded output.

## Stills from the actual movie

- [Wi-Fi off](wifi-off.png)
- [Help, device information and ingestion](help-device-ingestion.png)
- [Search and ask](search-and-ask.png)
- [Four questions](four-questions.png)
- [Chat and follow-up](chat-followup.png)
- [Finished](finished.png)

## Editing and review limits

The original Desktop movie is 2:21.37 and remains unchanged. The submission copy retains the continuous first 2:05, including setup, disconnection, all execution and the Finished screen. Only the trailing notification/recording-control portion was removed; no commands, outputs or intermediate steps were cut or rearranged. Export used passthrough without re-encoding. Frames at 00:20 and 01:40 are pixel-identical to the original, and the exported 02:04 completion frame was inspected.

Review used 30 overview frames, selected full-resolution frames, saved logs and source comparison, rather than continuous real-time playback. The network snapshot measures launch-time state; the visible disconnection, recorded sequence and local-only harness together support this demonstration. No packet capture or separate network audit is claimed.

The first take’s review remains preserved as a real presentation failure, but its private movie is excluded from submission. The second run regenerated wiki drafts; [subsequent source review](../../post-offline-review.json) is now complete. Required Obsidian screenshots and public repository/portal submission are separate remaining work.
