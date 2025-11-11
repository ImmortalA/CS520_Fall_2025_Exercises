from typing import List

def parse_music(music_string: str) -> List[int]:
    note_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }
    notes = music_string.split()
    beats = []
    for note in notes:
        beats.append(note_map[note])
    return beats