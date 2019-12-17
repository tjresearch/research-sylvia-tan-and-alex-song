import sys
import aubio
import pyaudio
from aubio import source, pitch, freq2note
import numpy as np
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

dummy = sys.argv

samplerate = 44100 #samples per second, standard for audio files
buffer_size = 1024 #smaller buffer size so that processing time will be every short
py_format = pyaudio.paInt32 #large file size but better processing
channels = 1
total_frames = 0
tolerance = 0.3
expected = [(261.63, 2.5), (293.67, 2.5), (329.63, 2.5), (349.23, 2.5), (392.00, 2.5), (440.00, 2.5), (493.88, 2.5), (523.25, 2.5), (493.88, 2.5), (440.00, 2.5), (392.00, 2.5)] 

temp = "C-1"
time_s = 0
times = []
pitches = []

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

pyaudio_format = pyaudio.paFloat32
n_channels = 1
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

pitchd = aubio.pitch("default", 4096, buffer_size, samplerate)
pitchd.set_unit("Hz")
pitchd.set_tolerance(tolerance)

notes = 0
pnotes = 0
tleast = 0
error = 0
nt = 0

print("recording")
print(temp)
while True:
    try:
        data = stream.read(buffer_size)
        signal = np.fromstring(data, dtype=np.float32)
        pitch = pitchd(signal)[0]
        pitch = int(round(pitch))
        note = freq2note(pitch)
        seconds = total_frames/float(samplerate) # equals seconds passed
        if note != temp:
            if nt == 0 or note != "C-1":
                #CALC PRINT LENGTH AND TIME OF CURRENT NOTE AS WELL AS TEMPO/TIME ERROR
                nt = nt + 1

                #print("pnotes:" + str(pnotes) + " ... notes:" + str(notes))
                if pnotes != notes:
                    time_t = seconds - time_s
                    time_s = seconds
                    print(time_t)
                    tleast = abs(expected[notes][1] - time_t)
                    #print("tleast: " + str(tleast))
                pnotes = notes

                #temp = note
                #pitches += [(pitch, note, time_t)]
                print(str(note))
                #print("length: " + str(time_t) + " pitch: " + str(pitch))

                #CALC PRINT CURRENT (PITCH) ERROR AND NOTE NUMBER
                harmonic1 = pitch/2
                harmonic2 = pitch*2
                least1 = (min(abs(expected[notes][0] - pitch), abs(expected[notes-1][0] - pitch), abs(expected[notes+1][0] - pitch)))
                least2 = (min(abs(expected[notes][0] - harmonic1), abs(expected[notes-1][0] - harmonic1), abs(expected[notes+1][0] - harmonic1)))
                least3 = (min(abs(expected[notes][0] - harmonic2), abs(expected[notes-1][0] - harmonic2), abs(expected[notes+1][0] - harmonic2)))
                least = min(least1, least2, least3)
                #print("leasts: " + str(least1) + " " + str(least2) + " " + str(least3))
                #print("w: " + str(abs(expected[notes-1] - harmonic1)))

                print("current error: " + str(least))
                if least == abs(expected[notes][0] - pitch) or least == abs(expected[notes][0] - harmonic1) or  least == abs(expected[notes][0] - harmonic2):
                    notes = notes + 1
                elif least == abs(expected[notes-1][0] - pitch) or  least == abs(expected[notes-1][0] - harmonic1) or  least == abs(expected[notes-1][0] - harmonic2):
                    notes = notes
                elif least == abs(expected[notes+1][0] - pitch) or  least == abs(expected[notes-1][0]- harmonic2) or  least == abs(expected[notes-1][0] - harmonic2):
                    notes = notes + 2

                #CALC PRINT TOTAL ERROR
                error = error + least*0.7 + tleast*0.3
                print("total error: " + str(error))
                print("note #" + str(notes))

        if notes == 10:
            error = error/10
            print("error " + str(error))
            notes = 0
            error = 0
        total_frames += len(signal)   # increment total number of frames

    except KeyboardInterrupt:
        print("*** Ctrl+C, exiting")
        break
print("finished recording")

stream.stop_stream()
stream.close()
p.terminate()
