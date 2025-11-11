def parse_music(music_string: str) -> List[int]:
    if not music_string.strip():
        return []

    note_map = {
        'o': 4,
        'o|': 2,
        '.|': 1
    }

    tokens = music_string.split()
    result = []

    for token in tokens:
        if token in note_map:
            result.append(note_map[token])
        else:
            # Handle unexpected tokens by skipping (or could raise ValueError)
            pass

    return result