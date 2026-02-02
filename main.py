from transcription import transcribe_wav
from record import Microphone


def write_file(file_name: str, text: str) -> None:
    with open(file_name, 'w') as f:
        f.write(text)


def main() -> None:
    mic = Microphone()
    filename = mic.handle_recording_phase()
    transcribed_text = transcribe_wav(filename)
    print(f"Transcription: {transcribed_text}")
    write_file(f"transcription-{filename[:-4]}.txt", transcribed_text)


if __name__ == "__main__":
    main()
