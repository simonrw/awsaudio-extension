from flask import Flask, request

import math  # import needed modules
import random
import pyaudio  # sudo apt-get install python-pyaudio


scale_notes = {
    # pitch standard A440 ie a4 = 440Hz
    "c": 16.35,
    "C": 17.32,
    "d": 18.35,
    "D": 19.45,
    "e": 20.6,
    "f": 21.83,
    "F": 23.12,
    "g": 24.5,
    "G": 25.96,
    "a": 27.5,
    "A": 29.14,
    "b": 30.87,
}


def playnote(note, note_style):
    octave = int(note[1])
    frequency = scale_notes[note[0]] * (2 ** (octave + 1))

    p = pyaudio.PyAudio()  # initialize pyaudio

    # sampling rate
    sample_rate = 22050

    LENGTH = random.uniform(0.1, 0.3)

    frames = int(sample_rate * LENGTH)

    wavedata = ""

    # generating waves
    stream = p.open(format=p.get_format_from_width(1), channels=1, rate=sample_rate, output=True)
    for x in range(frames):
        wave = math.sin(x / ((sample_rate / frequency) / math.pi)) * 127 + 128

        if note_style == "bytwos":
            for i in range(3):
                wave += (
                    math.sin((2 + 2**i) * x / ((sample_rate / frequency) / math.pi)) * 127 + 128
                )
            wavedata = chr(int(wave / 4))

        elif note_style == "even":
            for i in range(3):
                wave += (
                    math.sin((2 * (i + 1)) * x / ((sample_rate / frequency) / math.pi)) * 127 + 128
                )
            wavedata = chr(int(wave / 4))

        elif note_style == "odd":
            for i in range(3):
                wave += (
                    math.sin(((2 * i) + 1) * x / ((sample_rate / frequency) / math.pi)) * 127 + 128
                )
            wavedata = chr(int(wave / 4))

        elif note_style == "trem":
            wave = wave * (1 + 0.5 * math.sin((1 / 10) * x * math.pi / 180)) / 2
            wavedata = chr(int(wave))

        else:
            wavedata = chr(int(wave))

        stream.write(wavedata)

    stream.stop_stream()
    stream.close()
    p.terminate()


app = Flask(__name__)

hashed_notes = {}


@app.route("/", methods=["POST"])
def index():
    payload = request.get_json()
    service = payload["service"]

    print("PLAYING NOTE")

    if service not in hashed_notes:
        note = random.choice(list(scale_notes.keys()))
        octave = random.choice([3, 4])
        hashed_notes[service] = (note, octave)

    note, octave = hashed_notes[service]
    playnote((note, octave), "bytwos")
    return "ok"
