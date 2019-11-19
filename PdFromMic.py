import sys
import aubio
import pyaudio
from aubio import source, pitch, freq2note
import numpy as np
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

dummy, tempo = sys.argv
print("tempo: " + str(tempo)) #specify for quarter note bpm

samplerate = 44100 #samples per second, standard for audio files
buffer_size = 1024 #smaller buffer size so that processing time will be every short
py_format = pyaudio.paInt32 #large file size but better processing
channels = 1
total_frames = 0
tolerance = 0.2

temp = "C-1"
time_s = 0
quarter = 60/int(tempo)
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
            time_t = seconds - time_s
            time_s = seconds
            typen = time_t/quarter
            temp = note
            pitches += [(pitch, note, time_t)]
            print(str(note))
            print("length: " + str(time_t))
            print(str(typen))
        #print("%f %f" % (seconds, pitch)) 
        total_frames += len(signal)   # increment total number of frames

    except KeyboardInterrupt:
        print("*** Ctrl+C, exiting")
        break
print("finished recording")

stream.stop_stream()
stream.close()
p.terminate()