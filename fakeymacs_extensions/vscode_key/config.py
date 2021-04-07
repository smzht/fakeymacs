# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vscode_target
except:
    # VSCode 用のキーバインドを利用するアプリケーションソフトを指定する
    # （ブラウザを指定した場合には、github1s.com にアクセスして開く VSCode で利用可能となります）
    fc.vscode_target  = ["Code.exe"]
    fc.vscode_target += ["chrome.exe",
                         "msedge.exe",
                         "firefox.exe"
                        ]

try:
    # 設定されているか？
    fc.use_ctrl_atmark_for_mark
except:
    # 日本語キーボードを利用する際、VSCode で  C-@ をマーク用のキーとして使うかどうかを指定する
    # （True: 使う、False: 使わない）
    # （VSCode で C-@ を Toggle Integrated Terminal 用のキーとして使えるようにするために設けた設定です。
    #   True に設定した場合でも、Toggle Integrated Terminal 用のキーとして  C-<半角／全角> が使えます。）
    fc.use_ctrl_atmark_for_mark = False

try:
    # 設定されているか？
    fc.use_direct_input_in_vscode_terminal
except:
    # VSCode の Terminal内 で ４つのキー（Ctrl+k、Ctrl+r、Ctrl+s、Ctrl+y）のダイレクト入力機能を使うか
    # どうかを指定する（True: 使う、False: 使わない）
    fc.use_direct_input_in_vscode_terminal = False

fakeymacs.vscode_focus = "not_terminal"

def is_vscode_target(window):
    if window.getProcessName() in fc.vscode_target:
        return True
    else:
        return False

keymap_vscode = keymap.defineWindowKeymap(check_func=is_vscode_target)

## 共通関数
def define_key3(window_keymap, keys, command):
    define_key(window_keymap, keys,
               makeKeyCommand(window_keymap, keys, command, lambda: is_vscode_target(keymap.getWindow())))

def vscodeExecuteCommand(command):
    def _func():
        self_insert_command("f1")()
        princ(command)
        self_insert_command("Enter")()
    return _func

def vscodeExecuteCommand2(command):
    def _func():
        keymap.getWindow().setImeStatus(0)
        vscodeExecuteCommand(command)()
    return _func

## カット / コピー
def kill_line2(repeat=1):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command("C-k")()
    else:
        kill_line(repeat)

def yank2():
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command("C-y")()
    else:
        yank()

## バッファ / ウィンドウ操作
def kill_buffer():
    # VSCode Command : Close Editor
    vscodeExecuteCommand("workbench.action.closeActiveEditor")()

def switch_to_buffer():
    # VSCode Command : Quick Open Privious Recently Used Editor in Group
    vscodeExecuteCommand("workbench.action.quickOpenPreviousRecentlyUsedEditorInGroup")()

def list_buffers():
    # VSCode Command : Show All Editors By Most Recently Used
    vscodeExecuteCommand("workbench.action.showAllEditorsByMostRecentlyUsed")()

## 文字列検索
def isearch2(direction):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs.vscode_focus == "terminal"):
        self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
    else:
        isearch(direction)

def isearch_backward():
    isearch2("backward")

def isearch_forward():
    isearch2("forward")

## エディタ操作
def delete_group():
    # VSCode Command : Close All Editors in Group
    vscodeExecuteCommand("workbench.action.closeEditorsInGroup")()

def delete_other_groups():
    # VSCode Command : Close Editors in Other Groups
    vscodeExecuteCommand("workbench.action.closeEditorsInOtherGroups")()

def split_editor_below():
    # VSCode Command : Split Editor Orthogonal
    self_insert_command("C-k", "C-Yen")()

def split_editor_right():
    # VSCode Command : Split Editor
    self_insert_command("C-Yen")()

def other_group():
    # VSCode Command : Navigate Between Editor Groups
    vscodeExecuteCommand("workbench.action.navigateEditorGroups")()
    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs.vscode_focus = "not_terminal"

def switch_focus(number):
    def _func():
        # VSCode Command : Focus n-th Editor Group
        self_insert_command("C-{}".format(number))()
        if fc.use_direct_input_in_vscode_terminal:
            fakeymacs.vscode_focus = "not_terminal"
    return _func

## マルチカーソル
def mark_up():
    # VSCode Command : cursorColumnSelectUp
    self_insert_command("C-S-A-Up")()

def mark_down():
    # VSCode Command : cursorColumnSelectDown
    self_insert_command("C-S-A-Down")()

def mark_next_like_this():
    # VSCode Command : Add Selection To Next Find Match
    self_insert_command("C-d")()

def skip_to_next_like_this():
    # VSCode Command : Move Last Selection To Next Find Match
    self_insert_command("C-k", "C-d")()

## ターミナル操作
def create_terminal():
    # VSCode Command : Create New Integrated Terminal
    vscodeExecuteCommand2("workbench.action.terminal.new")()
    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs.vscode_focus = "terminal"

def toggle_terminal():
    if fc.use_direct_input_in_vscode_terminal:
        if fakeymacs.vscode_focus == "not_terminal":
            # VSCode Command : Focus on Terminal View
            vscodeExecuteCommand2("terminal.focus")()
            fakeymacs.vscode_focus = "terminal"
        else:
            # VSCode Command : Close Panel
            vscodeExecuteCommand2("workbench.action.closePanel")()
            fakeymacs.vscode_focus = "not_terminal"
    else:
        # VSCode Command : Toggle Integrated Terminal
        vscodeExecuteCommand2("workbench.action.terminal.toggleTerminal")()

## その他
def execute_extended_command():
    # VSCode Command : Show All Commands
    self_insert_command3("f1")()

def comment_dwim():
    # VSCode Command : Toggle Line Comment
    self_insert_command("C-Slash")()

## 「カット / コピー」のキー設定
define_key3(keymap_emacs, "C-k", reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_line2))))))
define_key3(keymap_emacs, "C-y", reset_search(reset_undo(reset_counter(reset_mark(repeat(yank2))))))

## 「バッファ / ウィンドウ操作」のキー設定
define_key3(keymap_emacs, "Ctl-x k",   reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key3(keymap_emacs, "Ctl-x b",   reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
define_key3(keymap_emacs, "Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))

## 「文字列検索」のキー設定
define_key3(keymap_emacs, "C-r", reset_undo(reset_counter(reset_mark(isearch_backward))))
define_key3(keymap_emacs, "C-s", reset_undo(reset_counter(reset_mark(isearch_forward))))

## 「エディタ操作」のキー設定
define_key3(keymap_emacs, "Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_group)))))
define_key3(keymap_emacs, "Ctl-x 1", reset_search(reset_undo(reset_counter(reset_mark(delete_other_groups)))))
define_key3(keymap_emacs, "Ctl-x 2", reset_search(reset_undo(reset_counter(reset_mark(split_editor_below)))))
define_key3(keymap_emacs, "Ctl-x 3", reset_search(reset_undo(reset_counter(reset_mark(split_editor_right)))))
define_key3(keymap_emacs, "Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_group)))))

for n in range(10):
    define_key(keymap_vscode, "C-A-{}".format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))
    if not fc.use_ctrl_digit_key_for_digit_argument:
        define_key(keymap_vscode, "C-{}".format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))

## 「マルチカーソル」のキー設定
define_key(keymap_vscode, "C-A-p", reset_search(reset_undo(reset_counter(mark_up))))
define_key(keymap_vscode, "C-A-n", reset_search(reset_undo(reset_counter(mark_down))))
define_key(keymap_vscode, "C-A-b", reset_search(reset_undo(reset_counter(mark2(repeat(backward_char), False)))))
define_key(keymap_vscode, "C-A-f", reset_search(reset_undo(reset_counter(mark2(repeat(forward_char), True)))))
define_key(keymap_vscode, "C-A-a", reset_search(reset_undo(reset_counter(mark2(move_beginning_of_line, False)))))
define_key(keymap_vscode, "C-A-e", reset_search(reset_undo(reset_counter(mark2(move_end_of_line, True)))))
define_key(keymap_vscode, "C-A-d", reset_search(reset_undo(reset_counter(mark_next_like_this))))
define_key(keymap_vscode, "C-A-s", reset_search(reset_undo(reset_counter(skip_to_next_like_this))))

## 「ターミナル操作」のキー設定
define_key(keymap_vscode, "C-S-(243)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key(keymap_vscode, "C-S-(244)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key(keymap_vscode, "C-(243)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
define_key(keymap_vscode, "C-(244)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))

if is_japanese_keyboard:
    define_key(keymap_vscode, "C-S-Atmark", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    if not fc.use_ctrl_atmark_for_mark:
        define_key(keymap_vscode, "C-Atmark", reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
else:
    define_key(keymap_vscode, "C-S-BackQuote", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    define_key(keymap_vscode, "C-BackQuote",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))

## 「その他」のキー設定
define_key3(keymap_emacs, "M-x",         reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key3(keymap_emacs, "M-Semicolon", reset_search(reset_undo(reset_counter(comment_dwim))))
