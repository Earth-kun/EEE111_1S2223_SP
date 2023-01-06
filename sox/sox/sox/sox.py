import sys
import os
from collections.abc import Sequence
from pathlib import Path

def gen_chord_sample(notes: list[str], octaves: Sequence[int]=None, out_file_path: str|Path='chord_sample'):
    A_chroma = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    A_chroma_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

    if not all([x in A_chroma or x in A_chroma_flat for x in notes]):
        raise ValueError('Invalid note(s) provided')
    
    if octaves is None:
        octaves = [4 for x in range(len(notes))]
    
    notes_and_octaves = [x + str(y) for x, y in zip(notes, octaves)]
    synth_str = ' '.join([f'pl {x}' for x in notes_and_octaves])
    
    delay_str = ' '.join([str(x * 0.05) for x in range(len(notes_and_octaves))])

    sox_exec_path = Path(__file__).resolve().parent

    if sys.platform.startswith(('win32')):
        sox_exec_path = sox_exec_path / 'bin' / 'win32' / 'sox.exe'
    elif sys.platform.startswith(('darwin')):
        sox_exec_path = sox_exec_path/ 'bin' / 'macos' / 'sox'
    elif sys.platform.startswith(('linux')):
        sox_exec_path = sox_exec_path / 'bin' / 'linux32' / 'sox.1'
    else:
        raise NotImplementedError(f'Operating system "{sys.platform}" not supported.')
    
    out_file_path = Path(out_file_path)
    e_args = ''

    if out_file_path.suffix == '':
        # Default is ogg vorbis
        out_file_path = out_file_path.with_suffix('.ogg')
    
    if out_file_path.suffix == '.wavpcm':
        # Store as 16-bit signed PCM
        e_args = '-e signed-integer -b 16'

    os_cmd = f'{sox_exec_path.absolute()} -n {e_args} {out_file_path} synth {synth_str} delay {delay_str} remix - fade 0 4 .1 reverb norm -10'
    os.system(os_cmd)

    return out_file_path

# if __name__ == '__main__':
#     gen_chord_sample(['G', 'C', 'E', 'A'])