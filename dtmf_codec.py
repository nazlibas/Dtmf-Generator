
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from scipy.io.wavfile import write, read

TURKISH_CHARS = [
"A","B","C","Ç","D","E","F","G","Ğ","H","I","İ","J","K","L","M","N","O","Ö","P","R","S","Ş","T","U","Ü","V","Y","Z"," "
]

LOW_FREQS  = [500, 600, 700, 800, 900, 1000]
HIGH_FREQS = [1500, 1600, 1700, 1800, 1900]

FS_DEFAULT = 44100
DURATION_DEFAULT = 0.040
GAP_DEFAULT = 0.005

def build_char_map():
    mapping = {}
    idx = 0
    for lf in LOW_FREQS:
        for hf in HIGH_FREQS:
            mapping[TURKISH_CHARS[idx]] = (lf, hf)
            idx += 1
    return mapping

CHAR_MAP = build_char_map()
REV_MAP = {v: k for k, v in CHAR_MAP.items()}

def synth_tone(f1, f2, fs, duration, amplitude=0.6):
    n = int(fs * duration)
    t = np.arange(n)/fs
    s = np.sin(2*np.pi*f1*t) + np.sin(2*np.pi*f2*t)
    return (s*(amplitude/2)).astype(np.float32)

def encode_text_to_signal(text, fs=FS_DEFAULT, duration=DURATION_DEFAULT, gap=GAP_DEFAULT):
    text = text.upper()
    gap_sig = np.zeros(int(fs*gap), dtype=np.float32)
    sig=[]
    for ch in text:
        f1,f2 = CHAR_MAP[ch]
        sig.append(synth_tone(f1,f2,fs,duration))
        sig.append(gap_sig)
    return np.concatenate(sig)

def encode_text_to_wav(text, wav_path):
    sig = encode_text_to_signal(text)
    write(wav_path, FS_DEFAULT, sig)
    return sig

def goertzel_power(x,fs,freq):
    N=len(x)
    k=int(0.5+(N*freq)/fs)
    w=2*np.pi*k/N
    coeff=2*np.cos(w)
    s_prev=0
    s_prev2=0
    for sample in x:
        s=sample+coeff*s_prev-s_prev2
        s_prev2=s_prev
        s_prev=s
    return s_prev2*s_prev2+s_prev*s_prev-coeff*s_prev*s_prev2

def apply_window(x):
    return x*np.hamming(len(x))

@dataclass
class DecodeConfig:
    duration:float=0.040
    gap:float=0.005
    thr:float=0.01

def decode_wav_to_text(wav_path,cfg=DecodeConfig()):
    fs,data=read(wav_path)
    if data.ndim>1:
        data=data[:,0]
    data=data.astype(np.float32)

    win=int(fs*cfg.duration)
    step=win+int(fs*cfg.gap)
    out=[]
    for i in range(0,len(data)-win,step):
        chunk=data[i:i+win]
        if np.max(np.abs(chunk))<cfg.thr:
            continue
        chunk=apply_window(chunk)
        low=max(LOW_FREQS,key=lambda f:goertzel_power(chunk,fs,f))
        high=max(HIGH_FREQS,key=lambda f:goertzel_power(chunk,fs,f))
        out.append(REV_MAP[(low,high)])
    return "".join(out)