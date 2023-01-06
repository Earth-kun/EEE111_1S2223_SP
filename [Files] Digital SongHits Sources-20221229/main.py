import curses
import curses.ascii
import curses.textpad

import ui_lib
import song
from uke import Ukulele, UkulelePrinter

SCREEN_MAIN = 0
SCREEN_SONGLIST = 1
SCREEN_SONGTEXT = 2
SCREEN_CHORDS = 3
SCREEN_QUIT = -1

def print_uke_full(w, start_line: int=0, finger_placement: tuple|list=None, chord_name: str=None, chord_inv_serial: tuple|list=(0, 0)):
    # Print ukulele template
    for i, s in enumerate(UkulelePrinter.str_uke_full(), start=start_line):
        w.write_str((i, 0), s)

    if type(finger_placement) is list and len(finger_placement) == 4:
        # Print chord name
        if chord_name is not None and len(chord_name) > 0:
            w.write_str((5 + start_line, 3), chord_name)
        
        # Print chord page
        if (type(chord_inv_serial) is list or type(chord_inv_serial) is tuple) \
            and len(chord_inv_serial) == 2:
            has_l = 1 <= chord_inv_serial[0] - 1 <= chord_inv_serial[1]
            has_r = 1 <= chord_inv_serial[0] + 1 <= chord_inv_serial[1]

            w.write_str((6 + start_line, 1), f'{"<" if has_l else " "} {chord_inv_serial[0]} / {chord_inv_serial[1]} {">" if has_r else " "}')

        # Place fingers as 'X's on fret
        for finger_idx, str_idx in zip(finger_placement[::-1], range(4, 8)):
            if finger_idx == 0:
                w.write_str((str_idx + start_line, UkulelePrinter.full_head_max_cols() - 2), 'X', attrs=w.color_pair_to_attr(1))
            else:
                w.write_str((str_idx + start_line, UkulelePrinter.full_head_max_cols() - 1 + (10 * finger_idx) - 5), 'X', attrs=w.color_pair_to_attr(1))

def print_uke_compact(w, start_line: int=0, finger_placement: tuple|list=None, chord_name: str=None, chord_inv_serial: tuple|list=(0, 0)):
    uke_str = """\
_______
| | | |
| | | |
| | | |
| | | |
'''''''
    """

    if type(finger_placement) is list and len(finger_placement) == 4:
        # Clear writings
        w.write_str((1, w.CENTER), '     ')
        w.write_str((2, w.CENTER), '       ')

        w.write_str((1, w.CENTER), chord_name)
        w.write_str((2, w.CENTER), f'{chord_inv_serial[0]} / {chord_inv_serial[1]}')

    for i, each_line in enumerate(uke_str.split('\n')):
        w.write_str((i + start_line, 3), each_line)
    
    # Skip if no finger placement is provided
    if type(finger_placement) is not list or len(finger_placement) != 4:
        return

    for i, each_line in enumerate(uke_str.split('\n')):
        min_finger, max_finger = min(finger_placement), max(finger_placement)

        # Write fret indicator
        if min_finger >= 2 and max_finger > 4:
            w.write_str((1 + start_line, 1), str(min_finger), attrs=w.color_pair_to_attr(3))
        else:
            w.write_str((1 + start_line, 1), '  ')

        # Write finger placements
        if 0 <= i <= 4:
            col_idxs = [x for x, z in enumerate(finger_placement) if z - min_finger == i]

            if min_finger > 0:
                i += 1
            
            for each_col_idx in col_idxs:
                w.write_str((i + start_line, 3 + (2 * each_col_idx)), 'X', attrs=w.color_pair_to_attr(1))

def print_status_bar(w: ui_lib.CursesMainWindow, msg, lines_from_end=0):
    cur_coord = w.cursor_pos()

    # Clear and rewrite new message
    w.write_str((w.rows - lines_from_end - 1, 0), ' ' * (w.cols - 1))
    w.write_str((w.rows - lines_from_end - 1, 0), msg[:w.cols - 1])

    w.move_cursor((cur_coord[0], cur_coord[1]))
    w.refresh()

def display_song_lyric(w: ui_lib.CursesWindow, song_lyrics: song.Song, highlighted_chord_idx: int=0):
    cur_chord_idx = 0
    w_song_text_idx = 0

    for each_lyric_block in song_lyrics:
        w.write_str((w_song_text_idx, 1), f'[{each_lyric_block.name}]', attrs=w.color_pair_to_attr(3))
        w_song_text_idx += 1
        
        for each_lyric_text, each_chords_pos in each_lyric_block.entries():
            # Print chords
            for ct, cp, cdur in each_chords_pos:
                chord_attr = w.color_pair_to_attr(2)

                if cur_chord_idx == highlighted_chord_idx:
                    chord_attr = w.color_pair_to_attr(1)

                w.write_str((w_song_text_idx, 1 + cp), ct, attrs=chord_attr)
                cur_chord_idx += 1

            w_song_text_idx += 1

            # Print lyrics
            w.write_str((w_song_text_idx, 1), each_lyric_text)
            w_song_text_idx += 1
        
        # Extra line
        w_song_text_idx += 1

def display_songs(w: ui_lib.CursesMainWindow, w_song: ui_lib.CursesWindow, songs: list[song.Song]):
    w_song.clear()

    for i, each_song in enumerate(songs):
        w_song.write_str((i, 1), f'> {each_song}')
    
    # Song total
    w.write_str((7, w.CENTER), f'{len(songs)} total song(s)')

@ui_lib.screen_arg_unpacker
def screen_songlist(w: ui_lib.CursesMainWindow):
    songlist_banner = """\
   _____                   ____                                   
  / ___/____  ____  ____ _/ __ )_________ _      __________  _____
  \__ \/ __ \/ __ \/ __ `/ __  / ___/ __ \ | /| / / ___/ _ \/ ___/
 ___/ / /_/ / / / / /_/ / /_/ / /  / /_/ / |/ |/ (__  )  __/ /    
/____/\____/_/ /_/\__, /_____/_/   \____/|__/|__/____/\___/_/     
                 /____/                                           
    """

    w.clear()
    w.print_banner(songlist_banner, ul=(0, w.CENTER))

    # Songlist
    song_coll_obj = song.SongCollection()
    disp_song_list = song_coll_obj.song_list()

    # songlist = range(20)
    w_songs = ui_lib.CursesScrollableWindow(
        (w.rows - 3 - 9, w.cols - 10 - 10),
        ul=(9, 10),
        pad_dim=(len(disp_song_list), w.cols - 10 - 10 - 1),
    )

    display_songs(w, w_songs, disp_song_list)

    print_status_bar(w, '> (UP/Down) Select; (F5) Refresh; (ENTER) View; (^S) Search; (^X) Main Menu')
    w.move_cursor((9 + 1, 10 + 2))

    song_select_idx = 0

    while True:
        if len(disp_song_list) > 0:
            w_songs.write_str((song_select_idx, 1), f'> {disp_song_list[song_select_idx]}', attrs=w.color_pair_to_attr(1))

        w_songs.refresh()
        
        c = w.getch()

        if curses.ascii.unctrl(c) == '^S':
            song_name = w.show_text_prompt(msg='Enter song name:', size=(3, 40))

            disp_song_list = song_coll_obj.find_songs(song_name)
            display_songs(w, w_songs, disp_song_list)
            song_select_idx = 0
        elif w.which_fn_key(c) == 5:
            # Refresh
            disp_song_list = song_coll_obj.get_songs_from_folder(refresh=True)
            display_songs(w, w_songs, disp_song_list)
            song_select_idx = 0
        elif curses.ascii.unctrl(c) == '^Q':
            is_quitting = w.show_yn_prompt(msg='Quit Songhits?')

            if is_quitting:
                return SCREEN_QUIT
        elif curses.ascii.unctrl(c) == '^X':
            return SCREEN_MAIN
        else:
            # Arrow keys
            if len(disp_song_list) <= 0:
                continue

            w_songs.write_str((song_select_idx, 1), f'> {disp_song_list[song_select_idx]}', attrs=w.color_pair_to_attr(2))

            if w.which_arrow_key(c) == w.K_DOWN_ARROW and song_select_idx < len(disp_song_list) - 1:
                song_select_idx += 1
                w_songs.scroll(w.K_DOWN_ARROW)
            elif w.which_arrow_key(c) == w.K_UP_ARROW and song_select_idx > 0:
                song_select_idx -= 1
                w_songs.scroll(w.K_UP_ARROW)
            elif w.is_enter_key(c):
                return SCREEN_SONGTEXT, disp_song_list[song_select_idx]

@ui_lib.screen_arg_unpacker
def screen_song_text(w: ui_lib.CursesMainWindow, song_obj: song.Song):
    w.clear()

    # Song details
    w.write_str((1, 2), song_obj.title)
    w.write_str((2, 2), f'by {song_obj.artist}')
    w.write_str((3, 2), f'Capo: {song_obj.global_semitones}, BPM: {song_obj.bpm}; TS: {song_obj.time_sig[0]} / {song_obj.time_sig[1]}')

    # Song lyrics/chords
    selected_chord_idx = 0
    song_cursor = song.SongCursor(song_obj)
    song_lyrics = list(song_obj.entries())

    w_song_text = ui_lib.CursesScrollableWindow(
        (w.rows - 5 - 2, 3 * w.cols // 5),
        ul=(5, 2),
        pad_dim=(song_obj.num_total_lines(include_chords=True, include_title=True, include_sep=True), w.cols - 2),
    )

    display_song_lyric(w_song_text, song_lyrics, highlighted_chord_idx=selected_chord_idx)

    # Guitar chords
    uke_obj = Ukulele()

    w_song_text_right_edge = (w_song_text.left + w_song_text.border_cols)
    uke_ul = (5, w_song_text_right_edge + 2)

    w_uke = ui_lib.CursesWindow.new_window((UkulelePrinter.compact_head_rows() + 5, UkulelePrinter.compact_head_max_cols() + 6), ul=uke_ul)
    w_uke.color_and_box(w_uke.color_pair_to_attr(2))

    # Print chord fingerings
    current_chord_finger_idx = 0
    chord_fingerings = uke_obj.get_chord_fingerings(song_cursor[selected_chord_idx]['chord_name'])
    chord_finger = chord_fingerings[current_chord_finger_idx]
    print_uke_compact(
        w_uke,
        start_line=4,
        finger_placement=chord_finger,
        chord_name=song_cursor[selected_chord_idx]['chord_name'],
        chord_inv_serial=(1, len(chord_fingerings))
    )

    print_status_bar(w, '> (Up/Down/Left/Right) Scroll Chords in Song; (ENTER) Play Chord; (^X) Songlist')

    w.move_cursor((6, 4))
    w_song_text.scroll(w.K_DOWN_ARROW)
    w_song_text.scroll(w.K_DOWN_ARROW)

    while True:
        w_song_text.refresh()
        w_uke.refresh()

        c = w.getch()

        if curses.ascii.unctrl(c) == '^Q':
            is_quitting = w.show_yn_prompt(msg='Quit Songhits?')

            if is_quitting:
                return SCREEN_QUIT
        elif curses.ascii.unctrl(c) == '^X':
            return SCREEN_SONGLIST
        elif w.is_enter_key(c):
            # Try to play the chord
            chord_name = song_cursor[selected_chord_idx]['chord_name']
            chord_fingerings = uke_obj.get_chord_fingerings(chord_name)
            chord_finger = chord_fingerings[current_chord_finger_idx]

            uke_obj.play_fingering(chord_finger, chord_name=chord_name)
        else:
            # Arrow keys
            if w.which_arrow_key(c) == w.K_DOWN_ARROW and selected_chord_idx < len(song_cursor) - 1:
                next_idx, line_diff = song_cursor.next_line_pos(selected_chord_idx)
                selected_chord_idx = next_idx

                for _ in range(line_diff):
                    w_song_text.scroll(w.K_DOWN_ARROW)

                # now_line = song_cursor[selected_chord_idx]['line']
                # r_list = [x for x in song_cursor[selected_chord_idx + 1:] if x['line'] != now_line]

                # if len(r_list) > 0:
                #     # Find next line
                #     next_line_obj = min(r_list, key=lambda x: x['line'])
                #     selected_chord_idx = song_rc.index(next_line_obj)

                #     for _ in range(next_line_obj['line'] - now_line):
                #         w_song_text.scroll(w.K_DOWN_ARROW)
            elif w.which_arrow_key(c) == w.K_UP_ARROW and selected_chord_idx > 0:
                prev_idx, line_diff = song_cursor.prev_line_pos(selected_chord_idx)
                selected_chord_idx = prev_idx

                for _ in range(line_diff):
                    w_song_text.scroll(w.K_UP_ARROW)

                # now_line = song_cursor[selected_chord_idx]['line']
                # l_list = [x for x in song_cursor[:selected_chord_idx] if x['line'] != now_line]

                # if len(l_list) > 0:
                #     # Find previous line
                #     prev_line_obj = max(l_list, key=lambda x: x['line'])
                #     selected_chord_idx = song_rc.index(prev_line_obj)

                #     for _ in range(now_line - prev_line_obj['line']):
                #         w_song_text.scroll(w.K_UP_ARROW)
            elif w.which_arrow_key(c) == w.K_LEFT_ARROW:
                prev_idx, line_diff = song_cursor.prev_chord_pos(selected_chord_idx)
                selected_chord_idx = prev_idx

                for _ in range(line_diff):
                    w_song_text.scroll(w.K_UP_ARROW)

                # if selected_chord_idx > 0 and song_rc[selected_chord_idx]['line'] == song_rc[selected_chord_idx - 1]['line']:
                #     selected_chord_idx -= 1
            elif w.which_arrow_key(c) == w.K_RIGHT_ARROW:
                next_idx, line_diff = song_cursor.next_chord_pos(selected_chord_idx)
                selected_chord_idx = next_idx

                for _ in range(line_diff):
                    w_song_text.scroll(w.K_DOWN_ARROW)

                # if selected_chord_idx < len(song_rc) - 1 and song_rc[selected_chord_idx]['line'] == song_rc[selected_chord_idx + 1]['line']:
                #     selected_chord_idx += 1
            
            if w.which_arrow_key(c) is not None:
                # Reset chord index if arrow keys were pressed
                current_chord_finger_idx = 0

            display_song_lyric(w_song_text, song_lyrics, selected_chord_idx)
            
            # Reprint ukulele
            chord_fingerings = uke_obj.get_chord_fingerings(song_cursor[selected_chord_idx]['chord_name'])
            chord_finger = chord_fingerings[current_chord_finger_idx]

            print_uke_compact(
                w_uke,
                start_line=4,
                finger_placement=chord_finger,
                chord_name=song_cursor[selected_chord_idx]['chord_name'],
                chord_inv_serial=(1, len(chord_fingerings))
            )


@ui_lib.screen_arg_unpacker
def screen_chords(w: ui_lib.CursesMainWindow):
    w.clear()

    chords_banner = """\
   ________                   __     ____                                   
  / ____/ /_  ____  _________/ /____/ __ )_________ _      __________  _____
 / /   / __ \/ __ \/ ___/ __  / ___/ __  / ___/ __ \ | /| / / ___/ _ \/ ___/
/ /___/ / / / /_/ / /  / /_/ (__  ) /_/ / /  / /_/ / |/ |/ (__  )  __/ /    
\____/_/ /_/\____/_/   \__,_/____/_____/_/   \____/|__/|__/____/\___/_/     
    """
    
    w.print_banner(chords_banner, ul=(0, w.CENTER))

    print_uke_full(w, start_line=5)
    print_status_bar(w, '> (LEFT/Right) Cycle Fingerings; (^G) Select Chord; (^S) Search Chord; (^X) Main Menu')

    chord_name = ''
    chord_fgs = []
    current_chord_fg_idx = 0

    w.set_cursor_state(0)
    w.move_cursor((0, 0))

    # Create Ukulele object
    uke_obj = Ukulele()
    chroma_scale = uke_obj.gen_chroma_scale()

    while True:
        c = w.getch()

        if curses.ascii.unctrl(c) == '^G':
            # Select note
            note_idx = w.show_selector(size=(8, 35), choices=chroma_scale, msg='Step 1: Choose a note')

            # Select chord
            chord_types = ['Major', 'Minor', 'Dominant 7th', 'Major 7th', 'Minor 7th', 'Suspended (4th)', 'Suspended 2nd', 'Diminished', 'Augmented']
            chord_abbr = ['M', 'm', '7', 'M7', 'm7', 'sus4', 'sus2', 'dim', 'aug']
            quals_max_len = max([len(x) for x in chord_types])
            chord_idx = w.show_selector(size=(10, (quals_max_len * 2) + 3 + 6), choices=chord_types, msg='Step 2: Choose a type')

            chord_name = chroma_scale[note_idx] + chord_abbr[chord_idx]
            chord_fgs = uke_obj.get_chord_fingerings(chord_name)

            # Output first fingering on fret
            current_chord_fg_idx = 0
            print_uke_full(w, finger_placement=chord_fgs[current_chord_fg_idx], start_line=5, chord_name=chord_name, chord_inv_serial=(current_chord_fg_idx + 1, len(chord_fgs)))
        elif curses.ascii.unctrl(c) == '^S':
            try:
                chord_name = w.show_text_prompt(msg='Enter chord:')
                chord_fgs = uke_obj.get_chord_fingerings(chord_name)

                # Output first fingering on fret
                current_chord_fg_idx = 0
                print_uke_full(w, finger_placement=chord_fgs[current_chord_fg_idx], start_line=5, chord_name=chord_name, chord_inv_serial=(current_chord_fg_idx + 1, len(chord_fgs)))

                print_status_bar(w, '', lines_from_end=1)
            except ValueError:
                print_status_bar(w, '(w) Invalid chord entered!', lines_from_end=1)
        elif curses.ascii.unctrl(c) == '^Q':
            is_quitting = w.show_yn_prompt(msg='Quit Songhits?')

            if is_quitting:
                return SCREEN_QUIT
        elif curses.ascii.unctrl(c) == '^X':
            return SCREEN_MAIN
        else:
            # Arrow keys
            if w.which_arrow_key(c) == w.K_LEFT_ARROW:
                if current_chord_fg_idx > 0:
                    current_chord_fg_idx -= 1
                    print_uke_full(w, finger_placement=chord_fgs[current_chord_fg_idx], start_line=5, chord_name=chord_name, chord_inv_serial=(current_chord_fg_idx + 1, len(chord_fgs)))
            elif w.which_arrow_key(c) == w.K_RIGHT_ARROW:
                if current_chord_fg_idx + 1 < len(chord_fgs):
                    current_chord_fg_idx += 1
                    print_uke_full(w, finger_placement=chord_fgs[current_chord_fg_idx], start_line=5, chord_name=chord_name, chord_inv_serial=(current_chord_fg_idx + 1, len(chord_fgs)))

@ui_lib.screen_arg_unpacker
def screen_main_menu(w: ui_lib.CursesMainWindow):
    songhits_banner = """\
   _____                   __    _ __       __
  / ___/____  ____  ____ _/ /_  (_) /______/ /
  \__ \/ __ \/ __ \/ __ `/ __ \/ / __/ ___/ / 
 ___/ / /_/ / / / / /_/ / / / / / /_(__  )_/  
/____/\____/_/ /_/\__, /_/ /_/_/\__/____(_)   
                 /____/                       
    """

    w.clear()
    w.print_banner(songhits_banner, ul=(3, w.CENTER))
    print_status_bar(w, '> (i) UP and DOWN to choose; ENTER to select')

    cmd_list = ['Browse &Songlist', 'Browse &Ukulele Chords', '&Quit']
    cmd_pos_list = []
    cmd_max_len = max([len(x) for x in cmd_list])

    start_row = w.rows // 2
    start_col = (w.cols - cmd_max_len) // 2

    for i, each_cmd in enumerate(cmd_list):
        if i == len(cmd_list) - 1:
            i += 1

        cmd_pos_list.append((start_row + i, start_col))

    cmd_pos = 0

    while True:
        for i, (cmd_str, pos) in enumerate(zip(cmd_list, cmd_pos_list)):
            amp_loc = cmd_str.find('&')
            color_attr = w.color_pair_to_attr(0)

            if cmd_pos == i:
                color_attr = w.color_pair_to_attr(2)
            
            w.write_str(pos, f'{">" if cmd_pos == i else " "} {cmd_str}', attrs=color_attr)

            # Convert ampersand-ed letter to underline
            if amp_loc >= 0:
                w.write_str((pos[0], pos[1] + amp_loc + 2), cmd_str[amp_loc + 1], attrs=color_attr | curses.A_UNDERLINE)
                w.write_str((pos[0], pos[1] + amp_loc + 3), cmd_str[amp_loc + 2:], attrs=color_attr)
                w.write_str((pos[0], pos[1] + 2 + len(cmd_str) - 1), ' ')

        w.move_cursor(cmd_pos_list[cmd_pos])

        c = w.getch()

        if curses.ascii.unctrl(c) == '^Q':
            is_quitting = w.show_yn_prompt(msg='Quit Songhits?')

            if is_quitting:
                return SCREEN_QUIT
        elif w.is_enter_key(c):
            if cmd_pos == 0:
                return SCREEN_SONGLIST
            elif cmd_pos == 1:
                return SCREEN_CHORDS
            elif cmd_pos == 2:
                is_quitting = w.show_yn_prompt(msg='Quit Songhits?')

                if is_quitting:
                    return SCREEN_QUIT
        else:
            # Arrow keys
            if w.which_arrow_key(c) == w.K_UP_ARROW and cmd_pos > 0:
                cmd_pos -= 1
                pass
            elif w.which_arrow_key(c) == w.K_DOWN_ARROW and cmd_pos < len(cmd_list) - 1:
                cmd_pos += 1
                pass

def ui_main(w: ui_lib.CursesMainWindow):
    songlist_args = None
    next_screen, _ = screen_main_menu(w)

    while True:
        if next_screen == SCREEN_QUIT:
            # Quit
            break
        elif next_screen == SCREEN_MAIN:
            next_screen, _ = screen_main_menu(w)
        elif next_screen == SCREEN_SONGLIST:
            # Browse songs
            next_screen, songlist_args = screen_songlist(w)
        elif next_screen == SCREEN_SONGTEXT:
            # View song
            next_screen, _ = screen_song_text(w, songlist_args[0])
        elif next_screen == SCREEN_CHORDS:
            # Open ukulele chords
            next_screen, _ = screen_chords(w)

def main():
    ui_lib.CursesMainWindow.wrapper(ui_main)

if __name__ == '__main__':
    main()