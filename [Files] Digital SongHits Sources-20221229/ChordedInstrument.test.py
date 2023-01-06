import unittest
import uke

class ChordedInstrument_SplitChordTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()

    def assert_splitChordsTrue(self, ans_map):
        for t_in, t_outs in ans_map:
            split_chord = self.ci_std.split_chord(t_in)
            self.assertTrue(any([x == split_chord for x in t_outs]))

    def test_basic(self):
        ans_map = [
            ['A', [('A', '', '')]],
            ['D', [('D', '', '')]],
        ]

        self.assert_splitChordsTrue(ans_map)

    def test_accidentalSharp(self):
        ans_map = [
            ['F#', [('F', '#', '')]],
            ['G#', [('G', '#', '')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_accidentalFlat(self):
        ans_map = [
            ['Eb', [('E', 'b', '')]],
            ['Gb', [('G', 'b', '')]],
        ]

        self.assert_splitChordsTrue(ans_map)

    def test_noAccidental_pt1(self):
        ans_map = [
            ['C', [('C', '', '')]],
            ['CM', [('C', '', 'M')]],
            ['CMaj', [('C', '', 'Maj')]],
            ['Fm', [('F', '', 'm')]],
            ['Fmin', [('F', '', 'min')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_noAccidental_pt2(self):
        ans_map = [
            ['Asus', [('A', '', 'sus')]],
            ['Asus4', [('A', '', 'sus4')]],
            ['Asus2', [('A', '', 'sus2')]],
            ['D+', [('D', '', '+')]],
            ['Daug', [('D', '', 'aug')]],
            ['Bdim', [('B', '', 'dim')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_noAccidental_pt3(self):
        ans_map = [
            ['E7', [('E', '', '7')]],
            ['DM7', [('D', '', 'M7')]],
            ['DMaj7', [('D', '', 'Maj7')]],
            ['Am7', [('A', '', 'm7')]],
            ['Amin7', [('A', '', 'min7')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_withAccidental_pt1(self):
        ans_map = [
            ['C#', [('C', '#', '')]],
            ['C#M', [('C', '#', 'M')]],
            ['C#Maj', [('C', '#', 'Maj')]],
            ['F#m', [('F', '#', 'm')]],
            ['F#min', [('F', '#', 'min')]],
            ['Bb', [('B', 'b', '')]],
            ['BbM', [('B', 'b', 'M')]],
            ['BbMaj', [('B', 'b', 'Maj')]],
            ['Fbm', [('F', 'b', 'm')]],
            ['Fbmin', [('F', 'b', 'min')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_withAccidental_pt2(self):
        ans_map = [
            ['A#sus', [('A', '#', 'sus')]],
            ['A#sus4', [('A', '#', 'sus4')]],
            ['A#sus2', [('A', '#', 'sus2')]],
            ['D#+', [('D', '#', '+')]],
            ['D#aug', [('D', '#', 'aug')]],
            ['C#dim', [('C', '#', 'dim')]],
            ['Absus', [('A', 'b', 'sus')]],
            ['Absus4', [('A', 'b', 'sus4')]],
            ['Absus2', [('A', 'b', 'sus2')]],
            ['Db+', [('D', 'b', '+')]],
            ['Dbaug', [('D', 'b', 'aug')]],
            ['Bbdim', [('B', 'b', 'dim')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_withAccidental_pt3(self):
        ans_map = [
            ['F#7', [('F', '#', '7')]],
            ['D#M7', [('D', '#', 'M7')]],
            ['D#Maj7', [('D', '#', 'Maj7')]],
            ['A#m7', [('A', '#', 'm7')]],
            ['A#min7', [('A', '#', 'min7')]],
            ['Eb7', [('E', 'b', '7')]],
            ['DbM7', [('D', 'b', 'M7')]],
            ['DbMaj7', [('D', 'b', 'Maj7')]],
            ['Abm7', [('A', 'b', 'm7')]],
            ['Abmin7', [('A', 'b', 'min7')]],
        ]

        self.assert_splitChordsTrue(ans_map)
    
    def test_raises(self):
        with self.assertRaises(ValueError):
            self.ci_std.split_chord('')
            
        with self.assertRaises(ValueError):
            self.ci_std.split_chord('         ')

        with self.assertRaises(ValueError):
            self.ci_std.split_chord('Hmin')
        
        with self.assertRaises(ValueError):
            self.ci_std.split_chord('This is a random string')
        
        with self.assertRaises(ValueError):
            self.ci_std.split_chord('Cmaj7b9')

class ChordedInstrument_SupportedChordsTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()
        self.base_chord_set = {
            '', 'M', 'Maj', 'm', 'min',
            '7', 'M7', 'Maj7', 'm7', 'min7',
            'sus4', 'sus', 'sus2', 'dim', 'aug',
            '+',
        }
    
    def test_baseChords(self):
        supported_chords = self.ci_std.supported_chords()
        self.assertTrue(self.base_chord_set <= set(supported_chords))

class ChordedInstrument_TransposeTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()
    
    def assert_transposeTrue(self, ans_map):
        for t_in, t_outs in ans_map:
            transed_chord = self.ci_std.transpose_chord(t_in[0], t_in[1])
            self.assertTrue(any([x == transed_chord for x in t_outs]))
    
    def test_basicPos(self):
        ans_map = [
            [('A', 1), ['A#']],
            [('G', 2), ['A']],
            [('B', 1), ['C']],
            [('F#', 5), ['B']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_basicNeg(self):
        ans_map = [
            [('A', -1), ['G#']],
            [('G', -2), ['F']],
            [('C', -1), ['B']],
            [('F#', -5), ['C#']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_basicLargeSemitones(self):
        ans_map = [
            [('A', 12), ['A']],
            [('G', -12), ['G']],
            [('C', 13), ['C#']],
            [('F#', -17), ['C#']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_basicNone(self):
        ans_map = [
            [('A', 0), ['A']],
            [('G', 0), ['G']],
            [('Bb', 0), ['Bb']],
            [('F#', 0), ['F#']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_withTypes_pt1(self):
        ans_map = [
            [('A', 1), ['A#']],
            [('GMaj', 3), ['A#Maj']],
            [('Cm', -5), ['Gm']],
            [('Dmin', -7), ['Gmin']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_withTypes_pt2(self):
        ans_map = [
            [('A+', 12), ['A+']],
            [('Gmin7', -1), ['F#min7']],
            [('C7', 4), ['E7']],
            [('Dsus4', -2), ['Csus4']],
        ]

        self.assert_transposeTrue(ans_map)
    
    def test_flats(self):
        ans_map = [
            [('Ab', 12), ['Ab']],
            [('Ebdim', -1), ['Ddim']],
            [('Gb7', 5), ['B7']],
            [('Bb+', -2), ['Ab+']],
            [('DbMaj7', -15), ['BbMaj7']],
        ]

        self.assert_transposeTrue(ans_map)

class ChordedInstrument_ChromaScaleTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()
    
    def assert_chromaScaleTrue(self, ans_map):
        for t_in, t_out in ans_map:
            chroma_scale = self.ci_std.gen_chroma_scale(base_note=t_in)
            self.assertEqual(chroma_scale, t_out)
    
    def test_base(self):
        test_ans = self.ci_std.gen_chroma_scale()
        ref_ans = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        self.assertEqual(test_ans, ref_ans)
    
    def test_movable(self):
        ans_map = [
            ('G', ['G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#']),
            ('C', ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']),
            ('F', ['F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E']),
        ]

        self.assert_chromaScaleTrue(ans_map)
    
    def test_sharps(self):
        ans_map = [
            ('G#', ['G#', 'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']),
            ('C#', ['C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'C']),
            ('A#', ['A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A']),
        ]

        self.assert_chromaScaleTrue(ans_map)
    
    def test_flats(self):
        ans_map = [
            ('Gb', ['Gb', 'G', 'Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F']),
            ('Bb', ['Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A']),
            ('Ab', ['Ab', 'A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G']),
        ]

        self.assert_chromaScaleTrue(ans_map)

    def test_invalid(self):
        ans_map = [
            ('Gb7', []),
            ('Hb', []),
            ('This is a random string', []),
        ]

        self.assert_chromaScaleTrue(ans_map)

class ChordedInstrument_NotesFromIntervalsTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()
    
    def assert_notesFromIntervalsTrue(self, ans_map):
        for t_in, t_out in ans_map:
            chroma_scale = self.ci_std.get_notes_from_intervals(t_in[0], t_in[1])
            self.assertEqual(chroma_scale, t_out)
    
    def test_basic(self):
        ans_map = [
            (('A', [0, 1, 2]), ('A', 'A#', 'B')),
            (('F', [0, 3, 4]), ('F', 'G#', 'A')),
            (('D', [0, 4, 5]), ('D', 'F#', 'G')),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)
    
    def test_offset(self):
        ans_map = [
            (('C', [3, 4, 5]), ('D#', 'E', 'F')),
            (('E', [1, 3, 5]), ('F', 'G', 'A')),
            (('G', [5, 6, 8]), ('C', 'C#', 'D#')),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)
    
    def test_sharps(self):
        ans_map = [
            (('C#', [0, 4, 5]), ('C#', 'F', 'F#')),
            (('F#', [0, 3, 5]), ('F#', 'A', 'B')),
            (('G#', [0, 6, 8]), ('G#', 'D', 'E')),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)

    def test_flats(self):
        ans_map = [
            (('Bb', [0, 4, 5]), ('Bb', 'D', 'Eb')),
            (('Eb', [0, 3, 5]), ('Eb', 'Gb', 'Ab')),
            (('Gb', [0, 6, 8]), ('Gb', 'C', 'D')),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)

    def test_singleElm(self):
        ans_map = [
            (('A', [0]), ('A',)),
            (('F', [3]), ('G#',)),
            (('D', [12]), ('D',)),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)
    
    def test_none(self):
        ans_map = [
            (('A', []), ()),
            (('F', []), ()),
            (('D', []), ()),
        ]

        self.assert_notesFromIntervalsTrue(ans_map)

class ChordedInstrument_ChordNotesTest(unittest.TestCase):
    def setUp(self):
        self.ci_std = uke.ChordedInstrument()
    
    def assert_chordNotesTrue(self, ans_map):
        for t_in, t_out in ans_map:
            chroma_scale = self.ci_std.get_chord_notes(t_in)
            self.assertEqual(chroma_scale, t_out)

    def test_noAccidental_pt1(self):
        ans_map = [
            ['C', ('C', 'E', 'G')],
            ['CM', ('C', 'E', 'G')],
            ['CMaj', ('C', 'E', 'G')],
            ['Fm', ('F', 'G#', 'C')],
            ['Fmin', ('F', 'G#', 'C')],
        ]

        self.assert_chordNotesTrue(ans_map)

    def test_noAccidental_pt2(self):
        ans_map = [
            ['Asus', ('A', 'D', 'E')],
            ['Asus4', ('A', 'D', 'E')],
            ['Asus2', ('A', 'B', 'E')],
            ['D+', ('D', 'F#', 'A#')],
            ['Daug', ('D', 'F#', 'A#')],
            ['Bdim', ('B', 'D', 'F')],
        ]

        self.assert_chordNotesTrue(ans_map)
    
    def test_noAccidental_pt3(self):
        ans_map = [
            ['E7', ('E', 'G#', 'B', 'D')],
            ['DM7', ('D', 'F#', 'A', 'C#')],
            ['DMaj7', ('D', 'F#', 'A', 'C#')],
            ['Am7', ('A', 'C', 'E', 'G')],
            ['Amin7', ('A', 'C', 'E', 'G')],
        ]

        self.assert_chordNotesTrue(ans_map)
    
    def test_withAccidental_pt1(self):
        ans_map = [
            ['C#', ('C#', 'F', 'G#')],
            ['C#M', ('C#', 'F', 'G#')],
            ['C#Maj', ('C#', 'F', 'G#')],
            ['F#m', ('F#', 'A', 'C#')],
            ['F#min', ('F#', 'A', 'C#')],
            ['Bb', ('Bb', 'D', 'F')],
            ['BbM', ('Bb', 'D', 'F')],
            ['BbMaj', ('Bb', 'D', 'F')],
            ['Gbm', ('Gb', 'A', 'Db')],
            ['Gbmin', ('Gb', 'A', 'Db')],
        ]

        self.assert_chordNotesTrue(ans_map)
    
    def test_withAccidental_pt2(self):
        ans_map = [
            ['A#sus', ('A#', 'D#', 'F')],
            ['A#sus4', ('A#', 'D#', 'F')],
            ['A#sus2', ('A#', 'C', 'F')],
            ['D#+', ('D#', 'G', 'B')],
            ['D#aug', ('D#', 'G', 'B')],
            ['C#dim', ('C#', 'E', 'G')],
            ['Absus', ('Ab', 'Db', 'Eb')],
            ['Absus4', ('Ab', 'Db', 'Eb')],
            ['Absus2', ('Ab', 'Bb', 'Eb')],
            ['Db+', ('Db', 'F', 'A')],
            ['Dbaug', ('Db', 'F', 'A')],
            ['Bbdim', ('Bb', 'Db', 'E')],
        ]

        self.assert_chordNotesTrue(ans_map)
    
    def test_withAccidental_pt3(self):
        ans_map = [
            ['F#7', ('F#', 'A#', 'C#', 'E')],
            ['D#M7', ('D#', 'G', 'A#', 'D')],
            ['D#Maj7', ('D#', 'G', 'A#', 'D')],
            ['A#m7', ('A#', 'C#', 'F', 'G#')],
            ['A#min7', ('A#', 'C#', 'F', 'G#')],
            ['Eb7', ('Eb', 'G', 'Bb', 'Db')],
            ['DbM7', ('Db', 'F', 'Ab', 'C')],
            ['DbMaj7', ('Db', 'F', 'Ab', 'C')],
            ['Abm7', ('Ab', 'B', 'Eb', 'Gb')],
            ['Abmin7', ('Ab', 'B', 'Eb', 'Gb')],
        ]

        self.assert_chordNotesTrue(ans_map)

    def test_raises(self):
        with self.assertRaises(ValueError):
            self.ci_std.get_chord_notes('')
            
        with self.assertRaises(ValueError):
            self.ci_std.get_chord_notes('         ')

        with self.assertRaises(ValueError):
            self.ci_std.get_chord_notes('Hmin')
        
        with self.assertRaises(ValueError):
            self.ci_std.get_chord_notes('This is a random string')
        
        with self.assertRaises(ValueError):
            self.ci_std.get_chord_notes('Cmaj7b9')

if __name__ == '__main__':
    unittest.main()