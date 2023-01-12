import re
import yaml
import os 
from pathlib import Path

class LyricSegment:
    """Represents a lyric segment

    Songs in general consist of several segments with labels
    pertaining to the different parts of the song. Segment
    names include the chorus, refrain, and verses. This class
    represents one of these segments.
    """
    def __init__(self, name: str, text: str):
        """Instantiate an object of this class

        This method will instantiate a new :py:class:`LyricSegment`
        object with the given ``name`` and ``text``.

        Objects of this class have only the following properties:
        * name
        * text

        :param name: name of the lyric segment
        :type name: str
        :param text: lyrics of the segment
        :type text: str
        """
        self.name = name
        self.text = text.split('\n')

    def __str__(self):
        """Return a string representation of this lyric segment

        This method will return a string of the following format::

            [<segment_name>]
            <segment_lyrics>

        :return: the lyrics with the segment name and content
        :rtype: str
        """
        str_lyrics = ''
        for idx, line in enumerate(self.text):
            if idx == len(self.text) - 1:
                str_lyrics += line
            else:
                str_lyrics += line + '\n'
        return f'[{self.name}]\n{str_lyrics}'

class ChordedLyricSegment(LyricSegment):
    """Represents a chorded lyric segment

    This class is also a :py:class:`LyricSegment` but
    also contains chord annotations. These annotations are
    placed on top of the lyrics, with the chords over
    the syllable where such a chord should be played.
    """
    def __init__(self, name: str, text: str, chords: str=''):
        """Instantiate an object of this class

        This method will instantiate a new :py:class:`ChordedLyricSegment`
        object with the given ``name``, ``text``, and ``chords``.
        The ``chords`` can be separated by newlines or spaces while the
        ``text`` will contain, in every newline, an alternating sequence
        of chord annotations and lyrics. The number of lines in ``text``
        should always be even.

        Objects of this class have only the following properties:
        * name
        * text
        * chords

        :param name: name of the lyric segment
        :type name: str
        :param text: lyrics of the segment
        :type text: list[str]
        :param chords: list containing each accompanying chords of the segment
        :type chords: list[str]
        """
        super().__init__(name, text)
        self.full_lyrics = self.text
        self.chords = chords.strip().split()

        self.text = []
        for idx, line in enumerate(self.full_lyrics):
            if idx % 2 != 0:
                self.text += [line]

        self.chord_annotations = []
        for idx, line in enumerate(self.full_lyrics):
            if idx % 2 == 0 and line != '':
                self.chord_annotations += [line]

    def __len__(self):
        """Count the number of chords in this lyric segment

        :return: number of chords in this lyric segment
        :rtype: int
        """
        return len(self.chords)

    def __str__(self):
        """Return a string representation of this lyric segment

        This method will return a string of the following format::

            [<segment_name>]
            <segment_lyrics>

        Unlike a :py:class:LyricSegment, ``<segment_lyrics>`` contains
        both the lyrics and the corresponding chord placements on top
        of each lyric line. Hence, the number of lines in ``<segment_lyrics>``
        should be even.

        :return: the lyrics with the segment name and content
        :rtype: str
        """
        str_ChordedLyrics = f'[{self.name}]' + '\n'
        offset = 0

        for line_index, line_chord in enumerate(self.chord_annotations):
            modified_line = line_chord
            for num_chord in range(len(re.findall(r'(?<!\w)\d+(?!\w)', modified_line))):
                if len(self.chords[num_chord + offset - 1]) > 1 and num_chord != 0:
                    index = modified_line.find(r'(?<!\w)\d+(?!\w)')
                    modified_line = modified_line[:index - len(self.chords[num_chord + offset - 1]) + 1] + modified_line[index]
                    modified_line = re.sub(r'(?<!\w)\d+(?!\w)', self.chords[num_chord + offset], modified_line, 1)                 
                else:
                    modified_line = re.sub(r'(?<!\w)\d+(?!\w)', self.chords[num_chord + offset], modified_line, 1)
            offset += len(re.findall(r'(?<!\w)\d+(?!\w)', line_chord))
            str_ChordedLyrics += modified_line + '\n'
            str_ChordedLyrics += self.text[line_index].strip() + '\n'
        
        return str_ChordedLyrics.strip()
    
    def entries(self):
        """Generate a "list" of lyrics and corresponding chords in the :py:class:`Song`

        The method returns an ``Iterable``, which can be converted to
        a ``list`` or sequence appropriately. The resulting ``list``
        should contain a tuple(str, list), with each element denoting
        a line in the song. For each element, the first element contains
        the lyrics and the second element contains a list of positions and chords
        of the corresponding lyrics ``chord_list``. Each element of ``chord_list``
        is a tuple of three elements (``chord_name``, ``chord_col``, ``chord_dur``)
        corresponding to the chord name, column from the leftmost edge of the
        lyrics (from zero), and duration of the chord.

        This method is usually used if we want to iterate through
        each lyric line with its chord information already bundled.

        :return: an ``Iterable`` object, with each element
            containing a tuple
        :rtype: Iterable[tuple[str, list[str, int, int]]]
        """
        list_entries = []
        counter = 0
        # list_EachLine_Lyric = str(self).split('\n')
        # line_chord_dur = [x for idx, x in enumerate(self.full) if idx % 2 == 0 and x != '']
        
        for idx, line in enumerate(self.chord_annotations):
            list_dur = line.strip().split()
            
            chord_elements = []
            temp = line
            offset = 0

            for x in list_dur:
                chord_col_temp = re.search(r'(?<!\w)\d+(?!\w)', temp)
                if chord_col_temp is not None:
                    chord_col_temp = chord_col_temp.start()
                    chord_col = (chord_col_temp + offset)

                    temp = temp[chord_col_temp + 1:]
                    offset += chord_col_temp + 1

                    chord_elements += [(self.chords[counter], chord_col, int(x))]
                    counter += 1

            list_entries += [(self.text[idx], chord_elements)]

        return list_entries

class Song:
    """Represents a song

    A song consists of several :py:class:`ChordedLyricSegment`s
    that can appear in any arbitrary order and possibly
    repetitively across the song. It also has some "metadata"
    to display how a song should be played or how should it
    be named.
    """
    def __init__(self, title: str, artist: str, file_path: str=None):
        """Instantiate an object of this class

        This method will instantiate a new :py:class:`Song`
        object with the given ``title``, ``artist``, and ``file_path``.
        The ``file_path`` is a path to the ``.crd.yaml`` file containing
        the song.

        Objects of this class have only the following properties:
        * title
        * artist
        * bpm - int of the beats per minute (speed) the song should
          be played against
        * lyrics_order - list[int] of song segment names depicting
          the order in which each segment appears in the song
        * global_semitones - int of the "capo" or semitones
          that *all* chords in the song should be played to for
          it to sound as intended
        * time_sig - tuple(int, int) of the time signature of
          the song; time_sig[0] is the numerator and time_sig[1]
          is the denominator

        :param title: name of the lyric segment
        :type title: str
        :param artist: lyrics of the segment
        :type artist: str
        :param file_path: accompanying chords of the segment
        :type file_path: str
        """
        self.title = title
        self.artist = artist
        self.file_path = file_path

        if os.path.isfile(file_path):
            list_info = []
            with open(file_path, 'r') as fh: #assumes that there is a file
                for i in range(7):
                    list_info += [fh.readline().strip()]

            self.bpm = list_info[2].split()[1]
            self.global_semitones = list_info[3].split()[1]

            list_info[4 : 7] = [' '.join(list_info[4 : 7]).split(' ', maxsplit=1)]
            list_info[4] = list_info[4][1].replace('-','').split()
            self.time_sig = (int(list_info[4][0]), int(list_info[4][1]))

    @classmethod
    def from_filename(cls, file_path):
        """Instantiate a Song object from a filename

        :classmethod:
        :param file_path: path where the ``.crd.yaml`` file resides
        :type file_path: str or Pa

        :return: information in the file stored in a ``Song`` object
        :rtype: Song
        """
        list_info = []
        if os.path.isfile(file_path):
            with open(file_path, 'r') as fh:
                for i in range(2):
                    list_info += [fh.readline().strip().split(' ', maxsplit=1)]
            
            return cls(list_info[0][1], list_info[1][1], file_path)

    # @classmethod
    # def from_yaml(cls, song_dict: dict):
    #     """Instantiate a Song object from a :py:mod:`yaml`-parsed dictionary

    #     This method is used to get a :py:class:`Song` object from a dictionary
    #     resulting from calling :py:meth:`yaml.safe_load` or any load function
    #     in the `yaml` library.
        
    #     For example, assuming that ``fh`` is a file handle to a ``.crd.yaml``
    #     file, the following code snippet shows creating a :py:class:`Song` object
    #     from it.

    #     .. code-block:: python
    #         song_dict = yaml.safe_load(fh)
    #         song_obj = Song.from_yaml(song_dict)

    #     :classmethod:
    #     :param song_dict: path where the ``.crd.yaml`` file resides
    #     :type song_dict: dict

    #     :return: information in the dictionary stored in a :py:class:`Song` object
    #     :rtype: :py:class:`Song`
    #     """
    #     title = song_dict['title']
    #     artist = song_dict['artist']
    #     file_path = './ChordFiles/'
    #     return cls(title, artist, file_path)

    def __str__(self):
        """Returns a string with basic information about the song

        This method returns the string of the format::

            "<song_title>" - by <song_artist>

        :return: string containing information about the :py:class:`Song` object
        :rtype: str
        """
        return f'"{self.title}" - by {self.artist}'

    def _load_lyrics(self, lyrics_list: list[dict]):
        """Process the lyrics tag found in a ``.crd.yaml`` file

        This method is used to process the ``lyrics`` key of a ``.crd.yaml`` file.

        :param lyrics_list: string containing information about the :py:class:`Song` object
        :type lyrics_list: list[dict]
        """
        self.lyrics = []
        for segment in lyrics_list:
            self.lyrics += [segment['text']]

        self.segments = []
        for segment in lyrics_list:
            self.segments += [segment['tag']]

        self.chords = []
        for segment in lyrics_list:
            self.chords += [segment['chords']]
    
    def num_total_lines(self, include_chords: bool=False, include_title: bool=False, include_sep: bool=False):
        """Count the number of total lines in the :py:class:`Song`

        This method is used to gauge how many lines (e.g. on a screen)
        do we need to display the whole :py:class:`Song`. The song is
        displayed as a concatenated series of stringified
        :py:class:`LyricSegment`s with optionally a space in between them.

        :param include_chords: whether to include the corresponding
            chord lines in each lyric line in the count. For each
            lyric line there is always a corresponding chord line.
        :type include_chords: bool
        :param include_title: whether to include the corresponding
            name in each lyric segment in the count. Each segment
            consumes one line.
        :type include_title: bool
        :param include_sep: whether to count the spaces between each
            lyric sergment in the count. Each space consumes one line.
        :type include_sep: bool

        :return: number of total lines consumed when the whole
            :py:class:`Song` is to be printed
        :rtype: int
        """
        total_len = len([x for x in self.lyrics[0].split('\n') if x != '']) // 2
        if include_chords == True:
            total_len += len([x for x in self.lyrics[0].split('\n') if x != '']) // 2
        elif include_title == True:
            total_len += len(self.segments)
        elif include_sep == True:
            total_len += (len([x for x in self.lyrics[0].split('\n') if x == '']) - 1)      
        
        return total_len

    def entries(self):
        """Generate a "list" of lyric segments of the :py:class:`Song`

        The method returns an ``Iterable``, which can be converted to
        a ``list`` or sequence appropriately. The resulting ``list``
        should contain a list of :py:class:`ChordedLyricSegment`s
        in the order shown in :py:attr:`~.lyrics_order`.

        This method is usually used if we want to iterate through
        each lyric segments in the order in which the song is
        supposed to be.

        :return: an ``Iterable`` object, with each element
            containing a :py:class:`ChordedLyricSegment`
        :rtype: Iterable[:py:class:`ChordedLyricSegment`]
        """
        list_chordedLS = []
        for index, segment in enumerate(self.lyrics):
            list_chordedLS += [ChordedLyricSegment(self.segments[index], segment, self.chords[index])]

        return list_chordedLS

file_path = './ChordFiles/everytime_we_touch.crd.yaml'

if os.path.isfile(file_path):
    with open(file_path, 'r') as fh:
        song_dict = yaml.safe_load(fh)

w = Song('sample0', 'sample1', file_path)
w._load_lyrics(song_dict['lyrics'])

print(w.lyrics[1])

# for x in w.entries():
#     print(str(x) + '\n' + '-----------------------------------------------------' + '\n')
