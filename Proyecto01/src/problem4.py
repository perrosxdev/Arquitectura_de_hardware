import wave
import struct
import numpy as np
import os

def freq_from_semitone_offset(offset):
    return 440.0 * (2.0 ** (offset / 12.0))

def write_mono_wav(path, samples, rate):
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(b''.join(struct.pack('<h', int(s)) for s in samples))

def write_stereo_wav(path, left, right, rate):
    with wave.open(path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        frames = []
        for l, r in zip(left, right):
            frames.append(struct.pack('<hh', int(l), int(r)))
        wf.writeframes(b''.join(frames))

def tone(freq, duration, rate, amplitude=16000):
    t = np.linspace(0, duration, int(rate*duration), endpoint=False)
    return amplitude * np.sin(2*np.pi*freq*t)

def main():
    out_dir = os.path.join(os.path.dirname(__file__), 'wav_out')
    os.makedirs(out_dir, exist_ok=True)

    # Semitone offsets relative to A4 (440 Hz)
    notes_offsets = {'C4': -9, 'D4': -7, 'E4': -5, 'F4': -4, 'G4': -2, 'A4': 0, 'B4': 2}
    pentatonic = ['C4','D4','E4','F4','G4','A4','B4']

    # 1) Pentatonic mono 44100
    RATE = 44100
    for note in pentatonic:
        f = freq_from_semitone_offset(notes_offsets[note])
        s = tone(f, 1.0, RATE)
        path = os.path.join(out_dir, f'part1_{note}_{RATE}Hz_mono.wav')
        write_mono_wav(path, s, RATE)

    # 2) Reverse pentatonic stereo 22050
    RATE = 22050
    rev = list(reversed(pentatonic))
    left = np.concatenate([tone(freq_from_semitone_offset(notes_offsets[n]), 1.0, RATE) for n in rev])
    right = left.copy()
    path = os.path.join(out_dir, 'part2_rev_pentatonic_22050Hz_stereo.wav')
    write_stereo_wav(path, left, right, RATE)

    # 3) Pentatonic mono 8000
    RATE = 8000
    for note in pentatonic:
        f = freq_from_semitone_offset(notes_offsets[note])
        s = tone(f, 1.0, RATE)
        path = os.path.join(out_dir, f'part3_{note}_{RATE}Hz_mono.wav')
        write_mono_wav(path, s, RATE)

    # 4) Stereo combined signal 10s, RATE=44100
    RATE = 44100
    dur = 10
    s1 = tone(500.0, dur, RATE, amplitude=8000)
    s2 = tone(250.0, dur, RATE, amplitude=8000)
    left = s1 + s2
    right = s1 + s2
    path = os.path.join(out_dir, 'part4_combined_44100_stereo.wav')
    write_stereo_wav(path, left, right, RATE)

    # 5) Lower volume by 75% (multiply by 0.25)
    left_q = left * 0.25
    right_q = right * 0.25
    path = os.path.join(out_dir, 'part5_quiet_75pct_stereo.wav')
    write_stereo_wav(path, left_q, right_q, RATE)

    # 6) Clean left channel (set left to zero)
    left_zero = np.zeros_like(left)
    path = os.path.join(out_dir, 'part6_left_cleaned_stereo.wav')
    write_stereo_wav(path, left_zero, right, RATE)

if __name__ == '__main__':
    import struct
    main()
