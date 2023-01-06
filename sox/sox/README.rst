=======================================
Chord-Generating SoX Wrapper for Python
=======================================

This library is a simple Python wrapper for the `SoX library <https://sox.sourceforge.net/>`_. It contains only one function - ``gen_chord_sample()`` - which generates an audio file from a set of chords supplied.

------------------
Quick Installation
------------------
1. Setup a ``virtualenv`` in your current working directory. The Python in this virtual environment should be at least v3.10.
2. ``activate`` the virtual environment. Assuming that ``venv`` is the name/directory of the created virtual environment.
    * *Windows* - Activate through Windows PowerShell using ``venv/Scripts/activate``
    * *Unix(ish)* - Activate through the terminal using ``source venv/bin/activate``.
3. Move to the directory of this README file.
4. Type ``pip install sox``.
5. You should be able to ``import`` the library using ``from sox import sox`` and call functions using, for example, ``sox.gen_chord_sample(...)``.

------------------
Function List
------------------

``gen_chord_sample(notes: list[str], octaves: Sequence[int]=None, out_file_path: str|Path='chord_sample') -> Path``

*Generate an audio file of a chord being strummed.*

The chords are provided separately as a ``list`` of notes and their corresponding octaves.

The audio file will be saved in ``out_file_path``. If the extension is not supplied, then the audio file will be saved as an Ogg Vorbis (``.ogg``) file. Supported extensions can be found in the `soxformat <https://linux.die.net/man/7/soxformat>`_ documentation. To play the sound through Python, use the ``.wavpcm`` extension since Python natively will play only signed 16-bit PCM Wave files.

""""""""""
Parameters
""""""""""

**notes** *list[str]*
a list of the string representation of the notes. Valid notes include (but not limited to): ``A``, ``A#``, ``Ab``

**octaves** *list[int]*
a list of the corresponding octaves of the supplied notes. Each element should be an integer from 0.

**out_file_path** *str|Path*
string or ``pathlib.Path`` to the output file where the generated audio file will be saved. The default is "chord_sample.ogg".

""""""
Raises
""""""
*ValueError*

* Notes provided are of the invalid format
* The notes provided does not exist in musical notation

*IndexError*

* No ``notes`` or ``octaves`` supplied
* Length of ``notes`` and ``octaves`` are not the same

*NotImplementedError*

* OS or platform is not supported
* Note that only Linux, MacOS, and Windows are supported

"""""""""""
Sample code
"""""""""""

::

   from sox import sox

   # Generate a ukulele Am7 chord
   notes = ['G', 'C', 'E', 'A']
   octaves = [4, 4, 4, 4]

   # Will create "chord_sample.ogg" in the current directory
   # where this script was run
   out_file_path = sox.gen_chord_sample(notes, octaves)
