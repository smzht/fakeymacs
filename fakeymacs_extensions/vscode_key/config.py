# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vscode_target
except:
    # VSCode 用のキーバインドを利用するアプリケーションソフトを指定する
    # （ブラウザを指定した場合には、vscode.dev にアクセスして開く VSCode で利用可能となります）
    fc.vscode_target  = ["Code.exe"]
    fc.vscode_target += ["chrome.exe",
                         "msedge.exe",
                         "firefox.exe"
                         ]

# fc.vscode_target に設定しているアプリケーションソフトが fc.not_emacs_target に設定してある場合、
# それを除外する
for target in fc.vscode_target:
    if target in fc.not_emacs_target:
        fc.vscode_target.remove(target)

try:
    # 設定されているか？
    fc.vscode_prefix_key
except:
    # 置き換えするプレフィックスキーの組み合わせ（VSCode のキー、Fakeymacs のキー）を指定する（複数指定可）
    # （置き換えた Fakeymacs のプレフィックスキーを利用することにより、プレフィックスキーの後に入力する
    #   キーが全角文字で入力されることが無くなります）
    # （同じキーを指定することもできます）
    # （Fakeymacs のキーに Meta キー（M-）は指定できません）
    fc.vscode_prefix_key  = []

# プレフィックスキー C-k は デフォルトで C-A-k に置き換えられるものとする
fc.vscode_prefix_key += [["C-k", "C-A-k"]]

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

try:
    # 設定されているか？
    fc.esc_mode_in_keyboard_quit
except:
    # keyboard_quit 関数コール時の Esc キーの発行方法を指定する
    # （1：Esc キーを常に発行する
    #   2：C-g を２回連続して押下した場合に Esc キーを発行する）
    fc.esc_mode_in_keyboard_quit = 1

class FakeymacsVSCode:
    pass

fakeymacs_vscode = FakeymacsVSCode()

fakeymacs_vscode.vscode_focus = "not_terminal"
fakeymacs_vscode.rectangle_mode = False
fakeymacs_vscode.post_processing = None

def is_vscode_target(window):
    if (window.getProcessName() in fc.vscode_target and
        window.getClassName() == "Chrome_WidgetWin_1"):
        return True
    else:
        return False

fakeymacs.is_vscode_target = is_vscode_target

if fc.use_emacs_ime_mode:
    keymap_vscode = keymap.defineWindowKeymap(check_func=lambda wnd: is_vscode_target(wnd) and not is_emacs_ime_mode(wnd))
else:
    keymap_vscode = keymap.defineWindowKeymap(check_func=is_vscode_target)

fakeymacs.keymap_vscode = keymap_vscode

## 共通関数
def self_insert_command_v(*keys):
    func = self_insert_command(*keys)
    def _func():
        ime_status = keymap.getWindow().getImeStatus()
        if ime_status:
            keymap.getWindow().setImeStatus(0)
        func()
        delay()
        if ime_status:
            keymap.getWindow().setImeStatus(1)
    return _func

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

def rect(func):
    def _func():
        func()
        fakeymacs_vscode.rectangle_mode = True
    return _func

def reset_rect(func):
    def _func():
        func()
        fakeymacs_vscode.rectangle_mode = False
    return _func

def region(func):
    def _func():
        func()
        fakeymacs.forward_direction = True
    return _func

def post(func):
    def _func():
        func()
        if fakeymacs_vscode.post_processing:
            fakeymacs_vscode.post_processing()
            fakeymacs_vscode.post_processing = None
    return _func

## ファイル操作
def find_directory():
    # VSCode Command : File: Open Folder...
    self_insert_command("C-k", "C-o")()
    # vscodeExecuteCommand("workbench.action.files.openFolder")()

def recentf():
    # VSCode Command : File: Open Recent...
    self_insert_command("C-r")()
    # vscodeExecuteCommand("workbench.action.openRecent")()

def locate():
    # VSCode Command : Go to File...
    self_insert_command("C-p")()
    # vscodeExecuteCommand("workbench.action.quickOpen")()

## カーソル移動
def previous_error():
    # VSCode Command : Go to Previous Problem in Files (Error, Warning, Info)
    self_insert_command("S-F8")()
    # vscodeExecuteCommand("editor.action.marker.prevInFiles")()

def next_error():
    # VSCode Command : Go to Next Problem in Files (Error, Warning, Info)
    self_insert_command("F8")()
    # vscodeExecuteCommand("editor.action.marker.nextInFiles")()

## カット / コピー
def kill_line_v(repeat=1):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs_vscode.vscode_focus == "terminal"):
        self_insert_command("C-k")()
    else:
        kill_line(repeat)

def yank_v():
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs_vscode.vscode_focus == "terminal"):
        self_insert_command("C-y")()
    else:
        yank()

## バッファ / ウィンドウ操作
def kill_buffer():
    # vscode.dev で動作するように、C-F4 の発行とはしていない（C-F4 がブラウザでキャッチされるため）
    # VSCode Command : View: Close Editor
    vscodeExecuteCommand("workbench.action.closeActiveEditor")()

def switch_to_buffer():
    # VSCode Command : View: Quick Open Privious Recently Used Editor in Group
    vscodeExecuteCommand("VQOPrRUEi")()
    # vscodeExecuteCommand("workbench.action.quickOpenPreviousRecentlyUsedEditorInGroup")()

def list_buffers():
    # VSCode Command : View: Show All Editors By Most Recently Used
    vscodeExecuteCommand("VSAEBM")()
    # vscodeExecuteCommand("workbench.action.showAllEditorsByMostRecentlyUsed")()

## 文字列検索
def isearch_v(direction):
    if (fc.use_direct_input_in_vscode_terminal and
        fakeymacs_vscode.vscode_focus == "terminal"):
        self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
    else:
        isearch(direction)

def isearch_backward():
    isearch_v("backward")

def isearch_forward():
    isearch_v("forward")

## エディタ操作
def delete_group():
    # VSCode Command : View: Close All Editors in Group
    vscodeExecuteCommand("VCAEi")()
    # vscodeExecuteCommand("workbench.action.closeEditorsInGroup")()

def delete_other_groups():
    # VSCode Command : View: Close Editors in Other Groups
    vscodeExecuteCommand("VCEiO")()
    # vscodeExecuteCommand("workbench.action.closeEditorsInOtherGroups")()

def split_editor_below():
    # VSCode Command : View: Split Editor Orthogonal
    self_insert_command("C-k", "C-Yen")()
    # vscodeExecuteCommand("workbench.action.splitEditorOrthogonal")()

def split_editor_right():
    # VSCode Command : View: Split Editor
    self_insert_command("C-Yen")()
    # vscodeExecuteCommand("workbench.action.splitEditor")()

def rotate_layout():
    # VSCode Command : Toggle Vertical/Horizontal Editor Layout
    self_insert_command("A-S-0")()
    # vscodeExecuteCommand("workbench.action.toggleEditorGroupLayout")()

def other_group():
    # VSCode Command : View: Navigate Between Editor Groups
    vscodeExecuteCommand("VNBEdG")()
    # vscodeExecuteCommand("workbench.action.navigateEditorGroups")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs_vscode.vscode_focus = "not_terminal"

def switch_focus(number):
    def _func():
        # VSCode Command : View: Focus Side Bar or n-th Editor Group
        self_insert_command("C-{}".format(number))()

        if fc.use_direct_input_in_vscode_terminal:
            fakeymacs_vscode.vscode_focus = "not_terminal"
    return _func

## 矩形選択 / マルチカーソル
def mark_previous_line():
    # VSCode Command ID : cursorColumnSelectUp
    self_insert_command("C-S-A-Up")()
    # vscodeExecuteCommand("cursorColumnSelectUp")()

def mark_next_line():
    # VSCode Command ID : cursorColumnSelectDown
    self_insert_command("C-S-A-Down")()
    # vscodeExecuteCommand("cursorColumnSelectDown")()

def mark_backward_char():
    if fakeymacs_vscode.rectangle_mode:
        # VSCode Command ID : cursorColumnSelectLeft
        self_insert_command("C-S-A-Left")()
        # vscodeExecuteCommand("cursorColumnSelectLeft")()

        if fakeymacs.forward_direction is None:
            fakeymacs.forward_direction = False
    else:
        mark2(backward_char, False)()

def mark_forward_char():
    if fakeymacs_vscode.rectangle_mode:
        # VSCode Command ID : cursorColumnSelectRight
        self_insert_command("C-S-A-Right")()
        # vscodeExecuteCommand("cursorColumnSelectRight")()

        if fakeymacs.forward_direction is None:
            fakeymacs.forward_direction = True
    else:
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
    # VSCode Command : Add Selection To Next Find Match
    region(self_insert_command("C-d"))()
    # vscodeExecuteCommand("editor.action.addSelectionToNextFindMatch")()

def mark_all_like_this():
    # VSCode Command : Select All Occurrences of Find Match
    region(self_insert_command("C-S-l"))()
    # vscodeExecuteCommand("editor.action.selectHighlights")()

def skip_to_previous_like_this():
    # VSCode Command : Move Last Selection To Previous Find Match
    region(vscodeExecuteCommand("MLSTP"))()
    # vscodeExecuteCommand("editor.action.moveSelectionToPreviousFindMatch")()

def skip_to_next_like_this():
    # VSCode Command : Move Last Selection To Next Find Match
    region(self_insert_command("C-k", "C-d"))()
    # vscodeExecuteCommand("editor.action.moveSelectionToNextFindMatch")()

def expand_region():
    # VSCode Command : Expand Selection
    region(self_insert_command("A-S-Right"))()
    # vscodeExecuteCommand("editor.action.smartSelect.expand")()

def shrink_region():
    # VSCode Command : Shrink Selection
    self_insert_command("A-S-Left")()
    # vscodeExecuteCommand("editor.action.smartSelect.shrink")()

def cursor_undo():
    # VSCode Command : Cursor Undo
    self_insert_command("C-u")()
    # vscodeExecuteCommand("cursorUndo")()

def cursor_redo():
    # VSCode Command : Cursor Redo
    vscodeExecuteCommand("CuRed")()
    # vscodeExecuteCommand("cursorRedo")()

def keyboard_quit_v1():
    keyboard_quit(esc=False)

## ターミナル操作
def create_terminal():
    # VSCode Command : Terminal: Create New Integrated Terminal
    vscodeExecuteCommand2("workbench.action.terminal.new")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs_vscode.vscode_focus = "terminal"

def toggle_terminal():
    if fc.use_direct_input_in_vscode_terminal:
        if fakeymacs_vscode.vscode_focus == "not_terminal":
            # VSCode Command : Terminal: Focus on Terminal View
            vscodeExecuteCommand2("terminal.focus")()

            fakeymacs_vscode.vscode_focus = "terminal"
        else:
            # VSCode Command : View: Close Panel
            vscodeExecuteCommand2("workbench.action.closePanel")()

            fakeymacs_vscode.vscode_focus = "not_terminal"
    else:
        # VSCode Command : View: Toggle Terminal
        vscodeExecuteCommand2("workbench.action.terminal.toggleTerminal")()

## その他
def keyboard_quit_v2():
    if fc.esc_mode_in_keyboard_quit == 1:
        keyboard_quit(esc=True)
        fakeymacs_vscode.post_processing = None
    else:
        if fakeymacs.last_keys in [[keymap_vscode, "C-g"],
                                   [keymap_vscode, "C-A-g"]]:
            keyboard_quit(esc=True)
            fakeymacs_vscode.post_processing = None
        else:
            keyboard_quit(esc=False)

def execute_extended_command():
    # VSCode Command : Show All Commands
    self_insert_command3("f1")()
    # vscodeExecuteCommand("workbench.action.showCommands")()

def comment_dwim():
    # VSCode Command : Toggle Line Comment
    self_insert_command("C-Slash")()
    # vscodeExecuteCommand("editor.action.commentLine")()

    resetRegion()

def trigger_suggest():
    # VSCode Command : Trigger Suggest
    self_insert_command("C-Space")()
    # vscodeExecuteCommand("editor.action.triggerSuggest")()

## マルチストロークキーの設定
define_key(keymap_vscode, "Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key(keymap_vscode, "M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key(keymap_vscode, "M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key(keymap_vscode, "M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

def mergeEmacsMultiStrokeKeymap():
    mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "Ctl-x")
    mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-")
    mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-g")
    mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-g M-")
    keymap_vscode.applying_func = None

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_vscode キーマップにマージする
keymap_vscode.applying_func = mergeEmacsMultiStrokeKeymap

## プレフィックスキーの設定
for pkey1, pkey2 in fc.vscode_prefix_key:
    define_key(keymap_vscode, pkey2, keymap.defineMultiStrokeKeymap("<VSCode> " + pkey1))

    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1 in ["", "A-"]:
            for mod2 in ["", "C-"]:
                for mod3 in ["", "S-"]:
                    mkey = mod1 + mod2 + mod3 + key
                    define_key(keymap_vscode, "{} {}".format(pkey2, mkey), self_insert_command_v(pkey1, mkey))

## 「ファイル操作」のキー設定
define_key(keymap_vscode, "Ctl-x C-d", reset_search(reset_undo(reset_counter(reset_mark(find_directory)))))
define_key(keymap_vscode, "Ctl-x C-r", reset_search(reset_undo(reset_counter(reset_mark(recentf)))))
define_key(keymap_vscode, "Ctl-x C-l", reset_search(reset_undo(reset_counter(reset_mark(locate)))))

## 「カーソル移動」のキー設定
define_key(keymap_vscode, "M-g p",   reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key(keymap_vscode, "M-g M-p", reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key(keymap_vscode, "M-g n",   reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
define_key(keymap_vscode, "M-g M-n", reset_search(reset_undo(reset_counter(reset_mark(next_error)))))

if is_japanese_keyboard:
    define_key(keymap_vscode, "Ctl-x S-Atmark",  reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
else:
    define_key(keymap_vscode, "Ctl-x BackQuote", reset_search(reset_undo(reset_counter(reset_mark(next_error)))))

define_key(keymap_vscode, "A-p", self_insert_command("C-Up"))
define_key(keymap_vscode, "A-n", self_insert_command("C-Down"))

## 「カット / コピー」のキー設定
define_key(keymap_vscode, "C-k", reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_line_v))))))
define_key(keymap_vscode, "C-y", reset_search(reset_undo(reset_counter(reset_mark(repeat(yank_v))))))

## 「バッファ / ウィンドウ操作」のキー設定
define_key(keymap_vscode, "Ctl-x k",   reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key(keymap_vscode, "Ctl-x b",   reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
define_key(keymap_vscode, "Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))

## 「文字列検索」のキー設定
define_key(keymap_vscode, "C-r", reset_undo(reset_counter(reset_mark(isearch_backward))))
define_key(keymap_vscode, "C-s", reset_undo(reset_counter(reset_mark(isearch_forward))))

## 「エディタ操作」のキー設定
define_key(keymap_vscode, "Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_group)))))
define_key(keymap_vscode, "Ctl-x 1", reset_search(reset_undo(reset_counter(reset_mark(delete_other_groups)))))
define_key(keymap_vscode, "Ctl-x 2", split_editor_below)
define_key(keymap_vscode, "Ctl-x 3", split_editor_right)
define_key(keymap_vscode, "Ctl-x 4", rotate_layout)
define_key(keymap_vscode, "Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_group)))))

if fc.use_ctrl_digit_key_for_digit_argument:
    key = "C-A-{}"
else:
    key = "C-{}"

for n in range(10):
    define_key(keymap_vscode, key.format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))

## 「矩形選択 / マルチカーソル」のキー設定
define_key(keymap_vscode, "C-A-p",   reset_search(reset_undo(reset_counter(rect(repeat(mark_previous_line))))))
define_key(keymap_vscode, "C-A-n",   reset_search(reset_undo(reset_counter(rect(repeat(mark_next_line))))))
define_key(keymap_vscode, "C-A-b",   reset_search(reset_undo(reset_counter(repeat(mark_backward_char)))))
define_key(keymap_vscode, "C-A-f",   reset_search(reset_undo(reset_counter(repeat(mark_forward_char)))))
define_key(keymap_vscode, "C-A-S-b", reset_search(reset_undo(reset_counter(reset_rect(repeat(mark_backward_word))))))
define_key(keymap_vscode, "C-A-S-f", reset_search(reset_undo(reset_counter(reset_rect(repeat(mark_forward_word))))))
define_key(keymap_vscode, "C-A-a",   reset_search(reset_undo(reset_counter(reset_rect(mark_beginning_of_line)))))
define_key(keymap_vscode, "C-A-e",   reset_search(reset_undo(reset_counter(reset_rect(mark_end_of_line)))))
define_key(keymap_vscode, "C-A-d",   reset_search(reset_undo(reset_counter(reset_rect(mark_next_like_this)))))
define_key(keymap_vscode, "C-A-S-d", reset_search(reset_undo(reset_counter(reset_rect(mark_all_like_this)))))
define_key(keymap_vscode, "C-A-s",   reset_search(reset_undo(reset_counter(reset_rect(skip_to_next_like_this)))))
define_key(keymap_vscode, "C-A-S-s", reset_search(reset_undo(reset_counter(reset_rect(skip_to_previous_like_this)))))
define_key(keymap_vscode, "C-A-x",   reset_search(reset_undo(reset_counter(reset_rect(expand_region)))))
define_key(keymap_vscode, "C-A-S-x", reset_search(reset_undo(reset_counter(reset_rect(shrink_region)))))
define_key(keymap_vscode, "C-A-u",   reset_search(reset_undo(reset_counter(reset_rect(cursor_undo)))))
define_key(keymap_vscode, "C-A-r",   reset_search(reset_undo(reset_counter(reset_rect(cursor_redo)))))
define_key(keymap_vscode, "C-A-g",   reset_search(reset_counter(reset_mark(keyboard_quit_v1))))

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
define_key(keymap_vscode, "Enter",       post(reset_undo(reset_counter(reset_mark(repeat(newline))))))
define_key(keymap_vscode, "C-m",         post(reset_undo(reset_counter(reset_mark(repeat(newline))))))
define_key(keymap_vscode, "C-g",         reset_search(reset_counter(reset_mark(keyboard_quit_v2))))
define_key(keymap_vscode, "M-x",         reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key(keymap_vscode, "M-Semicolon", reset_search(reset_undo(reset_counter(reset_mark(comment_dwim)))))

if is_japanese_keyboard:
    define_key(keymap_vscode, "C-Colon", trigger_suggest)
else:
    define_key(keymap_vscode, "C-Quote", trigger_suggest)

## vscode_extensions 拡張機能の読み込み
exec(readConfigExtension(r"vscode_extensions\config.py"), dict(globals(), **locals()))

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"vscode_key\config_personal.py", msg=False), dict(globals(), **locals()))
