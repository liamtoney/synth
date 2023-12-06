"""
https://en.wikipedia.org/wiki/Piano_key_frequencies
"""

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
