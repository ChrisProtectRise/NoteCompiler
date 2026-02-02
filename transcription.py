import whisper


def transcribe_wav(filename: str) -> str:
    model = whisper.load_model("large")  # tiny / base / small / medium / large
    result = model.transcribe(filename, language = "en", fp16 = False)
    return result["text"]


if __name__ == "__main__":
    transcribed_text = transcribe_wav("recording-2026-01-25_15-29-21.wav")
    print(transcribed_text)