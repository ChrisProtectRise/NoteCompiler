import os

import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime
import numpy as np


class Microphone:
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.recording = False
        self.audio_data = []
        self.stream = None

    def _start_recording(self) -> None:
        """Starts recording to a .wav"""
        print("--- Recording started ---")
        self.audio_data = []  # Clear previous data
        self.recording = True

        # Define the callback to capture audio chunks
        def callback(indata, frames, time, status):
            if status:
                print(status)
            if self.recording:
                self.audio_data.append(indata.copy())

        # Open the input stream
        self.stream = sd.InputStream(samplerate = self.sample_rate,
                                     channels = 1,
                                     dtype = 'int16',
                                     callback = callback)
        self.stream.start()

    def _stop_recording(self) -> tuple[str, str]:
        """Stop the recording and return the filename of the recorded audio"""
        if not self.recording:
            raise Exception("Not currently recording; can't call _stop_recording")

        self.recording = False
        self.stream.stop()
        self.stream.close()

        # Combine all captured chunks into one array
        full_audio = np.concatenate(self.audio_data, axis = 0)

        # Generate filename with timestamp
        folder_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.mkdir(folder_name)
        filename = f"{folder_name}/recording.wav"

        write(filename, self.sample_rate, full_audio)
        print(f"--- Recording finished: {filename} ---")
        return folder_name, filename

    def handle_recording_phase(self):
        """Start recording, wait for stop signal, then return filename of recorded audio"""
        self._start_recording()
        input("Press Enter to stop recording...")
        filename = self._stop_recording()
        return filename
