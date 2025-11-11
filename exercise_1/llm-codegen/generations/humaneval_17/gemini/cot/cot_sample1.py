from typing import List


def parse_music(music_string: str) -> List[int]:
    note_beats_map = {
        'o': 4,   # whole note
        'o|': 2,  # half note
        '.|': 1   # quarter note
    }

    result_beats = []
    
    # Split the input string by spaces.
    # The .split() method without arguments handles multiple spaces
    # and leading/trailing spaces by discarding empty strings,
    # which is suitable for "space-separated musical notes".
    note_tokens = music_string.split()

    for token in note_tokens:
        # Look up the beat duration for each note token.
        # Assuming all tokens in music_string will be valid notes
        # as per the problem description.
        result_beats.append(note_beats_map[token])

    return result_beats