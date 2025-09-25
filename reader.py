from os.path import dirname, join as pjoin
from scipy.io import wavfile
from scipy.fft import *
import numpy as np
import matplotlib.pyplot as plt

#data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
#print(data_dir)

#TODO
# 1. determine bpm of file/ask user
# 2. assume 32nd notes are smallest, use that to calculate frequency sample size
# 3. assemble array of frequencies vs times
# 4. translate into guitar notes (maybe check tuning based on lowest frequency) octaves: E2, A2, D3, G3, B3, E4
# 5. write out as tab (create standard format)

class FileAnalyzer():
    def __init__(self, wav_fname):   
        self.file = wav_fname
        self.refTable = np.loadtxt('./note_freq.csv',delimiter =',')
 

    def freq(self, start_time, end_time):

        # Open the file and convert to mono
        sr, data = wavfile.read(self.file)
        if data.ndim > 1:
            data = data[:, 0]
        else:
            pass

        # Return a slice of the data from start_time to end_time
        dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

        # Fourier Transform
        N = len(dataToRead)
        yf = rfft(dataToRead)
        xf = rfftfreq(N, 1 / sr)

        # Uncomment these to see the frequency spectrum as a plot
        # plt.plot(xf, np.abs(yf))
        # plt.show()

        # Get the most dominant frequency and return it
        idx = np.argmax(np.abs(yf))
        freq = xf[idx]
        return freq
    
    

    def graph(self):
        samplerate, data = wavfile.read(self.file)
        print(f"number of channels = {data.shape[1]}")
        length = data.shape[0] / samplerate
        print(f"length = {length}s")


        time = np.linspace(0., length, data.shape[0])
        plt.plot(time, data[:, 0], label="Left channel")
        plt.plot(time, data[:, 1], label="Right channel")
        plt.legend('center')
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

reader = FileAnalyzer('./numb20.wav')

#print(reader.refTable)

