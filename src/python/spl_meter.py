## //src / python / spl_meter.py
#!/usr/bin/env python3
import argparse
import numpy as np
import sounddevice as sd
import sys

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-d', '--device', type=int_or_str, help='input device (numeric ID or substring)')
parser.add_argument('-r', '--samplerate', type=float, help='sampling rate')
parser.add_argument('-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument('-t', '--interval', type=float, default=0.1, help='update interval in seconds')
args = parser.parse_args()

samplerate = sd.query_devices(args.device, 'input')['default_samplerate'] if args.samplerate is None else args.samplerate

def calculate_spl(indata):
    rms = np.sqrt(np.mean(indata**2))
    spl = 20 * np.log10(rms / 20e-6)  # Reference pressure: 20 µPa
    return spl

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    spl = calculate_spl(indata)
    print(f"{spl:.2f}")
    sys.stdout.flush()

try:
    with sd.InputStream(device=args.device, channels=args.channels,
                        samplerate=samplerate, callback=callback,
                        blocksize=int(samplerate * args.interval)):
        print('#' * 80)
        print('Press Ctrl+C to stop the SPL measurement')
        print('#' * 80)
        sd.sleep(2**31 - 1)
except KeyboardInterrupt:
    print('\nMeasurement finished')
except Exception as e:
    print(str(e))