

import matplotlib.pyplot as plt
import numpy as np
import dtmf_codec as dc

sig=dc.encode_text_to_signal("MERHABA DÜNYA")
plt.plot(sig)
plt.savefig("waveform.png")
plt.close()
