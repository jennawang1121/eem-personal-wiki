# Record the offline demonstration

Everything needed for the current local run is already downloaded. Keep these steps open before disconnecting; the assistant connection may stop while the internet is off.

1. Open Terminal. Paste and run:

   ```sh
   cd "/Users/wangjenna/Documents/ChatGPT/AgenticAI_Class 2/personal-wiki"
   ./offline-demo.command
   ```

   The script waits at **Press Return when ready**. Do not press Return yet.
2. Enlarge Terminal so commands and answers are readable. Close unrelated private windows. Press **Shift–Command–5**, choose **Record Entire Screen**, set **Options → Save to → Desktop**, then click **Record**. Voice narration is optional.
3. While recording, open the Wi-Fi menu and switch Wi-Fi **off**. Disconnect Ethernet and any USB/hotspot internet connection. Leave the disconnected state visible briefly.
4. Return to Terminal and press **Return**. **Keep Terminal maximized and frontmost until the run finishes; do not switch apps or scroll during execution.** The script now launches fresh local CLI processes and runs help, device checks, Gemma ingestion, four questions, chat with a follow-up, raw search, history isolation and re-ingestion. Do not type during the automatic tests.
5. Wait until the script prints **Finished. Save the recording and reconnect.** The run should usually take a few minutes. If an error appears, keep that output, stop the recording and tell the assistant what happened; do not describe it as a successful run.
6. Click the **Stop Recording** button in the menu bar. Rename the saved Desktop movie to `EEM-offline-demo.mov`. Reconnect Wi-Fi afterward.
7. Tell the assistant the recording is ready and where it was saved. No upload is needed if it is on this Mac. The assistant will inspect the logs, review regenerated notes and place the movie with the evidence.

The script automatically saves the terminal transcript and network-state snapshot in `evidence/offline/<timestamp>/`. It does not switch off the network itself. The movie should show both the disconnection and the subsequent real local execution.

The run regenerates topic drafts and backs up earlier pages. The assistant must review the new pages afterward; this is expected and the original Word files are not changed.

Apple reference: [Record the screen on a Mac](https://support.apple.com/en-nz/102618).
