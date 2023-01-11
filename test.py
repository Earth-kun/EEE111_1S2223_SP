import textwrap
import re

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
list_chords = chords.strip().split()

str_FullLyrics = ''
offset = 0

for idx, line in enumerate(list_EachLine_Lyric):          
    if idx == len(list_EachLine_Lyric) - 1:
        str_FullLyrics += line
    elif idx % 2 == 0:
        modified_line = line
        for i in range(len(re.findall(r'[1-9]', modified_line))):
            # print('offset = ' + str(offset) + '; i = ' + str(i) + '; line no. = ' + str(idx))
            if len(list_chords[i + offset - 1]) == 2 and i != 0:
                index = modified_line.find(r'\d')
                modified_line = modified_line[:index-1] + modified_line[index]
                modified_line = re.sub(r'[1-9]', list_chords[i + offset], modified_line, 1)
            elif len(list_chords[i + offset - 1]) == 3 and i != 0:
                index = modified_line.find(r'\d')
                modified_line = modified_line[:index-2] + modified_line[index]
                modified_line = re.sub(r'[1-9]', list_chords[i + offset], modified_line, 1)
            else:
                modified_line = re.sub(r'[1-9]', list_chords[i + offset], modified_line, 1)
        offset += len(re.findall(r'[1-9]', line))
        str_FullLyrics += modified_line + '\n'
    else:
        str_FullLyrics += line + '\n'

# print(str_FullLyrics)

int_Chord = 0

list_full = str_FullLyrics.strip().split('\n')

# for idx, line in enumerate(list1):
#     if idx % 2 == 0:
#         line_count = line.strip().split()
#         int_Chord += len(line_count)



list_entries = []
line_chord_dur = [x for idx, x in enumerate(list_EachLine_Lyric) if idx % 2 == 0 and x != '']
counter = 0

for idx, line in enumerate(line_chord_dur):
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

            chord_elements += [(list_chords[counter], chord_col, int(x))]
            counter += 1

    list_entries += [(list_EachLine_Lyric[(idx * 2) + 1], chord_elements)]


yee = ''

for idx, line in enumerate(list_EachLine_Lyric):          
    if idx == len(list_EachLine_Lyric) - 1:
        yee += line
    else:
        yee += line + '\n'

print(yee + ' yee')



