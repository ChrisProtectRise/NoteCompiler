from summary import generate_summary
from transcription import transcribe_wav
from record import Microphone


def write_file(filename: str, text: str) -> None:
    with open(filename, 'w') as f:
        f.write(text)


def main() -> None:
    mic = Microphone()
    folder_name, filename = mic.handle_recording_phase()

    transcribed_text = transcribe_wav(filename)
    write_file(f"{folder_name}/transcription.txt", transcribed_text)

    summary = generate_summary(transcribed_text)
    write_file(f"{folder_name}/summary.txt", summary)


if __name__ == "__main__":
    main()