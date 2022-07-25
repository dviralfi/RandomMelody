# RandomMelody 
Automatic Music Maker :loud_sound:	

Written by *Dvir Alfi* .

### Developed to make music making easy and fast. :musical_score:
**Random Melody is an Automatic Music Maker for musicians, composers and everyone that loves and are fascinated by music**. :headphones: :microphone: :radio:

The program is written in Python and uses the Midiutil package for MIDI file manipulation.

It provides a MIDI file that contains chords :notes: and melody :musical_note: , written totally randomly by the program.

The MIDI file can easily be used by your favorite DAW[^1]. :control_knobs:

* If you don't have such program, you can use this website, where you can edit and hear the MIDI file: https://onlinesequencer.net/import

## Installation Guide 

`pip install git+https://github.com/dviralfi/RandomMelody.git` 

You can also clone/fork the repo and run it manually, dont forget to install requirements: `pip install -r requirements.txt`

#### Optional Arguments

You can choose various options for the program.

*The options you won't choose will be chosen randomly.*

When you execute the program at the command line you can pass it as arguments:

-  -p : Path to save the midi files
-  -k : Key of the scale
-  -t : Type of the scale
-  -a : Emotional Atmosphere of the chords progressions. (happy, pop, joyful, cheerful, dark, emotional, sad, confusing, crying, building)
-  -l : Length of the melody, Number of Beats
-  -b : Bpm of the melody in numbers

## Quick Start:

### Cloned installation

`random_melody_generator.py -p path/to/save/file -k G# -t minor -a happy -b 128`

### PIP installation

`from random_melody_module import random_melody_generator`

`random_melody_generator.main(
                file_name="myfile",
                chords_atmosphere="sad",
                scale_key="F",
                midi_file_path="path/to/save/file"
                )`


[^1]:DAW - Digital Audio Workstation
