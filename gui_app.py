
import tkinter as tk
from tkinter import filedialog
import dtmf_codec as dc
import sounddevice as sd

def encode():
    sig=dc.encode_text_to_signal(txt.get())
    sd.play(sig,dc.FS_DEFAULT)
    sd.wait()

def save():
    p=filedialog.asksaveasfilename(defaultextension=".wav")
    dc.encode_text_to_wav(txt.get(),p)

def decode():
    p=filedialog.askopenfilename()
    out.insert("end",dc.decode_wav_to_text(p)+"\n")

root=tk.Tk()
txt=tk.StringVar(value="MERHABA DÜNYA")

tk.Entry(root,textvariable=txt,width=40).pack()
tk.Button(root,text="Encode+Play",command=encode).pack()
tk.Button(root,text="Save WAV",command=save).pack()
tk.Button(root,text="Decode WAV",command=decode).pack()
out=tk.Text(root,height=10)
out.pack()
root.mainloop()