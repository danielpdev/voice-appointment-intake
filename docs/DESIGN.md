# Design record

## Decision

A local Whisper model transcribes audio. A conservative parser extracts unambiguous date/time inputs or requests clarification. Even confirmed intake is not a booking; availability belongs to a separate booking service.

## Failure model

Invalid dates/times, ambiguous multiple dates, missing confirmation and the distinction between confirmed intake and a booked appointment. A synthetic spoken sample was transcribed locally.

## Tradeoffs

The bundled audio is synthetic macOS speech, not a human recording. English-only tiny.en and a conservative date parser are small baselines. No telephony integration, diarization or voice cloning is included.

## Next change to defend in review

Add time-zone selection and a larger consented ASR/date-extraction evaluation set.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
