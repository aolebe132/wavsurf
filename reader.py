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
    def __init__(self, wav_fname, bpm):   
        self.file = wav_fname
        #get values from csv (flipped to use freq as key and note as val)
        self.ref = {k:v for v,k in np.loadtxt('./note_freq.csv',delimiter =',')}
        self.bpm = bpm
        #print(self.ref)
 

    def freq(self):

        # Open the file and convert to mono
        sr, data = wavfile.read(self.file)
        if data.ndim > 1:
            data = data[:, 0]
        else:
            pass
        
        num_samples = data.shape[0]
        duration_sec = (num_samples/sr)
        beats_total = int((duration_sec/60)*self.bpm)
        divisions = beats_total*int(128)
        #spm = sr*60
        #spb = spm/self.bpm
        #spd = spb/128
        samples_per_div = int(((sr*60)/self.bpm)/128)

        print(f'{num_samples}, {duration_sec}, {beats_total}, {divisions}, {samples_per_div}')
        freqList = []
        for st in range(divisions): 
            start_time = st*samples_per_div
            #print(start_time)
            end_time = start_time + samples_per_div +1
            #print(end_time)
            # Return a slice of the data from start_time to end_time
            dataToRead = data[int(start_time) : int(end_time)]

            # Fourier Transform
            N = len(dataToRead)
            yf = rfft(dataToRead)
            xf = rfftfreq(N, 1 / sr)

            # Uncomment these to see the frequency spectrum as a plot
            # plt.plot(xf, np.abs(yf))
            # plt.show()

            # Get the most dominant frequency and return it
            idx = np.argmax(np.abs(yf))
            freqList.append(xf[idx])
            
        filthy = np.array(freqList)
        np.savetxt('freq_out.txt',filthy,fmt='%.3f',delimiter=',')


        #return filthy[filthy != 0.0]
        return filthy
    
    def assignNotes(self):
        input = self.freq()
        print(input)
        output = []
        keys = list(self.ref.keys())
        
        for f in input:
            
            for i in range(len(keys)-1):
                #print(f'{freq}, {f}')
                freq = keys[i]
                fnext = keys[i+1]
                if f>=freq and freq<=fnext:
                    output.append(self.ref[freq])
            
        return np.array(output)

        


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

reader = FileAnalyzer('./numb20.wav',63)
output = reader.assignNotes()
np.savetxt('out.txt',output,delimiter=',')

#print(reader.refTable)

