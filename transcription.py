import whisper


def transcribe_wav(filename: str) -> str:
    model = whisper.load_model("base")  # tiny / base / small / medium / large
    result = model.transcribe(filename, language = "en", fp16 = False)
    return result["text"]
