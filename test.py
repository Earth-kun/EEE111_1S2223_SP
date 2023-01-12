import textwrap
import re
import yaml
import os 
from pathlib import Path

chords='A F#m D E\nA F#m D E'
text_in = textwrap.dedent("""\
4                  4
Huwag nang mag-alinlangan pa
            4        4
Kung gusto mo ako lumapit ka
4                  4
Huwag nang patorpe-torpe pa
            4           4
Minsan tuloy ako'y naiinis na
""")

name = '[sample]'

list_EachLine_Lyric = text_in.strip().split('\n')
chords = chords.strip().split()

full_text = text_in.split('\n')

text = []
for idx, line in enumerate(full_text):
    if idx % 2 != 0:
        text += [line]

chord_annotations = []
for idx, line in enumerate(full_text):
    if idx % 2 == 0 and line != '':
        chord_annotations += [line]

def str(str_ChordedLyrics = '', offset = 0):
    for line_index, line_chord in enumerate(chord_annotations):
        modified_line = line_chord
        for num_chord in range(len(re.findall(r'[1-9]', modified_line))):
            if len(chords[num_chord + offset - 1]) == 2 and num_chord != 0:
                index = modified_line.find(r'\d')
                modified_line = modified_line[:index-1] + modified_line[index]
                modified_line = re.sub(r'[1-9]', chords[num_chord + offset], modified_line, 1)
            elif len(chords[num_chord + offset - 1]) == 3 and num_chord != 0:
                index = modified_line.find(r'\d')
                modified_line = modified_line[:index-2] + modified_line[index]
                modified_line = re.sub(r'[1-9]', chords[num_chord + offset], modified_line, 1)
            else:
                modified_line = re.sub(r'[1-9]', chords[num_chord + offset], modified_line, 1)
        offset += len(re.findall(r'[1-9]', line_chord))
        str_ChordedLyrics += modified_line + '\n'
        str_ChordedLyrics += text[line_index].strip() + '\n'
    return str_ChordedLyrics.strip()

def entries(list_entries = [], counter = 0):
    for idx, line in enumerate(chord_annotations):
        list_dur = line.strip().split()
        
        chord_elements = []
        temp = line
        offset = 0

        for x in list_dur:
            chord_col_temp = re.search(r'[1-9]', temp)
            if chord_col_temp is not None:
                chord_col_temp = chord_col_temp.start()
                chord_col = (chord_col_temp + offset)

                temp = temp[chord_col_temp + 1:]
                offset += chord_col_temp + 1

                chord_elements += [(chords[counter], chord_col, int(x))]
                counter += 1

        list_entries += [(list_EachLine_Lyric[(idx * 2) + 1], chord_elements)]
    return list_entries

#------------------------------------------------------------------------
print(str())
#---------------------------------------------------------------------------------

file_path = './ChordFiles/everytime_we_touch.crd.yaml'

if os.path.isfile(file_path):
    with open(file_path, 'r') as fh:
        song_dict = yaml.safe_load(fh)

