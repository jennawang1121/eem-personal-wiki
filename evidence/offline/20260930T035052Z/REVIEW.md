# Offline recording review

## Verdict

**The recorded run completed, but this movie is not ready to use as the public offline demonstration. Re-record a short, focused Terminal demonstration.** The logs are useful and should be preserved; the incomplete visual demonstration must not be presented as a complete pass.

## Recording and review method

Reviewed the Desktop movie named `Screen Recording 2026-09-29 at 8.50.18 PM.mov` (the filename uses a narrow space before PM). Duration: 694.64 seconds (11:34.64). Resolution: 2940 × 1912. No audio track; narration is not required by the assignment.

The review extracted 79 frames and inspected 50 overview frames (every five seconds through the first 150 seconds, every 30 seconds afterward, and the ending), plus six selected transition frames at larger size. Findings were cross-checked against the terminal transcript and exact saved JSON records. This was a visual frame review, not continuous real-time playback. The original movie was not edited or uploaded. Private frame extracts remain outside the submission project.

## Findings

| Requirement | What the recording and logs show | Assessment |
|---|---|---|
| Visible internet disconnection before fresh CLI execution | Around 00:10–00:12, the Wi-Fi panel shows the switch enabled. The start-of-run network snapshot reports no IPv4 or IPv6 states and Not Reachable. No clear Wi-Fi-off transition was established from reviewed frames. | Logs support no reachable network at launch; visual evidence is incomplete. A single snapshot does not prove the network stayed disconnected throughout. |
| Help, model/device information and local ingestion | Around 00:34–00:40, Terminal shows help and doctor output. The ingestion command and full actual results are saved in the transcript. The Terminal window occupies only part of the screen and output moves quickly. | Execution supported by logs; presentation needs a larger, unobstructed Terminal. |
| Three factual ask tests, one unsupported test, search and chat boundaries | The saved run spans approximately 00:34–01:54 of the movie. During much of the important latter portion, Obsidian or other apps cover Terminal. The three factual answers, refusal, chat plan/follow-up and raw search all exist in the saved records. | Tests ran, but the movie does not clearly show the required command/output sequence. |
| Completed run | Around 04:25, Terminal is visible again showing the final saved record and Finished message. | Supports completion, but does not recover the hidden intermediate outputs. |
| Suitable public evidence | Personal messaging is visible behind early windows; later frames show email and unrelated personal browsing. | Do not publish the original movie. Cropping cannot recover Terminal output that was covered. |
| Obsidian evidence | A note, heading, source links and related links are visible. | Useful partial visual evidence, but the video does not establish the complete required index/graph/source-navigation walkthrough. |

## Actual saved test results

- [Question 1](../../runs/20260930T035139-4ce24a.md): long futures for a future commodity purchase. The cited Final-sheet passage explicitly supports the direction and price-rise rationale.
- [Question 2](../../runs/20260930T035144-51894f.md): marginal-cost pricing fails to recover fixed costs in the supplied cost model. Quiz 2 paragraphs 38–43 support the cited answer.
- [Question 3](../../runs/20260930T035148-5166f3.md): LCOE ignores time, location and dispatchability. Both cited passages support these claims; minor repetition remains in the actual answer.
- [Question 4](../../runs/20260930T035152-3ffc6a.md): insufficient evidence for the exact exam date and classroom, as expected.
- [Chat follow-up](../../runs/20260930T035207-557c03.md) shortens the preceding study plan; [standalone budget question](../../runs/20260930T035212-a3a008.md) does not import the hypothetical chat budget.
- [Terminal transcript](terminal.txt) reaches final re-ingestion with twelve unchanged pages and no traceback. [Network snapshot](network-state.txt) reports Not Reachable at launch.

The regenerating ingestion reset wiki pages to draft review status. That is expected behavior; the generated pages still require source review before the final submission.

## Minimal replacement recording

1. Close messaging/email windows and maximize Terminal. Increase text size until comfortably readable.
2. Launch `./offline-demo.command`, leaving it at the Return prompt.
3. Start recording; show the Wi-Fi switch visibly OFF and disconnect other internet connections.
4. Press Return in Terminal. Keep Terminal frontmost for the entire automatic run. Do not switch to Obsidian, chat, email or a browser.
5. Wait for Finished, leave it visible briefly, and stop recording before reconnecting or opening other apps.

The actual scripted run took about 80 seconds, so a focused replacement should take roughly two minutes including setup. Preserve errors if any occur. The assistant can then review the replacement and prepare the public evidence.
