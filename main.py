import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
from tkinter import *
from tkinter.filedialog import askopenfilename


types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

peak = 10
nframes = 10
duration = 10
k = 10

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)


def clicked_open():
    global  filename
    filename = askopenfilename()
    l_file.configure(text="Выбран файл" +  filename)
    wav = wave.open(filename, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    duration = nframes / framerate
    w, h = 800, 300
    k = nframes / w / 32
    DPI = 72
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.frombuffer(content, dtype=types[sampwidth])

    plt.figure(1, figsize=(float(w) / DPI, float(h) / DPI), dpi=DPI)
    plt.subplots_adjust(wspace=0, hspace=0)

    for n in range(nchannels):
        channel = samples[n::nchannels]

        channel = channel[0::(round(k))]
        if nchannels == 1:
            channel = channel - peak

        axes = plt.subplot(2, 1, n + 1, facecolor="lavender")
        axes.plot(channel, "peru")
        axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
        plt.grid(True, color="r")
        axes.xaxis.set_major_formatter(ticker.NullFormatter())

    plt.savefig("wave", dpi=DPI)
    plt.show()

br = "silver"
window = Tk()
window.title("Mp3 -> Img")
window.geometry('800x400')
window["bg"] = br

l_find_file = Label(window, text="Выберите музыкальный файл в формате wav", font=("Comic Sans MS", 14, "bold"), bg=br)
l_find_file.pack()
filename = "music.wav"
b_find_file = Button(window, text="Выбрать файл", command=clicked_open, font=("Comic Sans MS", 14, "bold"), bg=br)
b_find_file.pack()
l_file = Label (window, text="Файл не выбран", font=("Comic Sans MS", 14, "bold"), bg=br)
l_file.pack()

window.mainloop()
