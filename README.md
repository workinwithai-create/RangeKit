# RangeKit

**Does your song feel flat, strained or mumbly when you sing it? Usually the problem is the key, not your voice. Sing your lowest and highest notes, and RangeKit scores all 12 keys against *your* range. It shows why each key works or doesn't, then plays the band in the key that fits so you can A/B it before you record.** Live: **https://rangekit.vercel.app**

Songwriters ask this all the time ("how do I pick the key to record in?", "my record sounds flat because the key doesn't sit in my range"). The usual answer is "sing it in a few keys and see". RangeKit does that for you, with numbers and a real band.

## How it works
1. **Your song:** BPM 60–180, the key it's written in, 4 chords (one per bar, looped over 4/8/16 bars) and a band (Ballad 68, Pop 92, Folk 100, Sparse 80). These are yours. RangeKit only *suggests* a key from your chords and melody and never overrides it. Everything is saved in your browser.
2. **Your voice:** start from a preset (Bass, Baritone, Tenor, Alto, Mezzo, Soprano), then set your own:
   - lowest comfortable note
   - highest comfortable note
   - belt top (the note you can hit on a good day)

   Set each one by **singing it** (mic, YIN pitch tracking, it shows the note and cents), by **pressing it on your MIDI keyboard**, or by picking it. "Hear" plays the note on a real sampled piano.
3. **Your melody:**
   - Record it on a MIDI keyboard or the on-screen/computer keys, or sing it into the mic. Each loop pass becomes a take, and partial takes are kept.
   - Or import a voice memo (WAV/MP3/M4A) or a .mid file, or load the demo ("High Road", an original 8-bar line spanning E4–A5).
   - Takes remember the key you heard while recording, so the written melody stays correct.
4. **Key fit:**
   - Every key is tried in its best octave and scored 0–100. Points come off for notes below your floor, above your comfortable top, and especially above your belt top. Too many notes near the edges also costs points, and so does the melody's centre sitting far from your sweet spot.
   - The range ladder draws your range, your belt zone and the melody in the original key and in your key.
   - The fit card names the best key and two runners-up, and explains why (lowest/highest note vs. your range, % of notes in the sweet spot). It also lists the chords in that key and a capo shape for guitar.
   - Nothing changes until **you** pick a key (click a key, use "Sing in", or press the "Sing in Bb major" button). Octave up/down buttons cover melodies an octave away.
5. **Listen:** the band (real samples) plus a guide melody (choir, piano, cello, flute, EP or nylon), or your recorded voice when it was sung in that key.
   - **A/B at matched loudness:** A = original key (Thin), B = your key (Need).
   - Live changes (key, chords, band, mutes, BPM, A/B) land on the next step without a restart.
6. **Export in your key:**
   - 48 kHz / 24-bit stereo WAV at the exact loop length (downbeat at sample 0, tail folded in, peak ≤ −1 dBFS).
   - Type-1 MIDI with tempo, 4/4, key signature, a chord marker per bar, band tracks, a chord-block track and the melody in your key.
   - A **key sheet** (.txt): the key to sing in, the transposed chords, a capo shape, and the fit table for all 12 keys.
   - A stems ZIP with every part, every take and your raw voice.
   - Files are named `rangekit-<band>-<bpm>bpm-<key>.wav/.mid`. On iPhone/iPad, exports open the share sheet ("Save to Files").

## Inputs and outputs
- **Web MIDI in:** velocity and sustain pedal (CC64). Notes never start the transport. **Web MIDI out:** the band mirrors to your synth.
- Audio input select (your mic/interface) and audio output select (`setSinkId`, with a fallback note).
- Hear-myself monitoring, latency fix slider, click (the kit's real cross-stick sample).
- Stops cleanly when the tab is hidden. On iPhone, turn off the silent switch.

## Sounds (real samples only)
- FluidR3_GM (MIT), pinned to gleitz/midi-js-soundfonts commit `044fab8e1456bfafc5776e86dfd6bb8697149aef` on jsDelivr, with raw.githubusercontent at the same commit as a fallback.
  - Instruments: piano, electric piano, finger bass, strings, nylon guitar, flute, cello, choir aahs.
  - One sample every 4 semitones, so pitch shift is at most ±2 (the engine refuses anything beyond ±4). Looped sustain, attack ramps and ≥10 ms releases.
- Virtuosity Drums acoustic kit (CC0), bundled in `public/samples/drums`.
- There are no oscillators or noise anywhere (`qa/no_synth.sh`). If a sample host is blocked, the app names the missing instruments and keeps playback and export off.
- Full credits: [public/samples/CREDITS.md](public/samples/CREDITS.md).

## Pricing
- **Launch (no Lemon Squeezy product configured yet):** everything is free at every length ("Checkout opening soon"; "Launch: full exports free until checkout opens"). Gating turns on only when `LEMON.storeId` and `LEMON.productId` are set. An empty gate never blocks anyone.
- **Free (once checkout is live):** set your range, score all 12 keys, A/B, record, play, and export WAV, MIDI and the key sheet up to 8 bars.
- **RangeKit license: $19 once** (no subscription). It unlocks 16-bar exports and the stems ZIP. License keys are checked with the Lemon Squeezy License API, and only keys for this `storeId`/`productId` are accepted.
- **Why one-time:**
  - You set your range once and use it for every new song. It's a tool, not a service.
  - It runs entirely in the browser, so there are no per-user server or AI costs.
  - It matches the other WorkinWithAI desks ($19 once).
- **Where to sell:** Lemon Squeezy (license keys, merchant of record for VAT/sales tax). Gumroad works too for a one-time sale. Bandcamp only makes sense bundled with a sample pack.

## Run locally
`npm run build` copies the static files into `dist/`. Serve `dist/` with any static server (`python3 -m http.server -d dist`).

## QA
- `qa/s9.py <url>`: AUDIO-ENGINE-RULES §9 checks 1–7. It also covers key fit by voice type, range input (MIDI + mic), recording, import, MIDI files in your key, the key sheet, MIDI in/out, A/B loudness, stems, persistence and the license gate.
- `qa/export_test.py <url>`: downloads through the real buttons, plus the iOS share-sheet path.
- `qa/no_synth.sh [url]`: the no-synth audit.
- `qa/fixtures/ode-flute-92bpm-C-mono16.wav` is a sampled-flute WorkinWithAI desk export (Ode to Joy, public domain), used as a "voice memo" and as the fake mic.

No accounts, no database, no tracking. © 2026 WorkinWithAI.
