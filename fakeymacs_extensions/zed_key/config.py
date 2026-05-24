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

try:
    # 設定されているか？
    fc.zed_prefix_key
except:
    # 置き換えするプレフィックスキーの組み合わせ（置き換え元のキー、置き換え先のキー）を指定する（複数指定可）
    # （プレフィッスクキーの後に入力するキーが、Fakeymacs で置き換えられないようにする対策です）
    # （同じキーを指定することもできます）
    # （置き換え先のキーに Meta キー（M-）は指定できません）
    fc.zed_prefix_key = [["C-k", "C-A-k"],
                         ]

try:
    # 設定されているか？
    fc.zed_replace_key
except:
    # 置き換えするキーの組み合わせ（置き換え元のキー、置き換え先のキー）を指定する（複数指定可）
    # （同じキーを指定することもできます）
    # （置き換え先のキーに Meta キー（M-）は指定できません）
    fc.zed_replace_key = []

try:
    # 設定されているか？
    fc.zed_use_ctrl_atmark_for_mark
except:
    # 日本語キーボードを利用する際、Zed で  C-@ をマーク用のキーとして使うかどうかを指定する
    # （True: 使う、False: 使わない）
    # （Zed で C-@ を Toggle Terminal 用のキーとして使えるようにするために設けた設定です。
    #   True に設定した場合でも、Toggle Terminal 用のキーとして  C-<半角／全角> が使えます。）
    fc.zed_use_ctrl_atmark_for_mark = False

try:
    # 設定されているか？
    fc.zed_use_direct_input_in_terminal
except:
    # パネルのターミナル内で４つのキー（C-k、C-r、C-s、C-y）のダイレクト入力機能を使うかどうかを
    # 指定する（True: 使う、False: 使わない）
    fc.zed_use_direct_input_in_terminal = False

try:
    # 設定されているか？
    fc.zed_esc_mode_in_keyboard_quit
except:
    # keyboard_quit 関数実行時（C-g 押下時）の Esc キーの発行方法を指定する
    # （1：C-g を押下した際、常に Esc キーを発行する
    #   2：C-g を２回連続して押下した場合に Esc キーを発行する）
    fc.zed_esc_mode_in_keyboard_quit = 1

# --------------------------------------------------------------------------------------------------

class FakeymacsZed:
    pass

fakeymacs_zed = FakeymacsZed()

fakeymacs_zed.terminal_focus = False

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
def define_key_z(keys, command, skip_check=True):
    if skip_check:
        # 設定をスキップするキーの処理を行う
        if "keymap_zed" in fc.skip_mapping_key:
            for skey in fc.skip_mapping_key["keymap_zed"]:
                if fnmatch.fnmatch(keys, skey):
                    print(f"skip key mapping : [keymap_zed] {keys}")
                    return

    define_key(keymap_zed, keys, command, False)

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

## カット / コピー
def kill_line_z(repeat=1):
    if fakeymacs_zed.terminal_focus:
        self_insert_command("C-k", "C-k")()
    else:
        kill_line(repeat)

def yank_z():
    if fakeymacs_zed.terminal_focus:
        self_insert_command("C-y")()
    else:
        yank()

## パネル操作
def close_panel():
    # Zed Command : workspace: close active dock
    zedExecuteCommand("workspace: close active dock")()

## ペイン操作
def delete_window():
    # Zed Command : pane: close all items
    self_insert_command4("C-k", "w")()

    if fakeymacs_vscode.terminal_focus:
        fakeymacs_vscode.terminal_focus = False

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
    if fakeymacs_zed.terminal_focus:
        # Zed Command : terminal panel: toggle focus
        zedExecuteCommand("terminal panel: toggle focus")()

        if fc.zed_use_direct_input_in_terminal:
            fakeymacs_zed.terminal_focus = False
    else:
        # Zed Command : workspace: activate next pane
        zedExecuteCommand("workspace: activate next pane")()

## 文字列検索
def isearch_v(direction):
    if fakeymacs_zed.terminal_focus:
        self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
    else:
        isearch(direction)

def isearch_backward():
    isearch_v("backward")

def isearch_forward():
    isearch_v("forward")

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
    region(self_insert_command("C-F3"))()

def mark_all_like_this():
    # Zed Command : editor: select all matches
    region(self_insert_command("C-F2"))()

def expand_region():
    # Zed Command : editor: select larger syntax node
    region(self_insert_command("A-S-Right"))()

def shrink_region():
    # Zed Command : editor: select smaller syntax node
    self_insert_command("A-S-Left")()

def cursor_undo():
    # VSCode Command : editor: undo selection
    self_insert_command("C-u")()

def cursor_redo():
    # VSCode Command : editor: redo selection
    self_insert_command("C-S-u")()

def keyboard_quit_z1():
    keyboard_quit(esc=False)

## ターミナル操作
def create_terminal():
    # Zed Command : workspace: new terminal
    zedExecuteCommand("workspace: new terminal")()

    if fc.zed_use_direct_input_in_terminal:
        fakeymacs_zed.terminal_focus = True

def toggle_terminal():
    if fc.zed_use_direct_input_in_terminal:
        if fakeymacs_zed.terminal_focus:
            close_panel()
            fakeymacs_zed.terminal_focus = False
        else:
            # Zed Command : terminal panel: toggle
            zedExecuteCommand("terminal panel: toggle")()
            fakeymacs_zed.terminal_focus = True
    else:
        # Zed Command : terminal panel: toggle
        zedExecuteCommand("terminal panel: toggle")()

## その他
def keyboard_quit_z2():
    if fc.zed_esc_mode_in_keyboard_quit == 1:
        keyboard_quit(esc=True)
    else:
        if (fakeymacs.last_keys[0] is keymap_zed and
            fakeymacs.last_keys[1] in ["C-g", "C-A-g"]):
            keyboard_quit(esc=True)
        else:
            keyboard_quit(esc=False)

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

## 「カット / コピー」のキー設定
define_key_z("C-k",       reset("sucm", repeat3(kill_line_z)))
define_key_z("C-y",       reset("sucm", repeat(yank_z)))

## 「ペイン操作」のキー設定
define_key_z("Ctl-x 0",   reset("sucm", delete_window))
define_key_z("Ctl-x 1",   delete_other_windows)
define_key_z("Ctl-x 2",   split_window_below)
define_key_z("Ctl-x 3",   split_window_right)
define_key_z("Ctl-x o",   reset("sucm", other_window))

## 「文字列検索」のキー設定
define_key_z("C-r",       reset("ucm", isearch_backward))
define_key_z("C-s",       reset("ucm", isearch_forward))

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
define_key_z("C-A-S-d",   reset("suc",  mark_all_like_this))
define_key_z("C-A-x",     reset("suc",  expand_region))
define_key_z("C-A-S-x",   reset("suc",  shrink_region))
define_key_z("C-A-u",     reset("suc",  cursor_undo))
define_key_z("C-A-r",     reset("suc",  cursor_redo))
define_key_z("C-A-g",     reset("scm",  keyboard_quit_z1))

## 「ターミナル操作」のキー設定
define_key_z("C-S-(243)", reset("sucm", create_terminal))
define_key_z("C-S-(244)", reset("sucm", create_terminal))
define_key_z("C-(243)",   reset("sucm", toggle_terminal))
define_key_z("C-(244)",   reset("sucm", toggle_terminal))

if is_japanese_keyboard:
    define_key_z("C-S-@", reset("sucm", create_terminal))

    if not fc.zed_use_ctrl_atmark_for_mark:
        define_key_z("C-@", reset("sucm", toggle_terminal))
else:
    define_key_z("C-S-`", reset("sucm", create_terminal))
    define_key_z("C-`",   reset("sucm", toggle_terminal))

## 「その他」のキー設定
define_key_z("C-g",       reset("scm",  keyboard_quit_z2))
define_key_z("M-x",       reset("sucm", execute_extended_command))
define_key_z("M-;",       reset("sucm", comment_dwim))

# --------------------------------------------------------------------------------------------------

## プレフィックスキーの置き換え設定
for pkey1, pkey2 in fc.zed_prefix_key:
    define_key_z(pkey2, keymap.defineMultiStrokeKeymap(f"<Zed> {pkey1}"))

    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
            mkey = mod1 + mod2 + mod3 + mod4 + key
            define_key_z(f"{pkey2} {mkey}", self_insert_command4(pkey1, mkey))

## キーの置き換え設定
for key1, key2 in fc.zed_replace_key:
    define_key_z(key2, self_insert_command(key1))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"zed_key\config_personal.py", msg=False), dict(globals(), **locals()))
