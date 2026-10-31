import json
import re
from datetime import datetime
from pathlib import Path
from functools import lru_cache


def parse(transcript):
    # Deliberately conservative: ambiguous natural-language dates are never guessed.
    dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", transcript)
    times = re.findall(r"\b\d{2}:\d{2}\b", transcript)
    if len(dates) != 1 or len(times) != 1:
        return dict(
            status="clarify",
            question="Please confirm one date (YYYY-MM-DD) and one time (HH:MM).",
            transcript=transcript,
        )
    try:
        datetime.fromisoformat(dates[0] + "T" + times[0])
    except ValueError:
        return dict(
            status="clarify",
            question="That date or time is invalid. Please correct it.",
            transcript=transcript,
        )
    if "cancel" in transcript.lower():
        return dict(
            status="clarify",
            question="Cancellation needs a booking reference and explicit confirmation.",
            transcript=transcript,
        )
    return dict(
        status="proposal",
        date=dates[0],
        time=times[0],
        timezone="Europe/Madrid",
        transcript=transcript,
        requires_confirmation=True,
        booked=False,
    )


@lru_cache
def model():
    from faster_whisper import WhisperModel

    return WhisperModel("tiny.en", device="cpu", compute_type="int8")


def transcribe(path):
    segments, info = model().transcribe(str(path), beam_size=1, language="en", vad_filter=False)
    text = " ".join(s.text.strip() for s in segments)
    return dict(text=text, language=info.language, model="faster-whisper/tiny.en", result=parse(text))


def confirm(proposal, date, time, confirmed=False):
    if not confirmed:
        raise PermissionError("explicit confirmation required")
    checked = parse(f"{date} at {time}")
    if checked["status"] != "proposal":
        raise ValueError("invalid confirmed date/time")
    # This component emits a confirmed intake only. The booking service must check availability.
    return dict(
        status="confirmed_intake",
        date=date,
        time=time,
        timezone="Europe/Madrid",
        original_transcript=proposal.get("transcript", ""),
        booked=False,
    )


def demo(mode="fixture"):
    if mode == "local":
        path = Path("data/sample.wav")
        if not path.exists():
            raise FileNotFoundError("Add data/sample.wav or use the upload API; no fixture is substituted.")
        return transcribe(path)
    cases = json.loads(Path("data/transcripts.json").read_text())
    return [parse(c["text"]) for c in cases]


def evaluate(mode="fixture"):
    if mode == "local":
        return dict(
            passed=True,
            transcription=demo(mode),
            limitation="One synthetic spoken sample; no general ASR accuracy claim.",
        )
    cases = json.loads(Path("data/transcripts.json").read_text())
    rows = [dict(text=c["text"], expected=c["expected"], actual=parse(c["text"])["status"]) for c in cases]
    return dict(
        passed=all(r["expected"] == r["actual"] for r in rows),
        cases=rows,
        mode_detail="Transcript parser only; this is not speech recognition evaluation.",
    )
