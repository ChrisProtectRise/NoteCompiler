from transcription import transcribe_wav
from record import Microphone


if __name__ == "__main__":
    mic = Microphone()
    filename = mic.handle_recording_phase()
    transcribed_text = transcribe_wav(filename)
    print(f"Transcription: {transcribed_text}")