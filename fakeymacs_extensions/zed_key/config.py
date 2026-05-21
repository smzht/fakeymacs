# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Zed エディタ用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.zed_target
except:
    # Zed エディタ用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.zed_target = ["Zed.exe",
                     ]

# --------------------------------------------------------------------------------------------------

zed_target = targetRegexify(fc.zed_target)

def is_zed_target(window):
    global zed_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == True and
            (zed_target[0].match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in zed_target[1]))):
            zed_status = True
        else:
            zed_status = False

    return zed_status

if fc.use_emacs_ime_mode:
    keymap_zed = keymap.defineWindowKeymap(check_func=lambda wnd: (is_zed_target(wnd) and
                                                                   not is_emacs_ime_mode(wnd)))
else:
    keymap_zed = keymap.defineWindowKeymap(check_func=is_zed_target)

## 共通関数
def define_key_z(keys, command):
    define_key(keymap_zed, keys, command)

def zedExecuteCommand(command):
    def _func():
        self_insert_command("C-S-p")()
        keymap.InputTextCommand(command)()
        self_insert_command("Enter")()

    return executeCommandWithImeOff(_func, 0.1)

def region(func):
    def _func():
        func()
        fakeymacs.forward_direction = True
    return _func

## ファイル操作
def find_directory():
    # Zed Command : workspace: open
    self_insert_command("C-k", "C-o")()

def recentf():
    # Zed Command : projects: open recent
    self_insert_command("C-r")()

def locate():
    # Zed Command : file finder: toggle
    self_insert_command("C-p")()

def remote():
    # Zed Command : projects: open remote
    self_insert_command("C-A-S-o")()

## カーソル移動
def recenter():
    # Zed Command : editor: scroll cursor center
    zedExecuteCommand("editor: scroll cursor center")()

## ペイン操作
def delete_window():
    # Zed Command : pane: close all items
    self_insert_command4("C-k", "w")()

def delete_other_windows():
    # 適当なコマンドが見つからない
    pass

def split_window_below():
    # Zed Command : pane: split down
    self_insert_command("C-k", "Down")()

def split_window_right():
    # Zed Command : pane: split right
    self_insert_command("C-k", "Right")()

def other_window():
    # Zed Command : workspace: activate next pane
    zedExecuteCommand("workspace: activate next pane")()

## 矩形選択 / マルチカーソル
def mark_previous_line():
    # Zed Command : editor: add selection above
    self_insert_command("C-A-Up")()

def mark_next_line():
    # Zed Command : editor: add selection below
    self_insert_command("C-A-Down")()

def mark_backward_char():
    mark2(backward_char, False)()

def mark_forward_char():
    mark2(forward_char, True)()

def mark_backward_word():
    mark2(backward_word, False)()

def mark_forward_word():
    mark2(forward_word, True)()

def mark_beginning_of_line():
    mark2(move_beginning_of_line, False)()

def mark_end_of_line():
    mark2(move_end_of_line, True)()

def mark_next_like_this():
    # Zed Command : editor: select next
    region(self_insert_command("C-d"))()

def keyboard_quit_z():
    keyboard_quit(esc=False)

## ターミナル操作
def create_terminal():
    # Zed Command : workspace: new terminal
    zedExecuteCommand("workspace: new terminal")()

def toggle_terminal():
    # Zed Command : terminal panel: toggle
    zedExecuteCommand("terminal panel: toggle")()

## その他
def execute_extended_command():
    # Zed Command : command_palette: toggle
    self_insert_command3("C-S-p")()

def comment_dwim():
    # Zed Command : editor: toggle comments
    self_insert_command("C-k", "C-c")()

## マルチストロークキーの設定
define_key_z("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_z("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_z("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_z("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

run_once = False
def mergeEmacsMultiStrokeKeymap():
    global run_once
    if not run_once:
        mergeMultiStrokeKeymap(keymap_zed, keymap_emacs, "Ctl-x")
        mergeMultiStrokeKeymap(keymap_zed, keymap_emacs, "M-")
        mergeMultiStrokeKeymap(keymap_zed, keymap_emacs, "M-g")
        mergeMultiStrokeKeymap(keymap_zed, keymap_emacs, "M-g M-")
        run_once = True

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_zed キーマップにマージする
keymap_zed.applying_func = mergeEmacsMultiStrokeKeymap

## 「ファイル操作」のキー設定
define_key_z("Ctl-x C-d", reset("sucm", find_directory))
define_key_z("Ctl-x C-r", reset("sucm", recentf))
define_key_z("Ctl-x C-l", reset("sucm", locate))
define_key_z("Ctl-x C-o", reset("sucm", remote))

## 「カーソル移動」のキー設定
define_key_z("C-l",       reset("suc", recenter))

## 「ペイン操作」のキー設定
define_key_z("Ctl-x 0",   reset("sucm", delete_window))
define_key_z("Ctl-x 1",   delete_other_windows)
define_key_z("Ctl-x 2",   split_window_below)
define_key_z("Ctl-x 3",   split_window_right)
define_key_z("Ctl-x o",   reset("sucm", other_window))

## 「矩形選択 / マルチカーソル」のキー設定
define_key_z("C-A-p",     reset("suc",  repeat(mark_previous_line)))
define_key_z("C-A-n",     reset("suc",  repeat(mark_next_line)))
define_key_z("C-A-b",     reset("suc",  repeat(mark_backward_char)))
define_key_z("C-A-f",     reset("suc",  repeat(mark_forward_char)))
define_key_z("C-A-S-b",   reset("suc",  repeat(mark_backward_word)))
define_key_z("C-A-S-f",   reset("suc",  repeat(mark_forward_word)))
define_key_z("C-A-a",     reset("suc",  mark_beginning_of_line))
define_key_z("C-A-e",     reset("suc",  mark_end_of_line))
define_key_z("C-A-d",     reset("suc",  mark_next_like_this))
define_key_z("C-A-g",     reset("scm",  keyboard_quit_z))

## 「ターミナル操作」のキー設定
define_key_z("C-S-(243)", reset("sucm", create_terminal))
define_key_z("C-S-(244)", reset("sucm", create_terminal))
define_key_z("C-(243)",   reset("sucm", toggle_terminal))
define_key_z("C-(244)",   reset("sucm", toggle_terminal))

if is_japanese_keyboard:
    define_key_z("C-S-@", reset("sucm", create_terminal))
    if not fc.use_ctrl_atmark_for_mark:
        define_key_z("C-@", reset("sucm", toggle_terminal))
else:
    define_key_z("C-S-`", reset("sucm", create_terminal))
    define_key_z("C-`",   reset("sucm", toggle_terminal))

## 「その他」のキー設定
define_key_z("M-x",       reset("sucm", execute_extended_command))
define_key_z("M-;",       reset("sucm", comment_dwim))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"zed_key\config_personal.py", msg=False), dict(globals(), **locals()))
