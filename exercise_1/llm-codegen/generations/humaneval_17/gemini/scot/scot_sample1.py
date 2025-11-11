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
    beats_list = []
    # Using split() without arguments handles multiple spaces and leading/trailing spaces
    # and correctly returns an empty list for an empty input string.
    notes = music_string.split()

    for note_str in notes:
        if note_str == 'o':
            beats_list.append(4)
        elif note_str == 'o|':
            beats_list.append(2)
        elif note_str == '.|':
            beats_list.append(1)
        # Assuming valid input as per problem description.
        # No explicit handling for unknown note_str, which would imply
        # an error or unexpected input format.
    return beats_list