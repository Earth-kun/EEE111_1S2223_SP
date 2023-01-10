from sox import sox

# Generate a ukulele Am7 chord
notes = ['G', 'C', 'E', 'A']
octaves = [4, 4, 4, 4]

# Will create "chord_sample.ogg" in the current directory
# where this script was run
out_file_path = sox.gen_chord_sample(notes, octaves)