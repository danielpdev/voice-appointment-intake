# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

A local Whisper model transcribes audio. A conservative parser extracts unambiguous date/time inputs or requests clarification. Even confirmed intake is not a booking; availability belongs to a separate booking service.

## Failure case to discuss

Invalid dates/times, ambiguous multiple dates, missing confirmation and the distinction between confirmed intake and a booked appointment. A synthetic spoken sample was transcribed locally.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

The bundled audio is synthetic macOS speech, not a human recording. English-only tiny.en and a conservative date parser are small baselines. No telephony integration, diarization or voice cloning is included.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
