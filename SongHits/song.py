# Import for type hints
from collections.abc import Iterable

# Built-in modules
import re # HINT: People who know regex may use this module
from pathlib import Path

# pip downlodeable modules
import yaml

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
        self.full_lyrics = text
        self.chords = chords.strip().split()

        temp_list = []
        for idx, line in enumerate(self.text):
            if idx % 2 != 0:
                temp_list += [line]
        self.text = temp_list
        

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

        for idx, line in enumerate(self.annotated_lyrics):          
            if idx == (len(self.full) - 2):
                str_ChordedLyrics += line.strip()
            elif idx % 2 == 0:
                modified_line = line
                for i in range(len(re.findall(r'[1-9]', modified_line))):
                    # print('offset = ' + str(offset) + '; i = ' + str(i) + '; line no. = ' + str(idx))
                    if len(self.chords[i + offset - 1]) == 2 and i != 0:
                        index = modified_line.find(r'\d')
                        modified_line = modified_line[:index-1] + modified_line[index]
                        modified_line = re.sub(r'[1-9]', self.chords[i + offset], modified_line, 1)
                    elif len(self.chords[i + offset - 1]) == 3 and i != 0:
                        index = modified_line.find(r'\d')
                        modified_line = modified_line[:index-2] + modified_line[index]
                        modified_line = re.sub(r'[1-9]', self.chords[i + offset], modified_line, 1)
                    else:
                        modified_line = re.sub(r'[1-9]', self.chords[i + offset], modified_line, 1)
                offset += len(re.findall(r'[1-9]', line))
                str_ChordedLyrics += modified_line + '\n'
            else:
                str_ChordedLyrics += line.strip() + '\n'
        
        return str_ChordedLyrics.strip()
    
    def entries(self) -> Iterable[tuple[str, list[tuple[str, int, int]]]]:
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
        # list_EachLine_Lyric = str(self).split('\n')
        line_chord_dur = [x for idx, x in enumerate(self.full) if idx % 2 == 0 and x != '']
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

                    chord_elements += [(self.chords[counter], chord_col, int(x))]
                    counter += 1

            list_entries += [(self.full[(idx * 2) + 1], chord_elements)]

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

        with open(file_path, 'r+') as fh: #assumes that there is a file
            fh.read(16)

    @classmethod
    def from_filename(cls, file_path: str|Path):
        """Instantiate a Song object from a filename

        :classmethod:
        :param file_path: path where the ``.crd.yaml`` file resides
        :type file_path: str or Path

        :return: information in the file stored in a ``Song`` object
        :rtype: Song
        """
        return cls(file_path)

    @classmethod
    def from_yaml(cls, song_dict: dict):
        """Instantiate a Song object from a :py:mod:`yaml`-parsed dictionary

        This method is used to get a :py:class:`Song` object from a dictionary
        resulting from calling :py:meth:`yaml.safe_load` or any load function
        in the `yaml` library.
        
        For example, assuming that ``fh`` is a file handle to a ``.crd.yaml``
        file, the following code snippet shows creating a :py:class:`Song` object
        from it.

        .. code-block:: python
            song_dict = yaml.safe_load(fh)
            song_obj = Song.from_yaml(song_dict)

        :classmethod:
        :param song_dict: path where the ``.crd.yaml`` file resides
        :type song_dict: dict

        :return: information in the dictionary stored in a :py:class:`Song` object
        :rtype: :py:class:`Song`
        """
        raise NotImplementedError('Stub code!')

    def __str__(self):
        """Returns a string with basic information about the song

        This method returns the string of the format::

            "<song_title>" - by <song_artist>

        :return: string containing information about the :py:class:`Song` object
        :rtype: str
        """
        raise NotImplementedError('Stub code!')

    def _load_lyrics(self, lyrics_list: list[dict]):
        """Process the lyrics tag found in a ``.crd.yaml`` file

        This method is used to process the ``lyrics`` key of a ``.crd.yaml`` file.

        :param lyrics_list: string containing information about the :py:class:`Song` object
        :type lyrics_list: list[dict]
        """
        raise NotImplementedError('Stub code!')
    
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
        raise NotImplementedError('Stub code!')

    def entries(self) -> Iterable[ChordedLyricSegment]:
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
        raise NotImplementedError('Stub code!')

class SongCursor:
    """Represents a song cursor

    The song cursor is a wrapper around the :py:class:`Song` class.
    It is used by the main UI to navigate and scroll across
    the song using the chord annotations on top of each lyric
    line.
    """
    def __init__(self, song: Song):
        """Instantiate an object of this class

        This method will instantiate a new :py:class:`SongCursor`
        object with the given ``song``.

        :param song: :py:class:`Song` object that this cursor will track
        :type song: :py:class:`Song`
        """
        raise NotImplementedError('Stub code!')
    
    def _chord_idx_to_rc(self, song: Song) -> list[dict]:
        """Generate a chord index mapping to (line, col) coordinates

        Inside a :py:class:`Song`, a chord can be fetched using its 0-index within the
        song.

        :param song: :py:class:`Song` object to preprocess the mapping from index to
            coordinates
        :type song: :py:class:`Song`

        :return: a list of dictionaries, with each dictionary containing three
            keys ``line``, ``col``, and ``chord_name``. This is read as: from coordinates
            ``(line, col)``, ``chord_name`` appears.
        :rtype: list[dict]
        """
        raise NotImplementedError('Stub code!')
    
    def next_line_pos(self, idx: int) -> tuple[int, int]:
        """Find the chord one line downward in the song

        This method finds the chord one line downward in the song. It does this
        by looking for the ``line`` of the chord at ``idx`` in the song and then
        checking whether a line exists below it. If so, then the leftmost chord
        at that line is fetched with its index ``next_idx`` and difference
        between its line and the line corresponding to ``idx`` ``diff_lines``. The tuple
        (``next_idx``, ``diff_lines``) is then returned.

        If ``idx`` is less than zero, it returns (0, 0).

        If a next line cannot be found, it returns (``idx``, 0).

        :param idx: current index of the chord to check for its corresponding
            chord in the next line
        :type idx: int

        :return: a 2-ary ``tuple``, with the first element being the index
            of the chord at the next line ``next_idx``, and the second element
            being the difference between the ``line``s of the chord at ``idx``
            and of the chord at ``next_idx``
        :rtype: tuple[int, int]
        """
        raise NotImplementedError('Stub code!')
    
    def prev_line_pos(self, idx: int) -> tuple[int, int]:
        """Find the chord one line upward in the song

        This method finds the chord one line upward in the song. It does this
        by looking for the ``line`` of the chord at ``idx`` in the song and then
        checking whether a line exists above it. If so, then the leftmost chord
        at that line is fetched with its index ``prev_idx`` and difference
        between its line and the line corresponding to ``idx`` ``diff_lines``. The tuple
        (``prev_idx``, ``diff_lines``) is then returned.

        If ``idx`` is greater than the number of chords in the song, it returns
        (``num_chords`` - 1, 0).

        If a previous line cannot be found, it returns (``idx``, 0).

        :param idx: current index of the chord to check for its corresponding
            chord in the previous line
        :type idx: int

        :return: a 2-ary ``tuple``, with the first element being the index
            of the chord at the previous line ``prev_idx``, and the second element
            being the difference between the ``line``s of the chord at ``idx``
            and of the chord at ``prev_idx``
        :rtype: tuple[int, int]
        """
        raise NotImplementedError('Stub code!')
    
    def next_chord_pos(self, idx: int) -> tuple[int, int]:
        """Find the chord next to a chord in the song

        This method finds the chord next to it in the song. If this is used
        in a UI setting, this is similar to pressing the NEXT key. So, if
        there are chords like so:

            C G Em F

        ... then, the next chord of Em is F. The index of F ``next_idx`` and
        the difference between the lines where Em and F `diff_lines` are fetched.
        The tuple (``next_idx``, ``diff_lines``) is then returned. Note that in
        this example, ``diff_lines`` is 0.

        If ``idx`` is greater than the number of chords in the song, it returns
        (``num_chords`` - 1, 0).

        :param idx: current index of the chord to check for its corresponding
            chord next to it
        :type idx: int

        :return: a 2-ary ``tuple``, with the first element being the index
            of the chord next to it ``next_idx``, and the second element
            being the difference between the ``line``s of the chord at ``idx``
            and of the chord at ``next_idx``
        :rtype: tuple[int, int]
        """
        raise NotImplementedError('Stub code!')
    
    def prev_chord_pos(self, idx: int) -> tuple[int, int]:
        """Find the chord before a chord in the song

        This method finds the chord immediately before it in the song. If
        this is used in a UI setting, this is similar to pressing the PREV key.
        So, if there are chords like so:

            C G Em F

        ... then, the previous chord of Em is G. The index of G ``prev_idx`` and
        the difference between the lines where Em and G ``diff_lines`` are fetched.
        The tuple (``prev_idx``, ``diff_lines``) is then returned. Note that in
        this example, ``diff_lines`` is 0.

        If ``idx`` is zero or less, it returns (0, 0).

        :param idx: current index of the chord to check for its corresponding
            chord before it
        :type idx: int

        :return: a 2-ary ``tuple``, with the first element being the index
            of the chord before it ``prev_idx``, and the second element
            being the difference between the ``line``s of the chord at ``idx``
            and of the chord at ``prev_idx``
        :rtype: tuple[int, int]
        """
        raise NotImplementedError('Stub code!')

    def __getitem__(self, key):
        """Get the (line, col) coordinates of a chord

        This function also supports ``slice``s to get a list of coordinates of
        the chords in that ``slice``.

        :param key: index of the chord(s) to get
        :type key: int or slice

        :return: a ``dict`` with the keys ``line``, ``col``, and ``chord_name``,
            corresponding to the coordinates. See :py:meth:`~._chord_idx_to_rc` for
            details.
        :rtype: dict

        .. seealso:: :py:meth:`~._chord_idx_to_rc`
        """
        raise NotImplementedError('Stub code!')
    
    def __len__(self):
        """Return the total number of chords in the song

        :return: an ``int`` of the total number of chords in the song
        :rtype: int
        """
        raise NotImplementedError('Stub code!')

class SongCollection:
    """Represents a collection of songs
    """
    def __init__(self, song_path: str|Path='./songs'):
        raise NotImplementedError('Stub code!')
    
    def song_list(self) -> list[Song]:
        """Get the internal songlist in this collection

        This object internally saves the song list retrieved from the
        provided directory during initialization. This method retrieves
        that list.

        :return: a list of :py:class:`Song`s found inside the folder
        :rtype: list[Song]
        """
        raise NotImplementedError('Stub code!')

    def get_songs_from_folder(self, refresh: bool=False) -> list[Song]:
        """Get songs from a specified folder

        This method looks non-recursively for ``.crd.yaml`` files inside
        the folder where this collection is currently set and returns it.
        Optionally, the ``refresh`` flag can be set to force the collection
        to replace its current contents with the one read by this method.

        The method returns the list of :py:class:`Song`s sorted by ascending
        title alphabetically.

        :param refresh: flag whether to replace the current collection contents
        :type refresh: bool

        :return: a list of :py:class:`Song`s found inside the folder
        :rtype: list[Song]
        """
        raise NotImplementedError('Stub code!')
    
    def find_songs(self, kwords: str) -> list[Song]:
        """Find songs in this collection that match certain keywords

        This method looks for songs that match the keywords ``kwords``.
        It then returns the list of :py:class:`Song`s sorted by ascending
        title alphabetically. It *does not* change the internal songlist
        in the collection.

        :param kwords: keywords to use to search for song names in this collection
        :type kwords: str

        :return: a sorted list of :py:class:`Song`s matching the ``kwords``
        :rtype: list[Song]
        """
        raise NotImplementedError('Stub code!')
    
    def __getitem__(self, key):
        """Get the ``key``th song in this collection

        This object internally saves the song list retrieved from the
        provided directory during initialization. This list is also
        sorted in ascending order alphabetically. This method retrieves
        the ``key``th element or sublist in the collection.

        :param key: index/indices of the :py:class:`Song`s to retrieve
        :type key: int or slice

        :return: a single instance (if key is int) or a list of :py:class:`Song`s
            (if key is slice) matching the indices
        :rtype: Song or list[Song]
        """
        raise NotImplementedError('Stub code!')

    def __len__(self) -> int:
        """Get the number of :py:class:`Song`s in this collection

        :return: number of :py:class:`Song`s in this collection
        :rtype: int
        """
        raise NotImplementedError('Stub code!')