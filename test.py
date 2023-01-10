import textwrap

chords = 'A E C#m B\nA E C#m B\nA E C#m B\nA E C#m B\n'
text = textwrap.dedent("""\
        4       4           4
        Subukan ang manalangin
                    4
        Sana 'di magbago ang pagtingin
        4      4           4
        Baka bukas ika'y akin
                    4
        Sana 'di magbago ang pagtingin
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        """)

name = '[sample]'

list_EachLine_Lyric = text.strip().split('\n')
list_Chords = chords.strip().split()

str_FullLyrics = name + '\n'
counter = 0

for idx, line in enumerate(list_EachLine_Lyric):          
    if idx == len(list_EachLine_Lyric) - 1:
        str_FullLyrics += line
    elif idx % 2 == 0:
        import re
        modified_line = line.replace('4', list_Chords[0]) # re.sub(r'[12348]', list_Chords[counter], line)
        counter += 1
        str_FullLyrics += modified_line + '\n'
    else:
        str_FullLyrics += line + '\n'
        
# print(str_FullLyrics)