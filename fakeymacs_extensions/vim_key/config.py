# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Vim 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vim_target
except:
    # Vim 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.vim_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", ["* - VIM*",
                                                                               "* - NVIM*",
                                                                               "* - Nvim*"]],
                     ]

try:
    # 設定されているか？
    fc.vim_keep_in_insert_mode
except:
    # インサートモードで C-g を押下した際、インサートモート居続けるかどうかを指定する
    # （True: インサートモードに居続ける、False: ノーマルモードに移行する）
    fc.vim_keep_in_insert_mode = False

try:
    # 設定されているか？
    fc.vim_insert_normal_mode_key
except:
    # インサートノーマルモードに移行するためのキーを指定する
    fc.vim_insert_normal_mode_key = "C-o"

# --------------------------------------------------------------------------------------------------

import re

class FakeymacsVim:
    pass

fakeymacs_vim = FakeymacsVim()

regex = "|".join([fnmatch.translate(app) for app in fc.vim_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
vim_target1 = re.compile(regex)
vim_target2 = [app for app in fc.vim_target if type(app) is list]

vim_status = False
vim_title = ""

def is_vim(window):
    global vim_status, vim_title

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == False and
            not getText(window).startswith("!") and
            (vim_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in vim_target2))):
            title = re.sub(r" [-(].*", "", getText(window))
            if vim_status:
                result1 = title.replace(vim_title, "")
                result2 = vim_title.replace(title, "")
                if " +" not in [result1, result2]:
                    vim_reset()
            else:
                vim_reset()

            vim_status = True
            vim_title = title
        else:
            vim_status = False

    return vim_status

if fc.use_emacs_ime_mode:
    keymap_vim = keymap.defineWindowKeymap(check_func=lambda wnd: (is_vim(wnd) and
                                                                   not is_emacs_ime_mode(wnd)))
else:
    keymap_vim = keymap.defineWindowKeymap(check_func=is_vim_target)

fakeymacs.keymap_vim = keymap_vim

fakeymacs_vim.insert_mode = False
fakeymacs_vim.visual_mode = False
fakeymacs_vim.single_line = None
fakeymacs_vim.vertical_movement = False
fakeymacs_vim.command_line_mode = False
fakeymacs_vim.insert_normal_mode = False

## 共通関数
def vim_reset():
    reset_search(reset_undo(reset_counter(lambda: None)))()
    escape()
    delay(0.05)
    escape()

def is_command_line():
    return (fakeymacs.is_searching == False or fakeymacs_vim.command_line_mode)

def is_normal_mode():
    return (not is_command_line() and
            not fakeymacs_vim.visual_mode and
            not fakeymacs_vim.insert_normal_mode and
            not fakeymacs_vim.insert_mode)

def is_insert_mode():
    return (not is_command_line() and
            not fakeymacs_vim.visual_mode and
            not fakeymacs_vim.insert_normal_mode and
            fakeymacs_vim.insert_mode)

def is_insert_normal_mode():
    return (not is_command_line() and
            fakeymacs_vim.insert_normal_mode)

def is_visual_mode():
    return (not is_command_line() and
            fakeymacs_vim.visual_mode)

def is_text_mode1():
    return (is_command_line() or
            (not fakeymacs_vim.visual_mode and
             not fakeymacs_vim.insert_normal_mode and
             fakeymacs_vim.insert_mode))

def is_text_mode2():
    return (is_command_line() or
            fakeymacs_vim.visual_mode or
            (not fakeymacs_vim.insert_normal_mode and
             fakeymacs_vim.insert_mode))

def define_key_v(keys, command, skip_check=True):
    if skip_check:
        # 設定をスキップするキーの処理を行う
        if "keymap_vim" in fc.skip_settings_key:
            for skey in fc.skip_settings_key["keymap_vim"]:
                if fnmatch.fnmatch(keys, skey):
                    print(f"skip settings key : [keymap_vim] {keys}")
                    return

    define_key(keymap_vim, keys, command)

def self_insert_command_v(*key_list, usjis_conv=True):
    func = self_insert_command2(*key_list, usjis_conv=usjis_conv)
    def _func():
        # ノーマルモードで日本語を入力した際は、インサートモードにする
        if getImeStatus():
            if is_normal_mode():
                fakeymacs_vim.insert_mode = True
                adjust_ime_status(self_insert_command("i"))()
        func()
    return _func

def adjust_ime_status(command):
    def _func():
        ime_status = getImeStatus()
        if ime_status:
            setImeStatus(0)
        command()
        if fakeymacs_vim.insert_mode:
            if ime_status:
                delay()
                setImeStatus(1)
    return _func

def execute_command(command):
    def _func():
        command()
        fakeymacs_vim.insert_normal_mode = False
    return _func

def execute_nm_command(nm_command, esc=False):
    def _func():
        if is_command_line():
            return False

        if esc:
            escape()
            delay(0.05)
            escape()

        if (not fakeymacs_vim.insert_normal_mode and
            not fakeymacs_vim.visual_mode and
            fakeymacs_vim.insert_mode):
            self_insert_command(fc.vim_insert_normal_mode_key)()

        adjust_ime_status(nm_command)()

        fakeymacs_vim.visual_mode = False
        fakeymacs_vim.insert_normal_mode = False

        return True
    return _func

def execute_ex_command(ex_command, enter=True, esc=False):
    def _func():
        if is_command_line():
            return False

        if esc:
            escape()
            delay(0.05)
            escape()

        def _command():
            self_insert_command(":")()
            princ(ex_command)
            if enter:
                self_insert_command("Enter")()

        if (not fakeymacs_vim.insert_normal_mode and
            not fakeymacs_vim.visual_mode and
            fakeymacs_vim.insert_mode):
            self_insert_command(fc.vim_insert_normal_mode_key)()

        if enter:
            adjust_ime_status(_command)()
        else:
            setImeStatus(0)
            _command()
            fakeymacs_vim.command_line_mode = True

        fakeymacs_vim.visual_mode = False
        fakeymacs_vim.insert_normal_mode = False

        return True
    return _func

def enter_insert_mode(key):
    def _func():
        if is_text_mode1():
            reset_undo(reset_counter(repeat(self_insert_command_v(key))))()
        else:
            reset_undo(reset_counter(self_insert_command_v(key)))()

            if is_visual_mode():
                if key in ["S-i", "S-a", "S-r", "s", "S-s", "c", "S-c"]:
                    fakeymacs_vim.visual_mode = False
                    fakeymacs_vim.insert_normal_mode = False
                    fakeymacs_vim.insert_mode = True

            elif is_insert_normal_mode():
                fakeymacs_vim.insert_normal_mode = False
            else:
                fakeymacs_vim.insert_mode = True
    return _func

def enter_visual_mode(key):
    def _func():
        if is_text_mode1():
            reset_undo(reset_counter(repeat(self_insert_command_v(key))))()
        else:
            reset_undo(reset_counter(set_mark_command(key)))()
    return _func

def enter_insert_normal_mode():
    if is_insert_normal_mode():
        self_insert_command(fc.vim_insert_normal_mode_key)()
        fakeymacs_vim.insert_normal_mode = False

    elif is_insert_mode():
        self_insert_command(fc.vim_insert_normal_mode_key)()
        setImeStatus(0)
        fakeymacs_vim.insert_normal_mode = True

def enter_command_line_mode(key):
    def _func():
        if is_text_mode1():
            reset_undo(reset_counter(repeat(self_insert_command(key))))()
        else:
            setImeStatus(0)
            reset_undo(reset_counter(execute_command(self_insert_command(key))))()
            fakeymacs_vim.command_line_mode = True
    return _func

def enter_search_mode(direction):
    def _func():
        if is_text_mode1():
            reset_undo(reset_counter(repeat(
                self_insert_command({"backward":"?", "forward":"/"}[direction]))))()
        else:
            setImeStatus(0)
            reset_undo(reset_counter(execute_command(
                self_insert_command({"backward":"?", "forward":"/"}[direction]))))()
            fakeymacs.is_searching = False
    return _func

## ファイル操作
def find_file():
    execute_ex_command("edit ", enter=False, esc=True)()

def save_buffer():
    execute_ex_command("write")()

def write_file():
    execute_ex_command("write ", enter=False)()

## カーソル移動
def backward_char():
    execute_command(self_insert_command("Left"))()

def forward_char():
    execute_command(self_insert_command("Right"))()

def backward_word():
    execute_command(self_insert_command("C-Left"))()

def forward_word():
    execute_command(self_insert_command("C-Right"))()

def previous_line():
    execute_command(self_insert_command("Up"))()
    fakeymacs_vim.vertical_movement = True

def next_line():
    execute_command(self_insert_command("Down"))()
    fakeymacs_vim.vertical_movement = True

def move_beginning_of_line():
    execute_command(self_insert_command("Home"))()

def move_end_of_line():
    if is_text_mode2():
        execute_command(self_insert_command("End"))()
    else:
        execute_command(self_insert_command("End", "Right"))()

def beginning_of_buffer():
    execute_command(self_insert_command("Home", "C-Home"))()
    fakeymacs_vim.vertical_movement = True

def end_of_buffer():
    execute_command(self_insert_command("C-End", "Right"))()
    fakeymacs_vim.vertical_movement = True

def goto_line():
    execute_ex_command("", enter=False)()

def scroll_up():
    execute_command(self_insert_command("PageUp"))()

def scroll_down():
    execute_command(self_insert_command("PageDown"))()

def recenter():
    execute_nm_command(self_insert_command("z", "z"))()

## カット / コピー / 削除 / アンドゥ
def delete_backward_char():
    if is_command_line():
        self_insert_command("Back")()

    elif is_visual_mode():
        execute_nm_command(self_insert_command("x"))()
    else:
        execute_nm_command(self_insert_command("S-x"))()

def delete_char():
    if is_command_line():
        self_insert_command("Delete")()

    elif is_visual_mode():
        execute_nm_command(self_insert_command("x"))()
    else:
        # 改行も削除できるようにビジュアルモードに移行してから削除している
        execute_nm_command(self_insert_command("v", "x"))()

def backward_kill_word():
    execute_nm_command(self_insert_command("d", "b"))()

def kill_word():
    execute_nm_command(self_insert_command("d", "w"))()

def kill_line():
    if is_visual_mode():
        escape()

    execute_nm_command(self_insert_command("v", "$", "Delete"))()

def kill_region():
    if is_visual_mode():
        if fakeymacs_vim.vertical_movement:
            fakeymacs_vim.single_line = False
        else:
            fakeymacs_vim.single_line = True

    execute_nm_command(self_insert_command("x"))()

def kill_ring_save():
    if is_visual_mode():
        execute_nm_command(self_insert_command("y"))()

        if fakeymacs_vim.vertical_movement:
            fakeymacs_vim.single_line = False
        else:
            fakeymacs_vim.single_line = True

def yank():
    if execute_nm_command(self_insert_command("S-p"))():
        if fakeymacs_vim.single_line:
            if not is_insert_mode():
                forward_char()

def undo():
    if fakeymacs.is_undo_mode:
        execute_nm_command(self_insert_command("u"))()
    else:
        execute_nm_command(self_insert_command("C-r"))()

def set_mark_command(key):
    def _func():
        if not is_command_line():
            if is_visual_mode():
                if fakeymacs_vim.visual_key == key:
                    escape()
                else:
                    execute_nm_command(self_insert_command(key))()
                    fakeymacs_vim.visual_mode = True
                    fakeymacs_vim.visual_key = key
                    if key != "v":
                        fakeymacs_vim.vertical_movement = True
            else:
                execute_nm_command(self_insert_command(key))()
                fakeymacs_vim.visual_mode = True
                fakeymacs_vim.visual_key = key
                if key == "v":
                    fakeymacs_vim.vertical_movement = False
                else:
                    fakeymacs_vim.vertical_movement = True
    return _func

def mark_whole_buffer():
    if not is_command_line():
        if is_visual_mode():
            escape()

        end_of_buffer()
        set_mark_command("S-v")()
        beginning_of_buffer()

def mark_page():
    mark_whole_buffer()

## テキストの入れ替え
def transpose_chars():
    if not is_command_line():
        delete_char()
        backward_char()
        yank()
        forward_char()

## バッファ操作
def kill_buffer():
    execute_ex_command("bp|bd#", esc=True)()

def previous_buffer():
    execute_ex_command("bprevious", esc=True)()

def next_buffer():
    execute_ex_command("bnext", esc=True)()

def switch_to_buffer():
    next_buffer()

def list_buffers():
    if execute_ex_command("ls", esc=True)():
        fakeymacs_vim.command_line_mode = True

## ウィンドウ操作
def delete_window():
    execute_nm_command(self_insert_command("C-w", "c"), esc=True)()

def delete_other_windows():
    execute_nm_command(self_insert_command("C-w", "o"))()

def split_window_below():
    execute_ex_command("split")()

def split_window_right():
    execute_ex_command("vsplit")()

def other_window():
    execute_nm_command(self_insert_command("C-w", "w"), esc=True)()

## タブ操作
def create_tab():
    execute_ex_command("tabnew ", enter=False, esc=True)()

def close_tab():
    execute_ex_command("tabclose", esc=True)()

def previous_tab():
    execute_ex_command("tabprevious", esc=True)()

def next_tab():
    execute_ex_command("tabnext", esc=True)()

def list_tabs():
    execute_ex_command("tabs", esc=True)()

## 文字列検索
def isearch(direction):
    def _func():
        if fakeymacs.is_searching is None:
            if execute_nm_command(
                    self_insert_command({"backward":"?", "forward":"/"}[direction]))():
                fakeymacs.is_searching = False

        elif fakeymacs.is_searching == False:
            self_insert_command({"backward":"C-t", "forward":"C-g"}[direction])()

        elif fakeymacs.is_searching == True:
            execute_nm_command(
                self_insert_command({"backward":"S-n", "forward":"n"}[direction]))()
    return _func

def isearch_backward():
    isearch("backward")()

def isearch_forward():
    isearch("forward")()

## キーボードマクロ
def keyboard_macro_start():
    execute_nm_command(self_insert_command("q", "a"), esc=True)()

def keyboard_macro_stop():
    execute_nm_command(self_insert_command("q"), esc=True)()

def keyboard_macro_play():
    execute_nm_command(self_insert_command("@", "a"), esc=True)()

## 矩形選択
def rectangle_mark_mode():
    execute_nm_command(self_insert_command("C-v"))()

## その他
def escape(keep_in_im=False):
    # print("<escape 実行前> " + "-" * 80)
    # print("fakeymacs_vim.insert_mode        : " + str(fakeymacs_vim.insert_mode))
    # print("fakeymacs_vim.visual_mode        : " + str(fakeymacs_vim.visual_mode))
    # print("fakeymacs_vim.command_line_mode  : " + str(fakeymacs_vim.command_line_mode))
    # print("fakeymacs_vim.insert_normal_mode : " + str(fakeymacs_vim.insert_normal_mode))
    # print("")

    if is_command_line():
        self_insert_command("Esc")()
        fakeymacs_vim.command_line_mode = False

    elif is_insert_mode():
        if not keep_in_im:
            setImeStatus(0)
            self_insert_command("Esc", "Right")()
            fakeymacs_vim.insert_mode = False

    elif is_visual_mode():
        self_insert_command("Esc")()
        fakeymacs_vim.visual_mode = False
    else:
        self_insert_command("Esc")()
        fakeymacs_vim.insert_normal_mode = False

    # print("<escape 実行後> " + "-" * 80)
    # print("fakeymacs_vim.insert_mode        : " + str(fakeymacs_vim.insert_mode))
    # print("fakeymacs_vim.visual_mode        : " + str(fakeymacs_vim.visual_mode))
    # print("fakeymacs_vim.command_line_mode  : " + str(fakeymacs_vim.command_line_mode))
    # print("fakeymacs_vim.insert_normal_mode : " + str(fakeymacs_vim.insert_normal_mode))
    # print("")

def space():
    self_insert_command("Space")()

def newline(enter_im=False):
    def _func():
        if enter_im:
            if is_normal_mode():
                fakeymacs_vim.insert_mode = True
                adjust_ime_status(self_insert_command("i"))()

        self_insert_command("Enter")()

        fakeymacs_vim.command_line_mode = False
        if fakeymacs.is_searching == False:
            fakeymacs.is_searching = True
    return _func

def indent_for_tab_command():
    self_insert_command("Tab")()

def keyboard_quit():
    if is_normal_mode() or is_insert_mode():
        if fakeymacs.is_undo_mode:
            fakeymacs.is_undo_mode = False
        else:
            fakeymacs.is_undo_mode = True

    escape(keep_in_im=fc.vim_keep_in_insert_mode)

    if fakeymacs.is_searching == False:
        fakeymacs.is_searching = None

    elif fakeymacs.is_searching == True:
        execute_ex_command("nohlsearch")()

def execute_extended_command():
    execute_ex_command("", enter=False, esc=True)()

def kill_emacs():
    setImeStatus(0)
    execute_ex_command("quit")()

## マルチストロークキーの設定
define_key_v("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_v("C-q",    keymap.defineMultiStrokeKeymap("C-q"))
define_key_v("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_v("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_v("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

## 数字キーの設定
for n in range(10):
    key = str(n)
    define_key_v(key, digit(n))
    if fc.use_ctrl_digit_key_for_digit_argument:
        define_key(keymap_emacs, f"C-{key}", digit2(n))
    define_key_v(f"M-{key}", digit2(n))
    define_key_v(f"S-{key}",
                 reset_undo(reset_counter(repeat(execute_command(self_insert_command_v(f"S-{key}"))))))

## アルファベットキーの設定
for vkey in range(VK_A, VK_Z + 1):
    key = vkToStr(vkey)
    for mod in ["", "S-"]:
        mkey = mod + key
        define_key_v(mkey, reset_undo(reset_counter(repeat(execute_command(self_insert_command_v(mkey))))))

## 特殊文字キーの設定
define_key_v("Space"  , reset_undo(reset_counter(repeat(execute_command(self_insert_command("Space"))))))
define_key_v("S-Space", reset_undo(reset_counter(repeat(execute_command(self_insert_command("S-Space"))))))

for vkey in [VK_OEM_MINUS, VK_OEM_PLUS, VK_OEM_COMMA, VK_OEM_PERIOD,
             VK_OEM_1, VK_OEM_2, VK_OEM_3, VK_OEM_4, VK_OEM_5, VK_OEM_6, VK_OEM_7, VK_OEM_102]:
    key = vkToStr(vkey)
    for mod in ["", "S-"]:
        mkey = mod + key
        define_key_v(mkey, reset_undo(reset_counter(repeat(execute_command(self_insert_command_v(mkey))))))

## 10key の特殊文字キーの設定
for vkey in [VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE]:
    key = vkToStr(vkey)
    define_key_v(key, reset_undo(reset_counter(repeat(execute_command(self_insert_command_v(key))))))

## quoted-insert キーの設定
for vkey in vkeys():
    key = vkToStr(vkey)
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mkey = mod1 + mod2 + mod3 + mod4 + key
        define_key_v(f"C-q {mkey}", execute_command(self_insert_command(mkey)))

## Esc キーの設定
if fc.use_esc_as_meta:
    define_key_v("Esc Esc", escape)
else:
    define_key_v("Esc", escape)

if fc.use_ctrl_openbracket_as_meta:
    define_key_v("C-[ C-[", escape)
else:
    define_key_v("C-[", escape)

## 「インサートモード移行」のキー設定
for key in ["i", "S-i", "a", "S-a", "o", "S-o", "S-r", "s", "S-s", "c", "S-c"]:
    define_key_v(key, enter_insert_mode(key))

## 「ビジュアルモード移行」のキーの設定
for key in ["v", "S-v"]:
    define_key_v(key, enter_visual_mode(key))

## 「インサートノーマルモード移行」のキー設定
if not getKeyCommand(keymap_ime, "C-o"):
    define_key_v("C-o", enter_insert_normal_mode)

define_key_v("C-A-o", enter_insert_normal_mode)

## 「コマンドラインモード移行」のキー設定
for key in [":", "!"]:
    define_key_v(key, enter_command_line_mode(key))

## 「検索モード移行」のキー設定
define_key_v("/", enter_search_mode("forward"))
define_key_v("?", enter_search_mode("backward"))

## universal-argument キーの設定
define_key_v("C-u", universal_argument)

## 「ファイル操作」のキー設定
define_key_v("Ctl-x C-f", reset_undo(reset_counter(find_file)))
define_key_v("Ctl-x C-s", reset_undo(reset_counter(save_buffer)))
define_key_v("Ctl-x C-w", reset_undo(reset_counter(write_file)))

## 「カーソル移動」のキー設定
define_key_v("C-b",      reset_undo(reset_counter(repeat(backward_char))))
define_key_v("C-f",      reset_undo(reset_counter(repeat(forward_char))))
define_key_v("M-b",      reset_undo(reset_counter(repeat(backward_word))))
define_key_v("M-f",      reset_undo(reset_counter(repeat(forward_word))))
define_key_v("C-p",      reset_undo(reset_counter(repeat(previous_line))))
define_key_v("C-n",      reset_undo(reset_counter(repeat(next_line))) )
define_key_v("C-a",      reset_undo(reset_counter(move_beginning_of_line)))
define_key_v("C-e",      reset_undo(reset_counter(move_end_of_line)))
define_key_v("M-<",      reset_undo(reset_counter(beginning_of_buffer)))
define_key_v("M->",      reset_undo(reset_counter(end_of_buffer)))
define_key_v("M-g g",    reset_undo(reset_counter(goto_line)))
define_key_v("M-g M-g",  reset_undo(reset_counter(goto_line)))
define_key_v("C-l",      reset_undo(reset_counter(recenter)))

define_key_v("Left",     reset_undo(reset_counter(repeat(backward_char))))
define_key_v("Right",    reset_undo(reset_counter(repeat(forward_char))))
define_key_v("C-Left",   reset_undo(reset_counter(repeat(backward_word))))
define_key_v("C-Right",  reset_undo(reset_counter(repeat(forward_word))))
define_key_v("Up",       reset_undo(reset_counter(repeat(previous_line))))
define_key_v("Down",     reset_undo(reset_counter(repeat(next_line))))
define_key_v("Home",     reset_undo(reset_counter(move_beginning_of_line)))
define_key_v("End",      reset_undo(reset_counter(move_end_of_line)))
define_key_v("C-Home",   reset_undo(reset_counter(beginning_of_buffer)))
define_key_v("C-End",    reset_undo(reset_counter(end_of_buffer)))
define_key_v("PageUp",   reset_undo(reset_counter(scroll_up)))
define_key_v("PageDown", reset_undo(reset_counter(scroll_down)))

## 「カット / コピー / 削除 / アンドゥ」のキー設定
define_key_v("C-h",      reset_undo(reset_counter(repeat(delete_backward_char))))
define_key_v("C-d",      reset_undo(reset_counter(repeat(delete_char))))
define_key_v("M-Delete", reset_undo(reset_counter(repeat(backward_kill_word))))
define_key_v("M-d",      reset_undo(reset_counter(repeat(kill_word))))
define_key_v("C-k",      reset_undo(reset_counter(repeat(kill_line))))
define_key_v("C-w",      reset_undo(reset_counter(kill_region)))
define_key_v("M-w",      reset_undo(reset_counter(kill_ring_save)))
define_key_v("C-y",      reset_undo(reset_counter(repeat(yank))))
define_key_v("C-/",      reset_counter(undo))
define_key_v("Ctl-x u",  reset_counter(undo))

define_key_v("Back",      reset_undo(reset_counter(repeat(delete_backward_char))))
define_key_v("Delete",    reset_undo(reset_counter(repeat(delete_char))))
define_key_v("C-Back",    reset_undo(reset_counter(repeat(backward_kill_word))))
define_key_v("C-Delete",  reset_undo(reset_counter(repeat(kill_word))))
define_key_v("C-c",       reset_undo(reset_counter(kill_ring_save)))
define_key_v("C-v",       reset_undo(reset_counter(repeat(yank))))
define_key_v("C-z",       reset_counter(undo))
define_key_v("C-_",       reset_counter(undo))
define_key_v("C-@",       reset_undo(reset_counter(set_mark_command("v"))))
define_key_v("C-Space",   reset_undo(reset_counter(set_mark_command("v"))))
define_key_v("Ctl-x h",   reset_undo(reset_counter(mark_whole_buffer)))
define_key_v("Ctl-x C-p", reset_undo(reset_counter(mark_page)))

## 「テキストの入れ替え」のキー設定
define_key_v("C-t", reset_undo(reset_counter(transpose_chars)))

## 「バッファ操作」のキー設定
define_key_v("M-k",       reset_undo(reset_counter(kill_buffer)))
define_key_v("Ctl-x k",   reset_undo(reset_counter(kill_buffer)))
define_key_v("Ctl-x b",   reset_undo(reset_counter(switch_to_buffer)))
define_key_v("Ctl-x C-b", reset_undo(reset_counter(list_buffers)))

define_key_v("M-p",       reset_undo(reset_counter(previous_buffer)))
define_key_v("M-n",       reset_undo(reset_counter(next_buffer)))
define_key_v("M-Up",      reset_undo(reset_counter(previous_buffer)))
define_key_v("M-Down",    reset_undo(reset_counter(next_buffer)))

## 「ウィンドウ操作」のキー設定
define_key_v("Ctl-x 0",   reset_undo(reset_counter(delete_window)))
define_key_v("Ctl-x 1",   delete_other_windows)
define_key_v("Ctl-x 2",   split_window_below)
define_key_v("Ctl-x 3",   split_window_right)
define_key_v("Ctl-x o",   reset_undo(reset_counter(other_window)))

## 「タブ操作」のキー設定
define_key_v("C-A-t", reset_undo(reset_counter(create_tab)))
define_key_v("C-A-c", reset_undo(reset_counter(close_tab)))
define_key_v("C-A-p", reset_undo(reset_counter(previous_tab)))
define_key_v("C-A-n", reset_undo(reset_counter(next_tab)))
define_key_v("C-A-l", reset_undo(reset_counter(list_tabs)))

## 「文字列検索」のキー設定
define_key_v("C-r", reset_undo(reset_counter(isearch_backward)))
define_key_v("C-s", reset_undo(reset_counter(isearch_forward)))

## 「キーボードマクロ」のキー設定
define_key_v("Ctl-x (", keyboard_macro_start)
define_key_v("Ctl-x )", keyboard_macro_stop)
define_key_v("Ctl-x e", reset_undo(reset_counter(repeat(keyboard_macro_play))))

## 「矩形選択」のキー設定
define_key_v("C-A-Space", reset_undo(reset_counter(set_mark_command("C-v"))))

## 「その他」のキー設定
define_key_v("Enter",     reset_undo(reset_counter(repeat(newline()))))
define_key_v("C-m",       reset_undo(reset_counter(repeat(newline()))))
define_key_v("C-Enter",   reset_undo(reset_counter(repeat(newline(enter_im=True)))))
define_key_v("C-g",       reset_search(reset_counter(keyboard_quit)))
define_key_v("M-x",       reset_undo(reset_counter(execute_extended_command)))
define_key_v("Ctl-x C-c", reset_undo(reset_counter(kill_emacs)))

## 「タブ」のキー設定
if fc.use_ctrl_i_as_tab:
    define_key_v("C-i", reset_undo(reset_counter(indent_for_tab_command)))

## 「スクロール」のキー設定
if fc.scroll_key:
    define_key_v(fc.scroll_key[0], reset_undo(reset_counter(scroll_up)))
    define_key_v(fc.scroll_key[1], reset_undo(reset_counter(scroll_down)))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"vim_key\config_personal.py", msg=False), dict(globals(), **locals()))
