import os  # Getting and checking paths
import argparse  # Getting the arguments from the user
import random  # Generate random values and choices from lists
from itertools import count, cycle  # Naming unique name to the midi file, and iterating over list many times.
from collections import deque  # Rotating lists
from midiutil.MidiFile import MIDIFile  # Creating midi file

__author__ = 'Dvir Alafi'

"""

        Random Melody Generator

This program written by Dvir Alafi.
Developed to make music making easy and fast.

The program provides a MIDI file that contains chords and melody, written totally randomly by the program.
The MIDI file can easily be used by your favorite DAW (Digital Audio Workstation).

You can choose various options for the program.
The options you won't choose will be chosen randomly.
When you execute the program at the command line you can pass it as arguments:

                        -p - Path to save the midi files.
                        -k - the Key of the scale - a letter.
                        -t - the Type of the scale.
                        -a - the emotional Atmosphere of the chords progressions.
                        -l - the Length of the melody - Number of Beats.
                        -b the Bpm of the melody - in numbers.

"""

# Constants:

DEFAULT_MELODY_LENGTH = 16  # 4 Bars - 16 Beats
DEFAULT_BPM = 120
DEFAULT_VOLUME = 100
DEFAULT_CHANCE_FOR_NOTE = 0.99  # 60%
DEFAULT_CHANCE_FOR_REST = 0.29  # 20%
DEFAULT_CHANCE_FOR_ADDING = 0.09  # 10%

ATMOSPHERE_DICT = {'happy': 'vi-IV-I-V',
                   'pop': 'I-V-vi-IV',
                   'joyful': 'I-vi-ii-V',
                   'cheerful': 'I-vi-IV-V',
                   'dark': 'I-vi-iii-VII',
                   'emotional': 'I-vi-iii-iii',
                   'sad': 'ii-vi-I-V',
                   'building': 'V-IV-I-I'}

SCALES_DICT = {
    'aeolian': (0, 2, 3, 5, 7, 8, 10),
    'bachian': (0, 2, 3, 5, 7, 9, 11),
    'blues': (0, 2, 3, 4, 5, 7, 9, 10, 11),
    'chromatic': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    'dorian': (0, 2, 3, 5, 7, 9, 10),
    'harmonicmajor': (0, 2, 4, 5, 7, 8, 11),
    'harmonicminor': (0, 2, 3, 5, 7, 8, 11),
    'locrian': (0, 2, 4, 5, 6, 7, 9),
    'lydian': (0, 2, 4, 6, 7, 9, 11),
    'major': (0, 2, 4, 5, 7, 9, 11),
    'melodicminor': (0, 2, 3, 5, 7, 8, 9, 10, 11),
    'minorneapolitan': (),
    'minor': (0, 2, 3, 5, 7, 8, 10),
    'mixolydian': (0, 2, 4, 5, 7, 9, 10),
    'naturalminor': (0, 2, 3, 5, 7, 8, 10),
    'octatonic': (),
    'phrygian': (0, 1, 4, 5, 7, 8, 10),
    'pentatonic': (0, 2, 4, 7, 9),
    'wholetone': (0, 2, 4, 6, 8, 10)}

"""
SCALES_TYPE_LIST = ['aeolian', 'blues', 'bachian', 'chromatic', 'dorian', 'harmonicmajor', 'harmonicminor',
'locrian', 'lydian', 'major', 'melodicminor', 'minor', 'minorneapolitan', 'mixolydian',
'naturalminor', 'octatonic', 'phrygian', 'pentatonic',  'wholetone']
"""

ROMAN_LETTERS_VALUE_DICT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}

CHORDS_SEQUENCE_DICT = {'major': (0, 2, 2),
                        'minor': (0, 1, 2),
                        'major seventh': (1, 3, 5, 7),
                        'minor seventh': (1, 3, 5, 7)}

DIATONIC_KEYS = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
DIATONIC_KEYS_PITCH_DICT = {'Bb': 58, 'B': 59, 'B#': 60, 'Cb': 59, 'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63,
                            'Eb': 63, 'E': 64, 'E#': 65, 'Fb': 64, 'F': 65, 'F#': 66, 'Gb': 66, 'G': 67, 'G#': 68,
                            'Ab': 68, 'A': 69, 'A#': 70}

USER_INSTRUCTIONS_TEXT = "You can choose options for the automatic music you want" \
                         "to generate. the options you won't choose will be chosen randomly.\n\n" \
                         "-p - Path to save the midi files.\n" \
                         "-k - the Key of the scale - a letter.\n" \
                         "-t - the Type of the scale.\n" \
                         "-a - the emotional Atmosphere of the chords progressions.\n" \
                         "-l - the Length of the melody - Number of Beats.\n" \
                         "-b - the Bpm of the melody - in numbers.\n"
ITEM_NOT_FOUND_USER_MESSAGE = "There is no '{user_input}' in the repository.\nplease select from this list :\n" \
                            "{repository_list}\nUntil then, it'll be chosen randomly. this time it's: {random_decision}"


# Functions:


def get_chord_notes_by_num(scale_notes, chord_num):
    """
    Returns the notes of the required chord:

    :param scale_notes: list of the notes in the scale of the chord , for example, ['C','D','E','F','G','A','B']
    :param chord_num: the number of the chord, for example I - first, iii - third, etc.

    :return: list of notes of the required chord

    """
    cycle_list = cycle(scale_notes)
    chord_notes = []
    chord_num -= 1  # Because of the index in lists. if i want the first one it's in index 0 and not in 1.

    for note in cycle_list:
        if scale_notes.index(note) == chord_num or scale_notes.index(note) == chord_num - len(scale_notes):
            chord_notes.append(note)
            chord_num += 2
        if len(chord_notes) == 3:
            break

    return chord_notes


def get_unique_file_name(file_path, basename, ext):
    """
    Returns a unique file path, with a new file name:

    :param file_path: The path of the file
    :param basename: the name of the file
    :param ext: the extension of the file, for example '.txt', '.py', '.mid' .

    :return: a unique file path with a unique name that doesnt exists in the path of the given folder.
             for example, if it has: Midis/RandoMMelody, then, it will return: Midis/RandoMMelody_2,
              and that in the next process: Midis/RandoMMelody_3, etc.

    """

    file_name = file_path + '/' + "{basename}.{ext}".format(basename=basename, ext=ext)
    available_numbers_counter = count(2)

    while os.path.exists(file_name):
        file_name = file_path + '/' + "{basename}_{number}.{ext}".format(basename=basename,
                                                                              number=next(available_numbers_counter),
                                                                              ext=ext)
    return file_name


def get_scale_notes(scale_key, scale_type):
    """
    Finds the notes of the given scale:


    :param scale_key: the key of the scale, for example, 'C#'
    :param scale_type: the type of the scale, for example 'minor'

    :return: a list of the notes in the specific key and type.

    """

    if scale_type not in SCALES_DICT:
        scale_type = random.choice(list(SCALES_DICT.keys()))
        print(ITEM_NOT_FOUND_USER_MESSAGE.format(scale_type, list(SCALES_DICT.keys()), scale_type))

    scale_jumping_values = SCALES_DICT[scale_type]
    diatonic_notes_deque = deque(DIATONIC_KEYS)

    diatonic_notes_deque.rotate(12 - DIATONIC_KEYS.index(scale_key))
    scale_notes = ()
    for jump_value in scale_jumping_values:
        scale_notes += (diatonic_notes_deque[jump_value],)  # Using Tuple for memory saving

    return scale_notes


def generate_chord_progression(requested_melody_length, midi_file, chords_track,
                               scale_notes, chords_atmosphere):

    """
    Generate the chord progression and write it to the MIDI file:


    :param requested_melody_length: the melody length requested .
    :param midi_file: the MIDI file Object, to manipulate and write to.
    :param chords_track: the chords track of the MIDI file
    :param scale_notes: a list of the notes in a specific key.
    :param chords_atmosphere: the atmosphere of the chords. for example - sad, happy, pop, etc.

    :return: None.
             making a change in the given MIDI file.



    """

    channel = 1  # Because 0 is for the melody part.
    current_melody_length = 0  # Initiate the time stamp for the track
    volume = DEFAULT_VOLUME

    #  chord_progression_values = for example I-V-vi-IV
    if chords_atmosphere in ATMOSPHERE_DICT:
        chord_progression_values = ATMOSPHERE_DICT[chords_atmosphere].split('-')
    else:
        chord_progression_values = random.choice(list(ATMOSPHERE_DICT.values())).split('-')
        print(ITEM_NOT_FOUND_USER_MESSAGE.format(user_input=chords_atmosphere,
                                                 repository_list=list(ATMOSPHERE_DICT.keys()),
                                                 random_decision=chord_progression_values))

    # chords_list = for example  [['E', 'G#', 'B'], ['B', 'D#', 'F#'], ['C#', 'E', 'G#'], ['A', 'C#', 'E']]
    chords_list = [get_chord_notes_by_num(scale_notes,
                                          ROMAN_LETTERS_VALUE_DICT[x.upper()]) for x in chord_progression_values]
    print(chords_list)

    duration = int(requested_melody_length / 4)

    # Writing chords to the file
    for chord_notes in chords_list:
        for note in chord_notes:
            pitch = DIATONIC_KEYS_PITCH_DICT[note]

            midi_file.addNote(chords_track, channel, pitch, current_melody_length, duration, volume)

        current_melody_length += duration  # after adding one chord the next should be after him.


def generate_random_melody(requested_melody_length, midi_file, melody_track, scale_notes):

    """
    Generate the melody and write it to the MIDI file:


    :param requested_melody_length: the melody length requested .
    :param midi_file: the MIDI file Object, to manipulate and write to.
    :param melody_track: the melody track of the MIDI file
    :param scale_notes: a list of the notes in a specific key.

    :return: None.
             making a change in the given MIDI file.

    """

    channel = 0  # Because 1 is for the chords part.
    current_melody_length = 0  # Initiate the time stamp for the track
    volume = DEFAULT_VOLUME

    chance_for_note = DEFAULT_CHANCE_FOR_NOTE
    chance_for_rest = DEFAULT_CHANCE_FOR_REST
    chance_for_adding = DEFAULT_CHANCE_FOR_ADDING

    while current_melody_length < requested_melody_length:
        random_chance = random.random()

        # if random_chance is between the 0.39 and 0.99 area its a
        # 60% chance and a note is added to the file:
        if chance_for_note > random_chance > chance_for_rest:

            pitch_letter = random.choice(scale_notes)
            pitch = DIATONIC_KEYS_PITCH_DICT[pitch_letter]

            duration = random.choice([0.5, 0.75, 1, 1.5, 2])
            if requested_melody_length - current_melody_length < 0.25:
                break
            while duration > requested_melody_length - current_melody_length:
                duration = random.choice([0.5, 0.75, 1, 1.5, 2])

            # continuing from the preview note:
            note_time = current_melody_length
            # Adding the note to the Midi file:
            midi_file.addNote(melody_track, channel, pitch, note_time, duration, volume)

            current_melody_length += duration
            continue

        # if random_chance is between the 0.09 and 0.39 area its a
        # 30% chance and silence is added to the file:
        elif chance_for_rest > random_chance > chance_for_adding:
            # Adding rest (silence):
            duration_of_rest = random.choice([0.5, 1, 1.5])
            if requested_melody_length - current_melody_length < 0.5:
                break

            while duration_of_rest > requested_melody_length - current_melody_length:
                duration_of_rest = random.choice([0.5, 1, 1.5])

            current_melody_length += duration_of_rest
            continue

        #  Here it Adds an Adding:
        if random.choice([0, 1, 2]) > 0:
            #  triplets of notes
            if requested_melody_length - current_melody_length < 0.75:  # calculating the remaining time left.
                break
            duration = random.choice([0.125, 0.25])
            for i in range(3):
                pitch_letter = random.choice(scale_notes)
                pitch = DIATONIC_KEYS_PITCH_DICT[pitch_letter]

                # continuing from the preview note:
                note_time = current_melody_length
                # Adding the note to the Midi file:
                midi_file.addNote(melody_track, channel, pitch, note_time, duration, volume)

                current_melody_length += duration

                break
        #  Pitch bend:
        pitch_quantity = random.choice(range(3000, 9000, 1000))  # range 3000 - 8000 in a 1000 jumps.
        MIDIFile.addPitchWheelEvent(midi_file, melody_track, channel, float(current_melody_length), pitch_quantity)
        print('pitch bend')


def play_midi_file(midi_file_path):
    """
    Playing a Midi file

    :param midi_file_path: The path of the MIDI file

    :return: None.
             Playing the file.

    """

    print(midi_file_path)
    pass


def main():
    """
    Main Function
    :return: None
    """
    # parsing the user arguments using Argparse:

    parser = argparse.ArgumentParser(description=USER_INSTRUCTIONS_TEXT)
    parser.add_argument('-p', "--midi_files_path",  help="Path to save the midi files of the auto-generated music."
                                                         "default path - your current working directory.",
                        default=os.getcwd())
    parser.add_argument('-k', '--scale_key', help="the key of the scale", default=random.choice(DIATONIC_KEYS))
    parser.add_argument('-t', '--scale_type', help="the type of the scale",
                        default=random.choice(list(SCALES_DICT.keys())))
    parser.add_argument('-a', '--chords_atmosphere', help="the atmosphere of the chord progression",
                        default=random.choice(list(ATMOSPHERE_DICT.keys())))
    parser.add_argument('-l', '--melody_length', help="the length of the melody", default=DEFAULT_MELODY_LENGTH)
    parser.add_argument('-b', '--bpm', help="the bpm of the melody", default=DEFAULT_BPM)

    args = parser.parse_args()
    midi_files_path = args.midi_files_path
    scale_type = args.scale_type
    scale_key = args.scale_key
    chords_atmosphere = args.chords_atmosphere
    melody_length = args.melody_length
    bpm = args.bpm

    midi_file = MIDIFile(2)  # 2 tracks - one for the Chords, and one for the Melody.

    melody_track = 0
    chords_track = 1
    init_time = 0  # start at the beginning

    midi_file.addTrackName(melody_track, init_time, "melody")
    midi_file.addTempo(melody_track, init_time, bpm)

    midi_file.addTrackName(chords_track, init_time, "chords")
    midi_file.addTempo(chords_track, init_time, bpm)

    scale_notes = get_scale_notes(scale_key, scale_type)

    generate_chord_progression(melody_length, midi_file, chords_track, scale_notes, chords_atmosphere)

    generate_random_melody(melody_length, midi_file, melody_track, scale_notes)

    midi_file_name = get_unique_file_name(midi_files_path, 'RandoMMelody', 'mid')

    with open(midi_file_name, 'wb') as output_file:

        midi_file.writeFile(output_file)


if __name__ == '__main__':
    main()
