from typing import List


def parse_music(music_string: str) -> List[int]:
    """ Input to this function is a string representing musical notes in a special ASCII format.
    Your task is to parse this string and return list of integers corresponding to how many beats does each
    not last.

    Here is a legend:
    'o' - whole note, lasts four beats
    'o|' - half note, lasts two beats
    '.|' - quater note, lasts one beat

    >>> parse_music('o o| .| o| o| .| .| .| .| o o')
    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
    """
    note_beats_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }

    # Split the input string into individual note components.
    # Using split() without arguments handles multiple spaces as a single delimiter
    # and ignores leading/trailing whitespace.
    note_components = music_string.split()

    beats_list = []
    for note in note_components:
        # Based on the problem description, we assume all note components
        # will be valid keys in the note_beats_map.
        beats_list.append(note_beats_map[note])

    return beats_list