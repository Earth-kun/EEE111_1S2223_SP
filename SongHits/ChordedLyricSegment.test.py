import unittest
import textwrap
import song

class ChordedLyricSegment_InitTest(unittest.TestCase):
    def test_basic(self):
        text_in = textwrap.dedent("""\
        4        4             4
        'Pag nilahad ang damdamin
                    4
        Sana 'di magbago ang pagtingin
        """)

        obj_a = song.ChordedLyricSegment('Chorus', text_in, chords='G D Bm A')

        self.assertEqual(obj_a.name, 'Chorus')
        self.assertEqual(obj_a.text, ['\'Pag nilahad ang damdamin', 'Sana \'di magbago ang pagtingin'])
        self.assertEqual(obj_a.chords, ['G', 'D', 'Bm', 'A'])

    def test_full(self):
        text_in = textwrap.dedent("""\
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        """)

        obj_a = song.ChordedLyricSegment('Chorus 2', text_in, chords='A E C#m B\n\n A E C#m B')
        self.assertEqual(obj_a.name, 'Chorus 2')
        self.assertEqual(obj_a.text, ['Pahiwatig', 'Sana \'di magbago ang pagtingin', 'Pahiwatig', 'Sana \'di magbago ang pagtingin'])
        self.assertEqual(obj_a.chords, ['A', 'E', 'C#m', 'B', 'A', 'E', 'C#m', 'B'])


class ChordedLyricSegment_LenTest(unittest.TestCase):
    def test_basic(self):
        text_in = textwrap.dedent("""\
        4        4             4
        'Pag nilahad ang damdamin
                    4
        Sana 'di magbago ang pagtingin
        """)

        obj_a = song.ChordedLyricSegment('Chorus', text_in, chords='G D Bm A')

        self.assertEqual(len(obj_a), 4)
    
    def test_fullPt1(self):
        text_in = textwrap.dedent("""\
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        4   4
        Pahiwatig
        4           4
        Sana 'di magbago ang pagtingin
        """)

        obj_a = song.ChordedLyricSegment('Chorus 2', text_in, chords='A E C#m B\n\n A E C#m B')

        self.assertEqual(len(obj_a), 8)

    def test_fullPt2(self):
        text_in = textwrap.dedent("""\
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

        obj_a = song.ChordedLyricSegment('Chorus 2', text_in, chords='A E C#m B\nA E C#m B\nA E C#m B\nA E C#m B\n')
        self.assertEqual(len(obj_a), 16)


class ChordedLyricSegment_StrTest(unittest.TestCase):
    def test_basic(self):
        text_in = textwrap.dedent("""\
        4        4             4
        'Pag nilahad ang damdamin
                    4
        Sana 'di magbago ang pagtingin
        """)

        text_out = textwrap.dedent("""\
        [Chorus]
        G        D             Bm
        'Pag nilahad ang damdamin
                    A
        Sana 'di magbago ang pagtingin
        """).rstrip('\r\n')

        obj_a = song.ChordedLyricSegment('Chorus', text_in, chords='G D Bm A')

        self.assertEqual(obj_a.name, 'Chorus')
        self.assertEqual(obj_a.text, ['\'Pag nilahad ang damdamin', 'Sana \'di magbago ang pagtingin'])
        self.assertEqual(obj_a.chords, ['G', 'D', 'Bm', 'A'])
        self.assertEqual(str(obj_a), text_out)
    
    def test_full(self):
        text_in = textwrap.dedent("""\
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

        text_out = textwrap.dedent("""\
        [Chorus 2]
        A       E           C#m
        Subukan ang manalangin
                    B
        Sana 'di magbago ang pagtingin
        A      E           C#m
        Baka bukas ika'y akin
                    B
        Sana 'di magbago ang pagtingin
        A   E
        Pahiwatig
        C#m         B
        Sana 'di magbago ang pagtingin
        A   E
        Pahiwatig
        C#m         B
        Sana 'di magbago ang pagtingin
        """).rstrip('\r\n')

        obj_a = song.ChordedLyricSegment('Chorus 2', text_in, chords='A E C#m B\nA E C#m B\nA E C#m B\nA E C#m B\n')

        self.assertEqual(obj_a.name, 'Chorus 2')
        self.assertEqual(obj_a.text, [
            'Subukan ang manalangin',
            'Sana \'di magbago ang pagtingin',
            'Baka bukas ika\'y akin',
            'Sana \'di magbago ang pagtingin',
            'Pahiwatig',
            'Sana \'di magbago ang pagtingin',
            'Pahiwatig',
            'Sana \'di magbago ang pagtingin'
        ])
        self.assertEqual(str(obj_a), text_out)


class ChordedLyricSegment_EntriesTest(unittest.TestCase):
    def test_singleLinePt1(self):
        text_in = textwrap.dedent("""\
        4        4             4
        'Pag nilahad ang damdamin
        """)

        obj_a = song.ChordedLyricSegment('Chorus', text_in, chords='G D Bm')
        self.assertEqual(list(obj_a.entries()), [('\'Pag nilahad ang damdamin', [('G', 0, 4), ('D', 9, 4), ('Bm', 23, 4)])])

    def test_singleLinePt2(self):
        text_in = textwrap.dedent("""\
                            4     4
        Dami pang gustong sabihin
        """)

        obj_a = song.ChordedLyricSegment('Verse I', text_in, chords='G A')
        self.assertEqual(list(obj_a.entries()), [('Dami pang gustong sabihin', [('G', 20, 4), ('A', 26, 4)])])
    
    def test_singleLinePt2(self):
        text_in = textwrap.dedent("""\
                            4     4
        Dami pang gustong sabihin
        """)

        obj_a = song.ChordedLyricSegment('Verse I', text_in, chords='G A')
        self.assertEqual(list(obj_a.entries()), [('Dami pang gustong sabihin', [('G', 20, 4), ('A', 26, 4)])])

    def test_singleLinePt3(self):
        text_in = textwrap.dedent("""\
        4                        4
          And you stood there in front of me just
        """)

        obj_a = song.ChordedLyricSegment('Pre-Chorus', text_in, chords='A#  C ')
        self.assertEqual(list(obj_a.entries()), [('  And you stood there in front of me just', [('A#', 0, 4), ('C', 25, 4)])])

    def test_multiLinePt1(self):
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

        obj_a = song.ChordedLyricSegment('Verse', text_in, chords='A F#m D E\nA F#m D E')
        self.assertEqual(list(obj_a.entries()), [
            ('Huwag nang mag-alinlangan pa', [('A', 0, 4), ('F#m', 19, 4)]),
            ('Kung gusto mo ako lumapit ka', [('D', 11, 4), ('E', 20, 4)]),
            ('Huwag nang patorpe-torpe pa', [('A', 0, 4), ('F#m', 19, 4)]),
            ('Minsan tuloy ako\'y naiinis na', [('D', 9, 4), ('E', 21, 4)]),
        ])

    def test_multiLinePt2(self):
        text_in = textwrap.dedent("""\
           2      2      4
        Suiran wo hen ai ni
           2      2  4
        Wo mei fenfa gaosu ni
           2        2    2     1   1
        Wo xinzhong yi you qingai
           2       2     4
        Danshi shi wo de ai
        """)

        obj_a = song.ChordedLyricSegment('Verse', text_in, chords='Db Eb Fm\nDb Eb Fm\nDb Eb Ab Fm Eb\nDb Eb Ab')
        self.assertEqual(list(obj_a.entries()), [
            ('Suiran wo hen ai ni', [('Db', 3, 2), ('Eb', 10, 2), ('Fm', 17, 4)]),
            ('Wo mei fenfa gaosu ni', [('Db', 3, 2), ('Eb', 10, 2), ('Fm', 13, 4)]),
            ('Wo xinzhong yi you qingai', [('Db', 3, 2), ('Eb', 12, 2), ('Ab', 17, 2), ('Fm', 23, 1), ('Eb', 27, 1)]),
            ('Danshi shi wo de ai', [('Db', 3, 2), ('Eb', 11, 2), ('Ab', 17, 4)]),
        ])
    
    def test_multiLinePt3(self):
        text_in = textwrap.dedent("""\
        8
        Water pouring down from the ceiling
                          8
        I knew this would happen, still hard to believe it
                     8
        Maybe I'm dramatic, I don't wanna seem it
                      8
        I don't wanna panic (Ooh, ooh, ooh)
        """)

        obj_a = song.ChordedLyricSegment('Verse', text_in, chords='GM7 Am7 GM7 Am7')
        self.assertEqual(list(obj_a.entries()), [
            ('Water pouring down from the ceiling', [('GM7', 0, 8)]),
            ('I knew this would happen, still hard to believe it', [('Am7', 18, 8)]),
            ('Maybe I\'m dramatic, I don\'t wanna seem it', [('GM7', 13, 8)]),
            ('I don\'t wanna panic (Ooh, ooh, ooh)', [('Am7', 14, 8)]),
        ])

if __name__ == '__main__':
    unittest.main()