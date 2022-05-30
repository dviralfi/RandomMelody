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

                        -p - Path to save the midi file.
                        -k - the Key of the scale - a letter.
                        -t - the Type of the scale.
                        -a - the emotional Atmosphere of the chords progressions.
                        -l - the Length of the melody - Number of Beats.
                        -b the Bpm of the melody - in numbers.

When the program is executed by the RandomMelodySite that I created also, it will get it arguments by calling
the 'main' function with the appropriate arguments.

"""

# Constants:

DEFAULT_MELODY_LENGTH = 16  # 4 Bars - 16 Beats
DEFAULT_BPM = 120
DEFAULT_VOLUME = 100
DEFAULT_CHANCE_FOR_NOTE = 0.99  # 60%
DEFAULT_CHANCE_FOR_REST = 0.29  # 20%
DEFAULT_CHANCE_FOR_ADDING = 0.09  # 10%

# 'building2': "i-v-VI-VII....i-v-VI-VI"
ATMOSPHERE_DICT = {'happy': 'vi-IV-I-V',
                   'pop': 'I-V-vi-IV',
                   'joyful': 'I-vi-ii-V',
                   'cheerful': 'I-vi-IV-V',
                   'dark': 'I-vi-iii-VII',
                   'emotional': 'I-vi-iii-iii',
                   'sad': 'ii-vi-I-V',
                   'confusing': 'I-VI-IV-V',
                   'crying': 'I-VI-IV-I',
                   'building': 'V-IV-I-I',
                   'needtodecide': "II-V-I",
                   }


# MODES_LIST = [Ionian [major scale], Dorian, Phrygian, Lydian, Mixolydian, Aeolian [natural minor scale], Locrian]


"""
Ionian (major scale)	W W H W W W H / C D E F G A B C	Happy
Dorian	W H W W W H W / D E F G A B C D	Melancholic
Phrygian	H W W W H W W / E F G A B C D E	Mysterious
Lydian	W W W H W W H / F G A B C D E F	Over-sweet
Mixolydian	W W H W W H W / G A B C D E F G	Content
Aeolian (minor scale)	W H W W H W W / A B C D E F G A	Sad
Locrian	H W W H W W W / B C D E F G A B	Bizarre

"""


MODES_DICT = {
    "ionian":"happy", 
    "dorian":"melancholic", 
    "phrygian":"mysterious", 
    "lydian":"over-sweet", 
    "mixolydian":"content", 
    "aeolian":"sad", 
    "locrian":"bizarre",

}

SCALES_DICT = {
    'major': (0, 2, 4, 5, 7, 9, 11),
    'minor': (0, 2, 3, 5, 7, 8, 10),

    'harmonicmajor': (0, 2, 4, 5, 7, 8, 11),
    'melodicminor': (0, 2, 3, 5, 7, 8, 9, 10, 11),
    'naturalminor': (0, 2, 3, 5, 7, 8, 10),
    'harmonicminor': (0, 2, 3, 5, 7, 8, 11),

    "ionian":(0, 2, 4, 5, 7, 9, 11), # same as Major
    'dorian': (0, 2, 3, 5, 7, 9, 10),
    'phrygian': (0, 1, 3, 5, 7, 8, 10),
    'lydian': (0, 2, 4, 6, 7, 9, 11),
    'mixolydian': (0, 2, 4, 5, 7, 9, 10),
    'aeolian': (0, 2, 3, 5, 7, 8, 10), # same as natural minor 
    'locrian': (0, 1, 3, 5, 6, 8, 10),

    'pentatonic': (0, 2, 4, 7, 9),
    'blues': (0, 2, 3, 4, 5, 7, 9, 10, 11),

    'bachian': (0, 2, 3, 5, 7, 9, 11),
    
    'minorneapolitan': (0, 1, 3, 5, 6, 9, 11),
    'majorneapolitan': (0, 1, 3, 5, 7, 9, 11),

    'octatonic-wholetone': (0, 2, 3, 5, 6, 8, 9, 11),
    'octatonic-semitone':(0, 1, 3, 4, 6, 7, 9, 10),
    
    'chromatic': (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
    'wholetone': (0, 2, 4, 6, 8, 10)}


"""
SCALES_TYPE_LIST = ['aeolian', 'blues', 'bachian', 'chromatic', 'dorian', 'harmonicmajor', 'harmonicminor',
'locrian', 'lydian', 'major', 'melodicminor', 'minor', 'minorneapolitan', 'mixolydian',
'naturalminor', 'octatonic', 'phrygian', 'pentatonic',  'wholetone']
"""

SILENCE_DURATIONS_LIST = [0.5, 1]
NOTE_DURATIONS_LIST = [0.5, 1, 2]
ADDINGS_DURATIONS_LIST = [0.25, 0.5]

ROMAN_LETTERS_VALUE_DICT = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
ROMAN_LETTERS_VALUE_LIST = ['Roman Letter:', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

# I – ii – iii – IV – V – vi – vii how the chords in any scale works (capital letter - major, small letter- minor)
MAJOR_CHORDS_TYPES = ["major", "minor", "minor", "major", "major", "minor", "diminished"]
MINOR_CHORDS_TYPES = ["minor", "dim", "major", "minor", "minor", "major", "major"]

HARMONIC_MINOR_CHORDS_TYPES = ["min","dim","aug","min","maj","maj","dim"]
HARMONIC_MINOR_EXT_CHORDS_TYPES = ["min/maj7","min-7th-flat-5","major-7th-flat-5","minor-7th","dom-7th","maj-7th","dim-7th"]

MELODIC_MINOR_CHORDS_TYPES = ["minor","minor","aug","major","major","dim","dim"]
MELODIC_MINOR_EXT_CHORDS_TYPES = ["min/maj7","min-7th","maj-7th-flat-5","dom-7th","dom-7th","min-7th-flat-5","min-7th-flat-5"]

MAJOR_EXT_CHORDS_TYPES = ["maj-7th","min-7th","min-7th","maj-7th","dom-7th","min-7th","min-7th-flat-5"]

MINOR_EXT_CHORDS_TYPES = ["min-7th-flat-5","maj-7th","min-7th","min-7th","maj-7th","dom-7th"]



CHORDS_SEQUENCE_DICT = {'major': (0, 4, 7),
                        'minor': (0, 3, 7),

                        'maj-7th': (0, 4, 7 ,11),
                        'min-7th': (0, 3, 7, 10),

                        'min-7th-flat-5': (0, 3, 6, 10),
                        'maj-7th-flat-5': (0, 4, 6, 11),

                        'dim':(0, 3, 6),
                        "dim-7th":(0, 3, 6, 9),

                        'aug':(0, 4, 8),
                        "aug-7th":(0, 4, 8, 10),

                        "maj-6th":(0, 4, 7, 9),
                        "maj-9th":(0, 4, 7, 11, 14),
                        "min-6th":(0, 3, 7, 9),
                        "min-9th":(0, 3, 7, 10, 14),
                        "min-11th":(),
                        "maj-11th":(),
                        "min-13th":(),
                        "maj-13th":(),


                        "dom-7th":(0, 4, 7, 10),
                        "dom-7th-sharp-9":(),
                        "dom-9th":(),
                        "dom-11th":(),
                        "dom-13th":(),

                        "sus2":(0,2,7),        
                        "sus4":(0,5,7),
                        "sus7":(),
                        "sus9":(),
                        "add2":(),
                        "add9":(),
                        }

CHROMATIC_KEYS = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

CHROMATIC_KEYS_PITCH_DICT = {'Bb': 58, 'B': 59, 'B#': 60, 'Cb': 59, 'C': 60, 'C#': 61, 'Db': 61, 'D': 62, 'D#': 63,
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


def is_major(chord_notes):
    """
    Gets a chord by his notes.
    Returns True if the chord is Major, False if its Minor
    """
    interval = CHROMATIC_KEYS.index(chord_notes[2]) - CHROMATIC_KEYS.index(chord_notes[1])
    
    if interval  == 3 or interval == -3:

        return True
    else:
        return False
    

def get_chord_notes_by_name(scale_notes,chord_name):
    
    scale_notes = scale_notes+scale_notes

    intervals = CHORDS_SEQUENCE_DICT[chord_name] # for example - (0,4,6,10)

    chord_notes = []
    for i in range(len(intervals)):
        chord_notes.append(scale_notes[intervals[i]])
        print(chord_notes)
    return chord_notes


def get_chord_notes_by_note_and_type(note,type):

    cycle_list = CHROMATIC_KEYS+CHROMATIC_KEYS

    chord_notes= [note,]
    c=1
    root_note_position = CHROMATIC_KEYS.index(note)

    while(len(chord_notes) < len(CHORDS_SEQUENCE_DICT[type])):
        chord_notes.append(cycle_list[root_note_position + CHORDS_SEQUENCE_DICT[type][c]])
        c += 1
    
    return chord_notes


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


def get_chords_of_scale(scale_key,scale_type):
    scale_notes = get_scale_notes(scale_key,scale_type)
        

    roman_letters = list(ROMAN_LETTERS_VALUE_DICT.keys())
    chords_numbers = list(ROMAN_LETTERS_VALUE_DICT.values())

    chords_dict = {}

    for counter in range(len(chords_numbers)):
        chord_num = chords_numbers[counter]
        roman_letter = roman_letters[counter]
        chords_dict[roman_letter] = get_chord_notes_by_num(scale_notes,chord_num)
        
    return chords_dict


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

    file_name = file_path + '\\' + "{basename}.{ext}".format(basename=basename, ext=ext)
    available_numbers_counter = count(2)

    while os.path.exists(file_name):
        file_name = file_path + '\\' + "{basename}_{number}.{ext}".format(basename=basename,
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
    diatonic_notes_deque = deque(CHROMATIC_KEYS)

    diatonic_notes_deque.rotate(12 - CHROMATIC_KEYS.index(scale_key))
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

    duration = int(requested_melody_length / 4)

    # Writing chords to the file
    for chord_notes in chords_list:
        for note in chord_notes:
            pitch = CHROMATIC_KEYS_PITCH_DICT[note]

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
            pitch = CHROMATIC_KEYS_PITCH_DICT[pitch_letter]

            # continuing from the preview note:
            note_time = current_melody_length

            duration = random.choice(NOTE_DURATIONS_LIST)
            if requested_melody_length - current_melody_length < min(NOTE_DURATIONS_LIST):
                break
            while duration > requested_melody_length - current_melody_length:
                duration = random.choice(NOTE_DURATIONS_LIST)

            # Adding the note to the Midi file:
            midi_file.addNote(melody_track, channel, pitch, note_time, duration, volume)

            current_melody_length += duration
            continue

        # if random_chance is between the 0.09 and 0.39 area its a
        # 30% chance and silence is added to the file:
        elif chance_for_rest > random_chance > chance_for_adding:
            # Adding rest (silence):
            duration_of_rest = random.choice(SILENCE_DURATIONS_LIST)
            if requested_melody_length - current_melody_length < min(SILENCE_DURATIONS_LIST):
                break

            while duration_of_rest > requested_melody_length - current_melody_length:
                duration_of_rest = random.choice(SILENCE_DURATIONS_LIST)

            current_melody_length += duration_of_rest
            continue

        #  Here it Adds an Adding:
        if random.choice([0, 1, 2, 3]) > 0:
            #  triplets of notes
            if requested_melody_length - current_melody_length < max(ADDINGS_DURATIONS_LIST):
                # calculating the remaining time left.
                break
            duration = random.choice(SILENCE_DURATIONS_LIST)
            for i in range(3):
                
                
                pitch_letter = random.choice(scale_notes)
                pitch = CHROMATIC_KEYS_PITCH_DICT[pitch_letter]

                # continuing from the preview note:
                note_time = current_melody_length
                # Adding the note to the Midi file:
                midi_file.addNote(melody_track, channel, pitch, note_time, duration, volume)

                current_melody_length += duration

            continue

        #  Pitch bend:
        pitch_quantity = random.choice(range(3000, 9000, 1000))  # range 3000 - 8000 in a 1000 jumps.
        MIDIFile.addPitchWheelEvent(midi_file, melody_track, channel, float(current_melody_length), pitch_quantity)


def play_midi_file(midi_file_path):
    """
    Playing a Midi file

    :param midi_file_path: The path of the MIDI file

    :return: None.
             Playing the file.

    """

    
    pass


def main(
    midi_file_path=os.getcwd(),scale_type=random.choice(list(SCALES_DICT.keys())),
    scale_key=random.choice(CHROMATIC_KEYS),chords_atmosphere=random.choice(list(ATMOSPHERE_DICT.keys())),
    melody_length=DEFAULT_MELODY_LENGTH,bpm=DEFAULT_BPM):
  
    """
    Main Function
    :return: New Midi File Path (The file has been created by the program), and the bytes file of Class "MidiFile" from MidiUtil module
    """
    
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

    new_midi_file_path = get_unique_file_name(midi_file_path, 'RandoMMelody', 'mid').replace("\\", "/")
    
    with open(new_midi_file_path, 'wb') as output_file:
        midi_file.writeFile(output_file)
        
    print("This is the Midi File Path: ",midi_file_path)
    return new_midi_file_path,midi_file
    # print('Your MIDI file is in : ' + midi_files_path + '\nBye!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=USER_INSTRUCTIONS_TEXT)
    parser.add_argument('-p', "--midi_file_path",  help="Path to save the midi files of the auto-generated music."
                                                         "default path - your current working directory.",
                        default=os.getcwd())
    parser.add_argument('-k', '--scale_key', help="the key of the scale", default=random.choice(CHROMATIC_KEYS))
    parser.add_argument('-t', '--scale_type', help="the type of the scale",
                        default=random.choice(list(SCALES_DICT.keys())))
    parser.add_argument('-a', '--chords_atmosphere', help="the atmosphere of the chord progression",
                        default=random.choice(list(ATMOSPHERE_DICT.keys())))
    parser.add_argument('-l', '--melody_length', help="the length of the melody", default=DEFAULT_MELODY_LENGTH)
    parser.add_argument('-b', '--bpm', help="the bpm of the melody", default=DEFAULT_BPM)

    args = parser.parse_args()
    midi_file_path = args.midi_file_path
    scale_type = args.scale_type
    scale_key = args.scale_key
    chords_atmosphere = args.chords_atmosphere
    melody_length = int(args.melody_length)
    bpm = int(args.bpm)

    main(midi_file_path,scale_type,scale_key,chords_atmosphere,melody_length,bpm)
