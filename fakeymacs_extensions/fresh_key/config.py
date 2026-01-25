####################################################################################################
## Fresh Editor 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.fresh_language
except:
    # Fresh に設定している表示言語を指定する（US: English、JP: 日本語）
    # fc.fresh_language = "US"
    fc.fresh_language = "JP"

try:
    # 設定されているか？
    fc.fresh_target
except:
    # Fresh Editor 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.fresh_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - fresh*"],
                       ]
try:
    # 設定されているか？
    fc.fresh_command_dict
except:
    # Fresh の Command pallet で利用するコマンドを指定する
    # （key: フルスペル英語コマンド、value[0]: 短縮英語コマンド、value[1]: 短縮日本語コマンド）
    fc.fresh_command_dict = {"Close Buffer"         : ["clbu",   "バ閉"],
                             "Close Split"          : ["clspl",  "分閉"],
                             "Split Horizontal"     : ["spho",   "水平"],
                             "Split Vertical"       : ["spvert", "垂直"],
                             "Record Macro"         : ["recmac", "マを記録"],
                             "Play Macro"           : ["plmac",  "マ再生"]
                             }

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.fresh_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
fresh_target1 = re.compile(regex)
fresh_target2 = [app for app in fc.fresh_target if type(app) is list]

def is_fresh(window):
    global fresh_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == True and
            (fresh_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in fresh_target2))):
            fresh_status = True
        else:
            fresh_status = False

    return fresh_status

if fc.use_emacs_ime_mode:
    keymap_fresh = keymap.defineWindowKeymap(check_func=lambda wnd: (is_fresh(wnd) and
                                                                     not is_emacs_ime_mode(wnd)))
else:
    keymap_fresh = keymap.defineWindowKeymap(check_func=is_fresh_target)

## 共通関数
def define_key_f(keys, command):
    define_key(keymap_fresh, keys, command)

def freshExecuteCommand(command, enter=True):
    if fc.fresh_language == "JP":
        command = fc.fresh_command_dict[command][1]
    else:
        command = fc.fresh_command_dict[command][0]

    def _func():
        self_insert_command("C-p")()
        princ(command)

        if enter:
            self_insert_command("Enter")()
    return _func

def freshExecuteCommand2(command, enter=True):
    def _func():
        setImeStatus(0)
        freshExecuteCommand(command, enter)()
    return _func

def region(func):
    def _func():
        func()
        fakeymacs.forward_direction = True
    return _func

## バッファ操作
def kill_buffer():
    freshExecuteCommand("Close Buffer")()

def switch_to_buffer():
    self_insert_command("C-PageDown")()

## ペイン操作
def delete_window():
    freshExecuteCommand("Close Split")()

def delete_other_windows():
    other_window()
    delete_window()

def split_window_below():
    freshExecuteCommand("Split Horizontal")()

def split_window_right():
    freshExecuteCommand("Split Vertical")()

def other_window():
    self_insert_command("A-]")()

## 矩形選択 / マルチカーソル
def mark_previous_line():
    self_insert_command("C-A-Up")()

def mark_next_line():
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
    region(self_insert_command("C-d"))()

def keyboard_quit_f():
    keyboard_quit(esc=False)

## キーボードマクロ
def keyboard_macro_start():
    if fc.fresh_language == "JP":
        freshExecuteCommand2("Record Macro", enter=True)()
    else:
        freshExecuteCommand2("Record Macro", enter=False)()

def keyboard_macro_stop():
    self_insert_command("F5")()

def keyboard_macro_play():
    freshExecuteCommand2("Play Macro", enter=False)()

## その他
def execute_extended_command():
    self_insert_command3("C-p")()

def comment_dwim():
    self_insert_command("C-/")()

## マルチストロークキーの設定
define_key_f("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_f("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_f("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_f("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

run_once = False
def mergeEmacsMultiStrokeKeymap():
    global run_once
    if not run_once:
        mergeMultiStrokeKeymap(keymap_fresh, keymap_emacs, "Ctl-x")
        mergeMultiStrokeKeymap(keymap_fresh, keymap_emacs, "M-")
        mergeMultiStrokeKeymap(keymap_fresh, keymap_emacs, "M-g")
        mergeMultiStrokeKeymap(keymap_fresh, keymap_emacs, "M-g M-")
        run_once = True

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_fresh キーマップにマージする
keymap_fresh.applying_func = mergeEmacsMultiStrokeKeymap

## 「バッファ」のキー設定
define_key_f("M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_f("Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_f("Ctl-x b", reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))

## 「ペイン」のキー設定
define_key_f("Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_window)))))
define_key_f("Ctl-x 1", reset_search(reset_undo(reset_counter(reset_mark(delete_other_windows)))))
define_key_f("Ctl-x 2", reset_search(reset_undo(reset_counter(reset_mark(split_window_below)))))
define_key_f("Ctl-x 3", reset_search(reset_undo(reset_counter(reset_mark(split_window_right)))))
define_key_f("Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

## 「矩形選択 / マルチカーソル」のキー設定
define_key_f("C-A-p",   reset_search(reset_undo(reset_counter(repeat(mark_previous_line)))))
define_key_f("C-A-n",   reset_search(reset_undo(reset_counter(repeat(mark_next_line)))))
define_key_f("C-A-b",   reset_search(reset_undo(reset_counter(repeat(mark_backward_char)))))
define_key_f("C-A-f",   reset_search(reset_undo(reset_counter(repeat(mark_forward_char)))))
define_key_f("C-A-S-b", reset_search(reset_undo(reset_counter(repeat(mark_backward_word)))))
define_key_f("C-A-S-f", reset_search(reset_undo(reset_counter(repeat(mark_forward_word)))))
define_key_f("C-A-a",   reset_search(reset_undo(reset_counter(mark_beginning_of_line))))
define_key_f("C-A-e",   reset_search(reset_undo(reset_counter(mark_end_of_line))))
define_key_f("C-A-d",   reset_search(reset_undo(reset_counter(mark_next_like_this))))
define_key_f("C-A-g",   reset_search(reset_counter(reset_mark(keyboard_quit_f))))

## 「キーボードマクロ」のキー設定
define_key_f("Ctl-x (", keyboard_macro_start)
define_key_f("Ctl-x )", keyboard_macro_stop)
define_key_f("Ctl-x e", reset_search(reset_undo(reset_counter(repeat(keyboard_macro_play)))))

## 「その他」のキー設定
define_key_f("M-x", reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key_f("M-;", reset_search(reset_undo(reset_counter(reset_mark(comment_dwim)))))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"fresh_key\config_personal.py", msg=False), dict(globals(), **locals()))
