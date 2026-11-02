#!/usr/bin/env bash
# Trims the screen capture and lays the app's exported WAV under it from the moment Play is pressed. Captions only: no voice-over, no generated audio.
set -euo pipefail; cd "$(dirname "$0")"
j(){ python3 -c "import json;print(json.load(open('marks.json'))['$1'])"; }
V=$(j video); S=$(j start); P=$(j play); A=$(j wav); D=$(python3 -c "print(int(round(($P-$S)*1000))+110)")
FONT=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf; OUT=${1:-rangekit-demo.mp4}
cap(){ echo "drawtext=fontfile=$FONT:text='$1':fontsize=34:fontcolor=white:box=1:boxcolor=0x0e1013cc:boxborderw=14:x=(w-text_w)/2:y=h-92:enable='between(t,$2,$3)'"; }
VF="$(cap 'Song feels strained when you sing it?' 0 2.1),$(cap 'Set your range: lowest, highest, belt top' 2.1 4.2),$(cap 'RangeKit scores all 12 keys for your voice' 4.2 8.4),$(cap 'Best: Bb major 99/100. Hear the band in your key' 8.4 13.0),$(cap 'Export WAV, MIDI and a key sheet in your key' 13.0 17.4),$(cap 'rangekit.vercel.app  -  \$19 once' 17.4 22)"
ffmpeg -loglevel error -y -ss "$S" -i "$V" -i "$A" -t 22 -map 0:v -map 1:a -af "adelay=$D|$D,apad" -vf "$VF,format=yuv420p" -r 30 -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart "$OUT"
ffprobe -v error -show_entries stream=codec_type,codec_name,duration -of compact "$OUT"
