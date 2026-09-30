#!/bin/sh
set -eu
cd "$(dirname "$0")"
printf '\nTurn off Wi-Fi and disconnect Ethernet or hotspots first.\nStart a recording showing disconnected network state and Terminal.\nThis script does not switch off networking or certify disconnection.\nPress Return when ready: '
read -r answer
RUN=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p "evidence/offline/$RUN"
date -u > "evidence/offline/$RUN/network-state.txt"
/usr/sbin/scutil --nwi >> "evidence/offline/$RUN/network-state.txt" 2>&1
/usr/bin/script -q "evidence/offline/$RUN/terminal.txt" /bin/sh ./offline-steps.sh
printf '\nFinished. Save the recording and reconnect. Regenerated wiki pages need another source review.\n'
