"""
https://en.wikipedia.org/wiki/Piano_key_frequencies
"""

import numpy as np
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

# Form lookup table which accounts for sharps and flats
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


# Function to create a sawtooth wave of a given frequency and duration
def saw(frequency: float, duration: float) -> np.ndarray:
    single_tooth = np.linspace(-1, 1, int(_FS / frequency))
    duration_samples = int(duration * _FS)
    n_cycles_ceil = int(np.ceil(duration_samples / single_tooth.size))
    return np.tile(single_tooth, n_cycles_ceil)[:duration_samples]


# Try it out!
chord = ('F', 'A', 'C', 'Eb')
duration = 2  # [s]
signal = np.zeros(int(duration * _FS))
for note in chord:
    signal += saw(n2f(note), duration)
wavfile.write('chord.wav', _FS, signal)
