
import argparse
import dtmf_codec as dc
import sounddevice as sd

parser=argparse.ArgumentParser()
sub=parser.add_subparsers(dest="cmd")

sub.add_parser("map")

enc=sub.add_parser("encode")
enc.add_argument("--text")
enc.add_argument("--out",default="encoded.wav")

dec=sub.add_parser("decode")
dec.add_argument("--infile")

args=parser.parse_args()

if args.cmd=="map":
    print(dc.CHAR_MAP)

if args.cmd=="encode":
    sig=dc.encode_text_to_wav(args.text,args.out)
    sd.play(sig,dc.FS_DEFAULT)
    sd.wait()

if args.cmd=="decode":
    print(dc.decode_wav_to_text(args.infile))