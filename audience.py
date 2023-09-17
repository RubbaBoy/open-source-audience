import time
from threading import Thread

import openai
import pyaudio
import wave
import audioop
from pydub import AudioSegment

from dotenv import load_dotenv
import os

from joke_rater import joke_rater
from rating_responder import rating_responder
from speech_parser import parse_audio

"""
cursor parking lot
----



-----

"""

# listen to audio
# save file to mp3
# give it to whisper
# give whisper output to chatgpt
# play respective laughtrack (if applicable)

base_path = "output"


def create_file_name():
    return "output_%s" % int(time.time())


def start_listening():
    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=pyaudio.paInt16,
                           channels=1,
                           rate=44100,
                           input=True,
                           input_device_index=2,
                           frames_per_buffer=1024)

    frames = []
    silence_threshold = 500
    consecutive_silence = 0
    consecutive_silence_threshold = 40
    any_audio = False

    print('Listening!')

    while True:
        data = stream.read(1024)
        frames.append(data)

        # silence check
        rms = audioop.rms(data, 2)

        if rms < silence_threshold:
            consecutive_silence += 1
        else:
            any_audio = True
            consecutive_silence = 0

        if consecutive_silence > consecutive_silence_threshold:
            break

    stream.stop_stream()
    stream.close()
    py_audio.terminate()

    if any_audio:
        file_name = create_file_name()
        wav_name = f"{base_path}/{file_name}.wav"
        mp3_name = f"{base_path}/{file_name}.mp3"

        with wave.open(wav_name, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(py_audio.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(44100)
            wav_file.writeframes(b"".join(frames))

        audio = AudioSegment.from_wav(wav_name)
        audio.export(mp3_name, format="mp3")

        print(mp3_name)
        text = parse_audio(mp3_name)
        os.remove(wav_name)
        if text != '':
            Thread(target=execute_joke, args=[text]).run()

    Thread(target=start_listening).run()


def execute_joke(text):
    print(text)
    rating = joke_rater(text)
    print(rating)
    rating_responder(rating)


def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(create_file_name())
    start_listening()


if __name__ == '__main__':
    main()
