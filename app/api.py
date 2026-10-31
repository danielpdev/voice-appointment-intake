import tempfile
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel, Field
from app.core import parse, confirm, transcribe

app = FastAPI(title="Voice appointment intake")


class Transcript(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


class Confirmation(BaseModel):
    proposal: dict
    date: str
    time: str
    confirmed: bool = False


@app.post("/api/parse")
def parse_text(b: Transcript):
    return parse(b.text)


@app.post("/api/confirm")
def confirmation(b: Confirmation):
    try:
        return confirm(**b.model_dump())
    except PermissionError as e:
        raise HTTPException(403, str(e)) from e
    except ValueError as e:
        raise HTTPException(422, str(e)) from e


@app.post("/api/transcribe")
async def audio(file: UploadFile):
    body = await file.read(10_000_001)
    if len(body) > 10_000_000:
        raise HTTPException(413, "Maximum audio size is 10 MB")
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "audio.wav"
        p.write_bytes(body)
        try:
            return transcribe(p)
        except Exception as e:
            raise HTTPException(422, "Audio could not be transcribed") from e
