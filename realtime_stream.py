
import sounddevice as sd
import numpy as np
import dtmf_codec as dc

fs=44100
dur=0.04
win=int(fs*dur)

print("Listening...")

def callback(indata,frames,time,status):
    x=indata[:,0]
    if np.max(np.abs(x))<0.02:
        return
    x=dc.apply_window(x)
    low=max(dc.LOW_FREQS,key=lambda f:dc.goertzel_power(x,fs,f))
    high=max(dc.HIGH_FREQS,key=lambda f:dc.goertzel_power(x,fs,f))
    ch=dc.REV_MAP.get((low,high))
    if ch:
        print(ch,end="",flush=True)

with sd.InputStream(channels=1,samplerate=fs,blocksize=win,callback=callback):
    input()