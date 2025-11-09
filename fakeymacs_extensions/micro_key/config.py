####################################################################################################
## Micro Editor 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.micro_target
except:
    # Micro Editor 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.micro_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - micro*"],
                       [None, "ConsoleWindowClass", "* - micro*"],
                       ]

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.micro_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
micro_target1 = re.compile(regex)
micro_target2 = [app for app in fc.micro_target if type(app) is list]

def is_micro(window):
    global micro_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == True and
            (micro_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in micro_target2))):
            micro_status = True
        else:
            micro_status = False

    return micro_status

if fc.use_emacs_ime_mode:
    keymap_micro = keymap.defineWindowKeymap(check_func=lambda wnd: (is_micro(wnd) and
                                                                     not is_emacs_ime_mode(wnd)))
else:
    keymap_micro = keymap.defineWindowKeymap(check_func=is_micro_target)

## 共通関数
def define_key_u(keys, command):
    define_key(keymap_micro, keys, command)

def microExecuteCommand(command, enter=True):
    def _func():
        self_insert_command("C-e")()
        princ(command)

        if enter:
            self_insert_command("Enter")()
    return _func

def microExecuteCommand2(command, enter=True):
    def _func():
        setImeStatus(0)
        microExecuteCommand(command, enter)()
    return _func

def region(func):
    def _func():
        func()
        fakeymacs.forward_direction = True
    return _func

## ペイン操作
def kill_buffer():
    self_insert_command("C-q")()

def delete_window():
    self_insert_command("C-q")()

def split_window_below():
    microExecuteCommand("hsplit")()

def split_window_right():
    microExecuteCommand("vsplit")()

def other_window():
    self_insert_command("C-w")()

## 矩形選択 / マルチカーソル
def mark_previous_line():
    self_insert_command("A-S-Up")()

def mark_next_line():
    self_insert_command("A-S-Down")()

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
    region(self_insert_command("A-n"))()

def keyboard_quit_u1():
    keyboard_quit(esc=False)

## キーボードマクロ
def keyboard_macro_start():
    self_insert_command("C-u")()

def keyboard_macro_stop():
    self_insert_command("C-u")()

def keyboard_macro_play():
    self_insert_command("C-j")()

## その他
def execute_extended_command():
    self_insert_command3("C-e")()

def comment_dwim():
    self_insert_command("A-/")()

## マルチストロークキーの設定
define_key_u("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_u("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_u("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_u("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

run_once = False
def mergeEmacsMultiStrokeKeymap():
    global run_once
    if not run_once:
        mergeMultiStrokeKeymap(keymap_micro, keymap_emacs, "Ctl-x")
        mergeMultiStrokeKeymap(keymap_micro, keymap_emacs, "M-")
        mergeMultiStrokeKeymap(keymap_micro, keymap_emacs, "M-g")
        mergeMultiStrokeKeymap(keymap_micro, keymap_emacs, "M-g M-")
        run_once = True

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_micro キーマップにマージする
keymap_micro.applying_func = mergeEmacsMultiStrokeKeymap

## 「ペイン操作」のキー設定
define_key_u("M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_u("Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_u("Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_window)))))
define_key_u("Ctl-x 2", reset_search(reset_undo(reset_counter(reset_mark(split_window_below)))))
define_key_u("Ctl-x 3", reset_search(reset_undo(reset_counter(reset_mark(split_window_right)))))
define_key_u("Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

## 「矩形選択 / マルチカーソル」のキー設定
define_key_u("C-A-p",   reset_search(reset_undo(reset_counter(repeat(mark_previous_line)))))
define_key_u("C-A-n",   reset_search(reset_undo(reset_counter(repeat(mark_next_line)))))
define_key_u("C-A-b",   reset_search(reset_undo(reset_counter(repeat(mark_backward_char)))))
define_key_u("C-A-f",   reset_search(reset_undo(reset_counter(repeat(mark_forward_char)))))
define_key_u("C-A-S-b", reset_search(reset_undo(reset_counter(repeat(mark_backward_word)))))
define_key_u("C-A-S-f", reset_search(reset_undo(reset_counter(repeat(mark_forward_word)))))
define_key_u("C-A-a",   reset_search(reset_undo(reset_counter(mark_beginning_of_line))))
define_key_u("C-A-e",   reset_search(reset_undo(reset_counter(mark_end_of_line))))
define_key_u("C-A-d",   reset_search(reset_undo(reset_counter(mark_next_like_this))))
define_key_u("C-A-g",   reset_search(reset_counter(reset_mark(keyboard_quit_u1))))

## 「キーボードマクロ」のキー設定
define_key_u("Ctl-x (", keyboard_macro_start)
define_key_u("Ctl-x )", keyboard_macro_stop)
define_key_u("Ctl-x e", reset_search(reset_undo(reset_counter(repeat(keyboard_macro_play)))))

## 「その他」のキー設定
define_key_u("M-x", reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key_u("M-;", reset_search(reset_undo(reset_counter(reset_mark(comment_dwim)))))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"micro_key\config_personal.py", msg=False), dict(globals(), **locals()))
