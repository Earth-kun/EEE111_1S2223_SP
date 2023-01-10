import unittest
import song

class LyricSegment_InitTest(unittest.TestCase):
    def test_basic(self):
        obj_a = song.LyricSegment('Verse 1', 'Dami pang gustong sabihin\nNgunit \'wag na lang muna')

        self.assertEqual(obj_a.name, 'Verse 1')
        self.assertEqual(obj_a.text, ['Dami pang gustong sabihin', 'Ngunit \'wag na lang muna'])

    def test_str(self):
        obj_a = song.LyricSegment('Verse 1', 'Dami pang gustong sabihin\nNgunit \'wag na lang muna')

        self.assertEqual(obj_a.name, 'Verse 1')
        self.assertEqual(obj_a.text, ['Dami pang gustong sabihin', 'Ngunit \'wag na lang muna'])
        self.assertEqual(str(obj_a), '[Verse 1]\nDami pang gustong sabihin\nNgunit \'wag na lang muna')
    
    def test_str_chorded(self):
        obj_a = song.LyricSegment('Chorus', 'G       D            Bm\n\'Pag nilahad ang damdamin\n             A\nSana \'di magbago ang pagtingin')

        self.assertEqual(obj_a.name, 'Chorus')
        self.assertEqual(obj_a.text, ['G       D            Bm', '\'Pag nilahad ang damdamin', '             A', 'Sana \'di magbago ang pagtingin'])
        self.assertEqual(str(obj_a), '[Chorus]\nG       D            Bm\n\'Pag nilahad ang damdamin\n             A\nSana \'di magbago ang pagtingin')

if __name__ == '__main__':
    unittest.main()