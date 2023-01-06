import sys
import os
import functools

import curses
import curses.textpad
import curses.ascii

class CursesTerm:
    K_UP_ARROW = curses.KEY_UP
    K_DOWN_ARROW = curses.KEY_DOWN
    K_LEFT_ARROW = curses.KEY_LEFT
    K_RIGHT_ARROW = curses.KEY_RIGHT

    def __init__(self, run_init: bool=False):
        if run_init:
            self.init_color_pairs()
    
    @classmethod
    def which_arrow_key(cls, key: int):
        curses_to_const = {
            curses.KEY_UP: cls.K_UP_ARROW,
            curses.KEY_DOWN: cls.K_DOWN_ARROW,
            curses.KEY_LEFT: cls.K_LEFT_ARROW,
            curses.KEY_RIGHT: cls.K_RIGHT_ARROW
        }

        if key in curses_to_const:
            return curses_to_const[key]

        return None
    
    @classmethod
    def which_fn_key(cls, key: int):
        curses_to_const = [
            curses.KEY_F1, curses.KEY_F2, curses.KEY_F3, curses.KEY_F4,
            curses.KEY_F5, curses.KEY_F6, curses.KEY_F7, curses.KEY_F8,
            curses.KEY_F9, curses.KEY_F10, curses.KEY_F11, curses.KEY_F12,
        ]

        if key in curses_to_const:
            return curses_to_const.index(key) + 1

        return None
    
    @classmethod
    def is_enter_key(cls, key: int):
        return key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r')

    @classmethod
    def set_cursor_state(cls, visibility):
        curses.curs_set(visibility)

    @classmethod
    def init_color_pairs(cls):
        # Fixed color pairs
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)

    @classmethod
    def color_pair_to_attr(cls, pair_idx: int, **cell_attrs):
        other_attrs = 0

        kwargs_to_attr = {
            'b': curses.A_BOLD,
            'i': curses.A_ITALIC,
            'reverse_color': curses.A_REVERSE,
            'u': curses.A_UNDERLINE,
        }

        for each_attr_name, each_attr_val in kwargs_to_attr.items():
            if each_attr_name in cell_attrs:
                other_attrs |= each_attr_val if cell_attrs[each_attr_name] else 0

        return curses.color_pair(pair_idx) | other_attrs

    @classmethod
    def cursor_pos(cls):
        return curses.getsyx()

    @classmethod
    def screen_dim(cls):
        return (curses.LINES, curses.COLS)

    @classmethod
    def get_center_ul(cls, win_dim: tuple|list=None):
        term_dim = cls.screen_dim()

        return ((term_dim[0] - win_dim[0]) // 2, (term_dim[1] - win_dim[1]) // 2)

class CursesWindow(CursesTerm):    
    CENTER = -1

    def __init__(self, w, dims: tuple|list, ul: tuple|list=(0, 0), run_init: bool=False):
        self._w = w

        self._top = ul[0]
        self._left = ul[1]
        self._rows = dims[0]
        self._cols = dims[1]

        super().__init__(run_init)

    @staticmethod
    def new_window(win_dim: tuple|list, ul: tuple|list=(0, 0)):
        w = curses.newwin(win_dim[0], win_dim[1], ul[0], ul[1])

        return CursesWindow(w, win_dim, ul=ul)
    
    @staticmethod
    def new_center_window(win_dim: tuple|list):
        center_ul = CursesTerm.get_center_ul(win_dim)
        
        return CursesWindow.new_window(win_dim, ul=center_ul)
    
    @staticmethod
    def new_textbox(win_dim: tuple|list, ul=(0, 0)):
        w = curses.newwin(win_dim[0], win_dim[1], ul[0], ul[1])

        return CursesTextWindow(w, win_dim, ul=ul)

    def filter_center_coords(self, coord: tuple):
        if len(coord) != 2:
            raise ValueError('Dimension count not equal to two!')
        
        new_coord = [coord[0], coord[1]]

        if coord[0] == self.CENTER:
            new_coord[0] = self.rows // 2

        if coord[1] == self.CENTER:
            new_coord[1] = self.cols // 2

        return new_coord

    def dims(self):
        return (self._rows, self._cols)

    @property
    def top(self):
        return self._top
    
    @property
    def left(self):
        return self._left

    @property
    def rows(self):
        return self._rows
    
    @property
    def cols(self):
        return self._cols

    def color_and_box(self, attrs=0):
        self._w.bkgd(' ', attrs)
        self._w.box()

    def coord_in_win(self, coord: tuple|list):
        return (coord[0] == self.CENTER or 0 <= coord[0] < self.rows) and \
            (coord[1] == self.CENTER or 0 <= coord[1] < self.cols)

    def write_str(self, coord: tuple|list, msg: str, attrs=0):
        new_coord = self.filter_center_coords(coord)

        if not self.coord_in_win(coord):
            return
        
        # Clip string if length exceeds window size
        if not self.coord_in_win((new_coord[0], new_coord[1] + len(msg))):
            msg = msg[:self.cols - new_coord[1] + 1]
        
        if coord[1] == CursesMainWindow.CENTER:
            new_coord[1] -= len(msg) // 2
        
        cur_pos = self.cursor_pos()
        self._w.addstr(new_coord[0], new_coord[1], msg, attrs)
        self.move_cursor(cur_pos)

    def move_cursor(self, coord: tuple|list):
        if not self.coord_in_win(coord):
            return

        self._w.move(coord[0], coord[1])

    def getch(self):
        return self._w.getch()

    def refresh(self):
        self._w.touchwin()
        self._w.refresh()

    def clear(self):
        self._w.clear()


class CursesTextWindow(CursesWindow):
    def __init__(self, w, dims: tuple|list, ul: tuple|list=(0, 0)):
        self._w_tbox = curses.newwin(dims[0] - 2, dims[1] - 4, ul[0] + 1, ul[1] + 2)
        self._tbox = curses.textpad.Textbox(self._w_tbox)

        super().__init__(w, dims, ul=ul, run_init=False)

    def color_and_box(self, attrs=0):
        self._w_tbox.bkgd(' ', attrs)

        super().color_and_box(attrs)

    def get_input(self):
        return self._tbox.edit()


class CursesScrollableWindow(CursesWindow):
    def __init__(self, dims: tuple|list, ul: tuple|list=(0, 0), pad_dim: tuple|list=None):
        w_content = curses.newpad(pad_dim[0], pad_dim[1])
        w_content.scrollok(True)
        w_content.idlok(True)

        self._w_border = CursesWindow(curses.newwin(dims[0], dims[1], ul[0], ul[1]), dims, ul=ul)
        self._w_border.color_and_box(attrs=self.color_pair_to_attr(2))
        self._w_border.refresh()

        super().__init__(w_content, pad_dim, ul=(ul[0] + 1, ul[1] + 1), run_init=False)
        
        self._ul_pad = [0, 0]
        self._pos_in_pad = [0, 0]
        self._pad_dim = pad_dim if pad_dim is not None else (self.rows - 1, self.cols - 1)

    @property
    def border_rows(self):
        return self._w_border.rows
    
    @property
    def border_cols(self):
        return self._w_border.cols

    @property
    def pos_in_pad(self):
        return self._pos_in_pad

    def refresh(self):
        self._w_border.color_and_box(attrs=self.color_pair_to_attr(2))
        self._w_border.refresh()
        
        self._w.bkgd(' ', self.color_pair_to_attr(2))
        self._w.refresh(self._ul_pad[0], self._ul_pad[1], self.top, self.left, self.top + self._w_border.rows - 3, self.left + self._w_border.cols - 3)
    
    def scroll(self, scroll_dir):
        dir_dict = {
            self.K_UP_ARROW: (-1, 0),
            self.K_DOWN_ARROW: (1, 0),
            self.K_LEFT_ARROW: (0, -1),
            self.K_RIGHT_ARROW: (0, 1),
        }

        if scroll_dir not in dir_dict:
            return

        # Set cursor position within pad
        new_pos_in_pad = [x + y for x, y in zip(self._pos_in_pad, dir_dict[scroll_dir])]

        if 0 <= new_pos_in_pad[0] < self._pad_dim[0] and 0 <= new_pos_in_pad[1] < self._pad_dim[1]:
            self._pos_in_pad = new_pos_in_pad
        
        # Set ul pad
        if self._pos_in_pad[0] - self._ul_pad[0] >= self._w_border.rows - 2:
            self._ul_pad[0] += 1
        elif self._pos_in_pad[0] - self._ul_pad[0] < 0:
            self._ul_pad[0] -= 1

        if self._pos_in_pad[1] - self._ul_pad[1] >= self._w_border.cols - 2:
            self._ul_pad[1] += 1
        elif self._pos_in_pad[1] - self._ul_pad[1] < 0:
            self._ul_pad[1] -= 1

        self.refresh()


class CursesMainWindow(CursesWindow):
    def __init__(self, stdscr: CursesWindow):
        super().__init__(stdscr, (curses.LINES, curses.COLS), run_init=True)

    @classmethod
    def wrapper(cls, entry_fcn, *args, **kwargs):
        def wfcn(stdscr):
            a = CursesMainWindow(stdscr)

            entry_fcn(a, *args, **kwargs)

        # Placed on top of main() to "release"
        # the special keys
        if sys.platform.startswith(('darwin', 'linux')):
            os.system('stty -ixon')
            os.system('stty -iexten')

        curses.wrapper(wfcn)

        # Placed just before exiting to revert the terminal
        # to its original configuration
        if sys.platform.startswith(('darwin', 'linux')):
            os.system('stty ixon')
            os.system('stty iexten')

    def print_banner(self, banner: str, ul: tuple|list=(CursesWindow.CENTER, CursesWindow.CENTER)):
        banner_ul = self.filter_center_coords(ul)

        if ul[1] == CursesMainWindow.CENTER:
            banner_max_len = max([len(x) for x in banner.split('\n')])
            banner_ul[1] -= banner_max_len // 2

        for i, each_line in enumerate(banner.split('\n')):
            self.write_str((banner_ul[0] + i, banner_ul[1]), each_line)


    def show_selector(self, size: tuple|list=(10, 40), choices: tuple|list=[], msg: str='Choose one.'):
        choice_max_len = max([len(x) for x in choices])

        def pos_rel_to_win(i):
            return (3 + (i % (sel_w.rows - 4)), (2 + (3 + choice_max_len + 1) * (i // (sel_w.rows - 4))))

        current_cur = self.cursor_pos()

        sel_w = CursesWindow.new_center_window(size)
        sel_w.color_and_box(sel_w.color_pair_to_attr(1))
        sel_w.write_str((1, 2), msg)

        for i, each_choice in enumerate(choices):
            pos = pos_rel_to_win(i)

            sel_w.write_str(pos, f'  {each_choice}')

        choice_pos = 0
        sel_w.write_str((3, 2), f'> {choices[choice_pos]}', attrs=sel_w.color_pair_to_attr(2))
        self.move_cursor((sel_w.top + 3, sel_w.left + 2))

        sel_w.refresh()

        while True:
            prompt_ch = self.getch()

            old_choice_pos = choice_pos
            new_choice_pos = choice_pos

            if prompt_ch == curses.KEY_DOWN:
                if choice_pos + 1 < len(choices) and (choice_pos + 1) % (sel_w.rows - 4) > 0:
                    new_choice_pos = old_choice_pos + 1
            elif prompt_ch == curses.KEY_UP:
                if choice_pos > 0 and choice_pos % (sel_w.rows - 4) > 0:
                    new_choice_pos = old_choice_pos - 1
            elif prompt_ch == curses.KEY_LEFT:
                if (choice_pos - (sel_w.rows - 4)) >= 0:
                    new_choice_pos = old_choice_pos - (sel_w.rows - 4)
            elif prompt_ch == curses.KEY_RIGHT:
                if (choice_pos + (sel_w.rows - 4)) < len(choices):
                    new_choice_pos = old_choice_pos + (sel_w.rows - 4)
            elif prompt_ch == curses.KEY_ENTER or prompt_ch == ord('\n') or prompt_ch == ord('\r'):
                break

            old_pos = pos_rel_to_win(choice_pos)
            new_pos = pos_rel_to_win(new_choice_pos)

            sel_w.write_str(old_pos, f'  {choices[old_choice_pos]}', attrs=sel_w.color_pair_to_attr(1))
            sel_w.write_str(new_pos, f'> {choices[new_choice_pos]}', attrs=sel_w.color_pair_to_attr(2))
            self.move_cursor((sel_w.top + new_pos[0], sel_w.left + new_pos[1]))

            choice_pos = new_choice_pos

            sel_w.refresh()
        
        del sel_w
        self.move_cursor(current_cur)
        self.refresh()

        return choice_pos

    def show_text_prompt(self, size: tuple|list=(3, 20), msg: str='Input text:'):
        if len(msg) >= size[1] - 4:
            # Chop off message if it overflows
            msg = msg[:size[1] - 4]

        current_cur = self.cursor_pos()

        text_w = CursesWindow.new_textbox(size, ul=CursesTerm.get_center_ul(size))
        text_w.color_and_box(text_w.color_pair_to_attr(1))
        text_w.write_str((0, 2), msg)
        text_w.refresh()

        txt_in = text_w.get_input().strip()

        del text_w
        self.move_cursor(current_cur)
        self.refresh()

        return txt_in

    def show_yn_prompt(self, size: tuple|list=(8, 40), msg: str='Are you sure?'):
        if len(msg) >= size[1]:
            # Chop off message if it overflows
            msg = msg[:size[1] - 4]
        
        if size[0] < 7 or size[1] < 14:
            raise Exception('Prompt dimensions are too small - minimum is (7, 14)')

        no_loc = (size[1] - len(msg)) // 2
        yes_loc = no_loc + (len(msg) - 5)

        current_cur = self.cursor_pos()
        self.set_cursor_state(1)

        prompt_w = CursesWindow.new_center_window(size)
        prompt_w.color_and_box(prompt_w.color_pair_to_attr(1))
        prompt_w.write_str((2, no_loc), msg)
        prompt_w.write_str((size[0] - 3, no_loc), '> No', attrs=prompt_w.color_pair_to_attr(2)) # Selected
        prompt_w.write_str((size[0] - 3, yes_loc), '  Yes')
        self.move_cursor((size[0] - 3 + prompt_w.top, no_loc + prompt_w.left))
        prompt_w.refresh()
        
        is_yes = False

        while True:
            prompt_ch = self.getch()

            if prompt_ch == curses.KEY_LEFT and is_yes:
                prompt_w.write_str((size[0] - 3, no_loc), '> No', attrs=prompt_w.color_pair_to_attr(2)) # Selected
                prompt_w.write_str((size[0] - 3, yes_loc), '  Yes')
                self.move_cursor((size[0] - 3 + prompt_w.top, no_loc + prompt_w.left))

                is_yes = not is_yes
            elif prompt_ch == curses.KEY_RIGHT and not is_yes:
                prompt_w.write_str((size[0] - 3, no_loc), '  No')
                prompt_w.write_str((size[0] - 3, yes_loc), '> Yes', attrs=prompt_w.color_pair_to_attr(2)) # Selected
                self.move_cursor((size[0] - 3 + prompt_w.top, yes_loc + prompt_w.left))

                is_yes = not is_yes
            elif prompt_ch == curses.KEY_ENTER or prompt_ch == ord('\n') or prompt_ch == ord('\r'):
                break

            prompt_w.refresh()

        self.set_cursor_state(1)

        if not is_yes:
            self.move_cursor(current_cur)

            del prompt_w
            self.refresh()
        
        return is_yes

def screen_arg_unpacker(fcn):
    @functools.wraps(fcn)
    def wrap(*args, **kwargs):
        retval = fcn(*args, **kwargs)

        if type(retval) is int:
            return (retval, ())

        if (type(retval) is tuple or type(retval) is list) and len(retval) >= 1:
            return (retval[0], retval[1:])
        
        raise SyntaxError('Return value in decorated function should either be "int" or tuple("int", ...).')

    return wrap