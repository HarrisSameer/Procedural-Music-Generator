import random

from composing import Song, Percussion, Instrument, Scale, Chord, note2number, number2note
import numpy as np
import os
from play_midi import play_midi


def run():
    song_path = generate_song()
    # Uncomment to play the song in a blocking fashion
    # play_midi(song_path)


def generate_song():
    random_seed = random.randint(1, 100000)
    random.seed(random_seed)

    song = Song(120)

    bass_track = song.new_track(Instrument.BASS_SYNTH_2)
    bass_pattern = generate_procedural_bass()
    for i, note in enumerate(bass_pattern):
        bass_track.add_note(note, i * 2, 2)

    melody_track = song.new_track(Instrument.FLUTE)
    melody_pattern = generate_procedural_melody()
    for i, note in enumerate(melody_pattern):
        melody_track.add_note(note, i, 2)

    chords_track = song.new_track(Instrument.CELLO)
    chords_pattern = generate_procedural_chords(melody_pattern)
    for i, chord in enumerate(chords_pattern):
        chords_track.add_chord(chord, i * 2, 4)

    if not os.path.exists('out'):
        os.mkdir('out')
    song_path = 'out/song.mid'
    song.save(song_path)

    print('Generated song:', song_path)
    return song_path

def generate_procedural_bass():
    pattern = [random.randint(30, 50) for _ in range(8)]
    return pattern

def generate_procedural_melody():
    pattern = [random.randint(55, 67) for _ in range(8)]
    return pattern

def generate_procedural_chords(melody_pattern):
    chords = []
    for i, note in enumerate(melody_pattern):
        if i % 4 == 0:
            chord = Chord.MAJOR.start_from(note)
        elif i % 4 == 2:
            chord = Chord.MINOR.start_from(note)
        else:
            chord = Chord.MAJOR.start_from(note)
        chords.append(chord)
    return chords




def name_from_seed(seed):
    with open('assets/nouns.txt') as f:
        nouns = [s.strip() for s in f.readlines()]
    with open('assets/adjectives.txt') as f:
        adjectives = [s.strip() for s in f.readlines()]
    noun = nouns[seed % 1000]
    adjective = adjectives[seed // 1000]
    return '{}_{}'.format(adjective, noun)


if __name__ == '__main__':
    run()
