"""
Yes, there are packages which do most of this stuff already, but I wanted to implement
these fundamental functions from ~scratch to learn how they work...
"""

import numpy as np
from scipy import signal
from scipy.io import wavfile

_DEFAULT_OCTAVE = 4  # The octave of the note-frequency lookup table
_A4_FREQUENCY = 440.0  # [Hz] Linked to _DEFAULT_OCTAVE
_NOTES = (
    'C',  # C4 is "middle C"
    'C#/Db',
    'D',
    'D#/Eb',
    'E',
    'F',
    'F#/Gb',
    'G',
    'G#/Ab',
    'A',  # A4 is "A440"
    'A#/Bb',
    'B',
)
_FS = 44100  # [Hz] Audio sampling rate
_DTYPE = np.int16  # Data type corresponding to 16-bit audio
_S_PER_MIN = 60  # [s/min]
_N_CORNERS = 4  # Emulate a "Moog-style" 4-pole (24 dB/octave) filter

# Form lookup table which accounts for sharps and flats (see
# https://en.wikipedia.org/wiki/Scientific_pitch_notation#Table_of_note_frequencies)
_note_frequency_lookup_table = {}
for _i, _note in enumerate(_NOTES):
    _frequency = _A4_FREQUENCY * (2 ** ((_i - _NOTES.index('A')) / 12))
    for _note in _note.split('/'):
        _note_frequency_lookup_table[_note] = _frequency


# Function to calculate the frequency of a provided note and octave (only allows notes
# existing on the piano keyboard)
def n2f(note: str, octave: int = _DEFAULT_OCTAVE) -> float:
    if note not in _note_frequency_lookup_table:
        raise ValueError('Invalid note format')
    if octave not in range(9):
        raise ValueError('Octave must be an integer between 0 and 8 (inclusive)')
    if octave == 0 and note not in ('A', 'A#', 'Bb', 'B'):
        raise ValueError('Requested note is too low')
    if octave == 8 and note != 'C':
        raise ValueError('Requested note is too high')
    _octave_shift = octave - _DEFAULT_OCTAVE
    return _note_frequency_lookup_table[note] * (2**_octave_shift)  # [Hz]


# Function to write a NumPy array to a WAV file as 16-bit 44.1 kHz normalized mono audio
def write_wav(filename: str, signal: np.ndarray):
    output = signal.copy()
    output /= np.abs(output).max()  # Normalize to [-1, 1]
    output *= np.iinfo(_DTYPE).max  # Scale to 16-bit range
    wavfile.write(filename, _FS, output.astype(_DTYPE))


# Function to create a sawtooth wave of a given frequency and duration
def saw(frequency: float, duration: float) -> np.ndarray:
    single_tooth = np.linspace(-1, 1, int(_FS / frequency))
    duration_samples = int(duration * _FS)
    n_cycles_ceil = int(np.ceil(duration_samples / single_tooth.size))
    return np.tile(single_tooth, n_cycles_ceil)[:duration_samples]


# Function to apply a low-pass filter to a signal
def lowpass(s: np.ndarray, cutoff_frequency: float) -> np.ndarray:
    sos = signal.butter(
        _N_CORNERS, cutoff_frequency, btype='lowpass', output='sos', fs=_FS
    )
    return signal.sosfilt(sos, s)


# Try it out!
BPM = 120
CHORD = ('F', 'A', 'C', 'Eb')
NOTE_LENGTH = 4  # [beats] E.g., 4 beats = whole note
CUTOFF_FREQUENCY = 1000  # [Hz]
duration = NOTE_LENGTH / (BPM / _S_PER_MIN)
s = saw(n2f(CHORD[0]), duration)
for note in CHORD[1:]:
    s += saw(n2f(note), duration)
s = lowpass(s, CUTOFF_FREQUENCY)
write_wav('chord.wav', s)
