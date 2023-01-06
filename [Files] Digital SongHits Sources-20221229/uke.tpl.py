from typing import Sequence

class ChordedInstrument:
    """Represents a chorded instrument

    This class solely consists of class methods and is meant to be
    inherited by subclasses.
    """
    # HINT: Erase these errors and populate these class properties
    #       with the appropriate data:
    #
    # A_chroma - list of strings depicting the chroma scale starting at A
    #            with notes in between written with a sharp (#)
    # A_chroma_flat - same as A_chroma except that notes in between are
    #                 flats (b)
    # chord_maps - dict with key being the chord quality (e.g. m, M, 7)
    #              and value a list of integers depicting the integer
    #              notation for that chord
    A_chroma = NotImplementedError('Stub code!')
    A_chroma_flat = NotImplementedError('Stub code!')
    chord_maps = NotImplementedError('Stub code!')

    @classmethod
    def split_chord(cls, chord: str) -> tuple[str, str, str]:
        """Split a chord into its components

        A chord consists of three parts - base/root note, accidental(s),
        and chord type. The base/root note is the base label denoting
        which note in the scale the chord most closely sounds like.
        The accidentals (sharps # and flats b) are labels on the
        base/root note. The chord type is the quality of the chord,
        and directly corresponds to which notes in the chromatic
        scale with the base/root note to play/include together.

        The method returns a tuple of the base/root note, accidental(s),
        and chord type, respectively. If the base/root note has
        no accidentals, then that element of the tuple is an empty string.
        Invalid chords entered raises a ``ValueError``.

        :param chord: the chord to split
        :type chord: `str`

        :return: the split chord in terms of its
            root note, accidental, and chord type, respectively
        :rtyp: tuple[str, str, str]

        :raise: ValueError when an empty string is provided,
            the chord is of an invalid format,
            or the chord is not supported by the program

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def supported_chords(cls) -> list[str]:
        """Get a list of supported chords

        The list of supported chords returned by this method
        is a list of chord abbreviations.

        :return: a list of supported chord type abbreviations
        :rtyp: list[str]

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def transpose_chord(cls, chord: str, semitones: int) -> str:
        """Transpose a chord to some amount of semitones

        "Transposing" a chord means finding the ``semitones``
        amount of half-steps to the left or right of the root note
        of the chord. For example, a Am7 chord transposed +2 semitones
        becomes a Bm7 chord while the same transposed -2 semitones becomes
        a Gm7 chord.

        If the root note has a flat in it, the transposed root note will
        have a flat if any. Otherwise, the transposed note will have a
        sharp instead.

        :param chord: the chord to transpose
        :type chord: `str`
        :param semitones: the number of semitones to which the cord is to be transposed
        :type semitones: int

        :return: the newly-transposed chord
        :rtyp: str

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def gen_chroma_scale(cls, base_note: str='A') -> list[str]:
        """Generate the chromatic scale from the specified ``base_note``

        The chromatic scale consists of twelve notes ordered in ascending
        pitch or frequency. In English, they are designated with the
        letters A-G with some letters in between affixed by a sharp (#)
        or a flat (b).
        
        The starting note can be changed to produce different variations
        of the scale. For example, if the base note is F, then the scale
        will be listed as such:

            F F# G G# A A# B C C# D D# E

        By default, this method will use sharps to denote the notes in the
        middle of the "normal" notes. If the base note is written with a
        flat, like ``Ab``, then the chromatic scale will be generated using
        flats instead. For example, if the base note is F, then the scale
        using flats will be listed as such:

            F Gb G Ab A Bb B C Db D Eb E

        If the base note is of the invalid format, this method returns an
        empty list.

        :param base_note: the first note in the scale
        :type base_note: str

        :return: the chromatic scale starting from ``base_note``. The length
            of the list should be twelve
        :rtyp: list[str]

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def get_notes_from_intervals(cls, base_note: str, intervals: Sequence[int]) -> tuple[str]:
        """Get the corresponding notes given an integer notation and the base note

        This method is used to retrieve the notes that make up a chord. Chords
        can be represented in `integer notation <https://integermusic.blogspot.com/2014/11/chords.html>`_, which
        denotes which notes in the chromatic scale in relation to a base/root note
        is part of the chord. For example, with a base note B:

        * {0} represents the note set {B}
        * {0, 4, 7} represents the note set {B, D#, F#} - a B major chord

        :param base_note: the first note in the chromatic scale
        :type base_note: str
        :param intervals: the notes to retrieve in integer notation
        :type intervals: Sequence[int]

        :return: a tuple of notes corresponding to the integer notation ``intervals``.
            The length of the tuple should be equal to the length of ``intervals``.
        :rtyp: tuple[str]

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def get_chord_notes(cls, chord: str) -> tuple[str]:
        """Get the notes corresponding to a chord

        The method accepts ``chord``s in abbreviation notation only
        Valid chords include (but not limited to): ``A``, ``Amaj7``,
        ``Cdim``.

        :param chord: the chord whose component notes we want to retrieve
        :type chord: str

        :return: the notes of the chord in ascending order in relation
            to the chromatic scale. The first element should be the
            base/root note of the chord.
        :rtyp: tuple[str]

        :classmethod:
        """
        raise NotImplementedError('Stub code!')


class Ukulele(ChordedInstrument):
    """Represents a ukulele

    An ukulele is a :py:class:`ChordedInstrument` where we can extract
    the fingerings of a specific chord. We are also able to play a sound
    using this class.
    """
    def __init__(self, tuning: Sequence[str]=['G', 'C', 'E', 'A'], octaves: Sequence[int]=[4, 4, 4, 4], num_frets: int=20):
        """Instantiate an object of this class

        This method will instantiate a new :py:class:`Ukulele`
        object with the given ``tuning``, corresponding ``octaves``,
        and ``num_frets``. The number of elements in ``tuning`` and
        ``octaves`` should be the same.

        Objects of this class have only the following properties:
        * tuning
        * octaves
        * num_frets

        :param tuning: tuning of strings the ukulele. The standard tuning
            of an ukulele from left to right is [G4, C4, E4, A4]
        :type tuning: list[str] or tuple[str]
        :param octaves: corresponding octaves of the tuning
        :type octaves: list[int] or tuple[int]
        :param num_frets: number of frets in the ukulele
        :type num_frets: int
        """
        raise NotImplementedError('Stub code!')

    def gen_fret_notes(self) -> dict[str, list[str]]:
        """Generate a chromatic scale for each string in the :py:class:`Ukulele`

        This method generates the chromatic scale using :py:attr:num_frets notes
        for each base/root note in :py:attr:tuning of the ukulele.

        :return: a dictionary containing the chromatic scale for each note
            in each string of the ukulele. The number of elements in each
            value of the dictionary should be equal to the number of frets
        :rtyp: dict[str, list[str]]
        """
        raise NotImplementedError('Stub code!')

    def get_note_idxs_on_fret(self, notes: list[str]) -> dict[str, list[int]]:
        """Get the strings and frets where certain notes are located

        This method determines, for each string in the ukulele, the location
        of each fret in each string. When pressed and strummed individually, it
        will produce a sound from one of the notes in the ``notes`` parameter.

        For example::

            fret_map = uke.get_note_idxs_on_fret(['C', 'E', 'G'])
            fret_map['C'] # Contains [0, 4, 7, 12, ...]
            fret_map['G'] # Contains [0, 5, 9, 12, ...]

        Note that the size of the list corresponding to each string will be different,
        but the numbers are always less than :py:attr:num_frets.

        :param notes: the notes we want to find on the fretboard
        :type notes: list[str]

        :return: a dictionary with its keys being the elements of :py:attr:tuning
            corresponding to the "default"/"open" tone of the string.
            Its values correspond to which frets a note in ``notes`` are located.
        :rtyp: dict[str, list[int]]
        """
        raise NotImplementedError('Stub code!')

    def get_chord_fingerings(self, chord_name: str) -> list[list[int]]:
        """Get the possible chord fingerings for a chord

        This method will find all possible chord fingerings for a chord.
        It is a list where each element is a list of the same length as
        :py:attr:`~.tuning` with each nth element in the list corresponding
        to the fret to press in the nth string in :py:attr:`~.tuning`. If
        an element is zero, it means that the string is open (i.e. not
        pressed).

        The fingerings have the following properties:

        * All strings are strummed, i.e. each string has a finger
        * Each finger in a chord should be +- 3 of the average fret
          position of all of the fingers in it.
        * The largest spacing between any two fingers is at most four
          frets.
        * Open strings are not counted when computing for the average
          fret position or spacing between any two fingers.
        * The maximum position of the closest finger from the fret nut
          is the seventh fret.

        The ``chord_name`` supplied should be a valid one according to
        :py:meth:`split_chord`.

        :param chord_name: the name of the chord to process
        :type chord_name: str

        :return: a list of the possible fingerings for the chord
        :rtyp: list[list[int]]
        """
        raise NotImplementedError('Stub code!')

    def play_fingering(self, fingering: list[int], chord_name: str=None):
        """Play a strumming sound corresponding to a chord fingering

        :param fingering: the fingering of the chord on a :py:class:`Ukulele`
        :type fingering: list[int]
        :param chord_name: the name of the chord to play
        :type chord_name: str

        :return: the notes of the chord in ascending order in relation
            to the chromatic scale. The first element should be the
            base/root note of the chord.
        :rtyp: list[str]
        """
        # HINT: Use the provided Simple SoX Wrapper library and
        #       simpleaudio (from pip) to implement this function
        # HINT: You can import modules inside this function itself, but
        #       do not forget to catch ``ImportError``s in case you
        #       did not install the wrapper
        raise NotImplementedError('Stub code!')


class UkulelePrinter:
    """Represents a ukulele printer

    This class contains convenience methods to print different
    ukulele graphics in the terminal. It can print two
    representations of a ukulele - full and compact. The full
    graphic is used in the chord browser where the fretboard
    is oriented horizontally and spans the whole width of the
    terminal, and the compact graphic is used in the song
    browser where the fretboard is oriented vertically and
    only has a provision for at most four frets and the fret
    nut.
    """
    FRET_HEAD_FULL = """\
  OOO
___|____
        `;...
           ||
           ||
           ||
           ||
           ||
           ||
___.____,;'''
   |
  OOO
    """

    FRET_HEAD_COMPACT = """\
_______
| | | |
| | | |
| | | |
| | | |
'''''''
    """

    @classmethod
    def full_head_rows(cls) -> int:
        """Return the number of lines/rows of the full ukulele head

        :return: number of lines/rows of the full ukulele head
        :rtyp: int

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def full_head_max_cols(cls) -> int:
        """Return the number of maximum columns of the full ukulele head

        The graphic for the ukulele head has different number of columns
        per line. This method returns the maximum number of columns in
        each line.

        :return: number of maximum columns of the full ukulele head
        :rtyp: int

        :classmethod:
        """
        raise NotImplementedError('Stub code!')
    
    @classmethod
    def compact_head_rows(cls) -> int:
        """Return the number of lines/rows of the compact ukulele head

        :return: number of lines/rows of the compact ukulele head
        :rtyp: int

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def compact_head_max_cols(cls) -> int:
        """Return the number of maximum columns of the compact ukulele head

        The graphic for the ukulele head has different number of columns
        per line. This method returns the maximum number of columns in
        each line.

        :return: number of maximum columns of the compact ukulele head
        :rtyp: int

        :classmethod:
        """
        raise NotImplementedError('Stub code!')

    @classmethod
    def str_uke_full(cls, fret_width: int=9, num_frets: int=12) -> list[str]:
        """Return the lines that represent the graphic for a full ukulele

        The full ukulele graphic is used in the chord browser where the fretboard
        spans the whole column. It consists of the head of the ukulele
        and the frets. Each fret has a width ``fret_width`` and each string is
        drawn using the ``-`` character, with each fret demarcated by a
        ``|`` character. The last fret ends with a ``|``.

        :param fret_width: the number of characters consisting each fret
        :type fret_width: int
        :param num_frets: the number of frets in the ukulele
        :type num_frets: int

        :return: a list of strings representing each line of the graphic
            of a whole ukulele. 
        :rtyp: list[str]

        :classmethod:
        """
        # HINT: Looking at ``FRET_HEAD_FULL~``, you may notice that
        #       the "strings" occur at lines 4 to 7 inclusive, while
        #       line 3 has no "string".
        raise NotImplementedError('Stub code!')
