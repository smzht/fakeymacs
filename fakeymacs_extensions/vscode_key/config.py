# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vscode_browser_title
except:
    # VS Code Web の画面で VSCode 用のキーバインドを利用するブラウザタブのタイトルを指定する
    fc.vscode_browser_title = ["* - Visual Studio Code*",
                               "Codespaces - *",
                               "Firebase Studio - *",
                               ]

# VSCode 用のキーバインドを利用するアプリケーションソフト、置き換えするプレフィックスキーの組み合わせ、
# 置き換えするキーの組み合わせを指定する（fc.vscode_setting1 ～ fc.vscode_setting10 まで 10個設定可）
#
# 辞書型で、次の３つのデータを指定する
#
# １）"target"     : VSCode 用のキーバインドを利用するアプリケーションソフトを指定する
#   （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
#     クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
#     リストの後ろの項目から省略可）を指定してください）
#
# ２）"prefix_key" : 置き換えするプレフィックスキーの組み合わせ（置き換え元のキー、置き換え先のキー）
#                    を指定する（複数指定可）
#   （プレフィッスクキーの後に入力するキーが、Fakeymacs で置き換えられないようにする対策です）
#   （同じキーを指定することもできます）
#   （置き換え先のキーに Meta キー（M-）は指定できません）
#
# ３）"replace_key": 置き換えするキーの組み合わせ（置き換え元のキー、置き換え先のキー）を指定する
#                    （複数指定可）
#   （同じキーを指定することもできます）
#   （置き換え先のキーに Meta キー（M-）は指定できません）

try:
    # 設定されているか？
    fc.vscode_setting1
except:
    fc.vscode_setting1 = {"target"     : ["Code.exe",
                                          ["chrome.exe",  "Chrome_WidgetWin_1", fc.vscode_browser_title],
                                          ["msedge.exe",  "Chrome_WidgetWin_1", fc.vscode_browser_title],
                                          ["firefox.exe", "MozillaWindowClass", fc.vscode_browser_title],
                                          ["mstsc.exe",   "RAIL_WINDOW",        fc.vscode_browser_title],
                                          ],
                          "prefix_key" : [["C-k", "C-A-k"],
                                          ],
                          "replace_key": [["C-i", "C-i"],
                                          ]
                          }

try:
    # 設定されているか？
    fc.vscode_setting2
except:
    fc.vscode_setting2 = {"target"     : ["Cursor.exe",
                                          ],
                          "prefix_key" : [["C-k", "C-A-k"],
                                          ["C-m", "C-A-m"],
                                          ],
                          "replace_key": [["C-i", "C-i"],
                                          ["C-i", "C-A-i"],
                                          ["C-e", "C-A-e"],
                                          ["C-l", "C-A-l"],
                                          ]
                          }

try:
    # 設定されているか？
    fc.vscode_setting3
except:
    fc.vscode_setting3 = {"target"     : ["Windsurf.exe",
                                          ],
                          "prefix_key" : [["C-k", "C-A-k"],
                                          ],
                          "replace_key": [["C-i", "C-i"],
                                          ["C-i", "C-A-i"],
                                          ["C-l", "C-A-l"],
                                          ]
                          }

try:
    # 設定されているか？
    fc.vscode_setting4
except:
    fc.vscode_setting4 = {"target"     : ["Kiro.exe",
                                          ],
                          "prefix_key" : [["C-k", "C-A-k"],
                                          ],
                          "replace_key": [["C-i", "C-i"],
                                          ["C-i", "C-A-i"],
                                          ["C-l", "C-A-l"],
                                          ]
                          }

# --------------------------------------------------------------------------------------------------

try:
    # 設定されているか？
    fc.use_ctrl_atmark_for_mark
except:
    # 日本語キーボードを利用する際、VSCode で  C-@ をマーク用のキーとして使うかどうかを指定する
    # （True: 使う、False: 使わない）
    # （VSCode で C-@ を Toggle Terminal 用のキーとして使えるようにするために設けた設定です。
    #   True に設定した場合でも、Toggle Terminal 用のキーとして  C-<半角／全角> が使えます。）
    fc.use_ctrl_atmark_for_mark = False

try:
    # 設定されているか？
    fc.use_direct_input_in_vscode_terminal
except:
    # パネルのターミナル内で４つのキー（C-k、C-r、C-s、C-y）のダイレクト入力機能を使うかどうかを
    # 指定する（True: 使う、False: 使わない）
    # （この設定は、VSCode の settings.json に設定した window.title が有効に機能しないアプリ
    #   （Firebase Studio など）での利用を想定しています。）
    fc.use_direct_input_in_vscode_terminal = False

try:
    # 設定されているか？
    fc.terminal_list_for_direct_input
except:
    # ターミナルをエディタ領域で使う際、ダイレクト入力機能を使うターミナルの種類を指定する
    fc.terminal_list_for_direct_input = ["bash",
                                         "wsl",
                                         "powershell",
                                         "zsh"
                                         ]

try:
    # 設定されているか？
    fc.esc_mode_in_keyboard_quit
except:
    # keyboard_quit 関数実行時（C-g 押下時）の Esc キーの発行方法を指定する
    # （1：C-g を押下した際、常に Esc キーを発行する
    #   2：C-g を２回連続して押下した場合に Esc キーを発行する）
    fc.esc_mode_in_keyboard_quit = 1

# --------------------------------------------------------------------------------------------------

class FakeymacsVSCode:
    pass

fakeymacs_vscode = FakeymacsVSCode()

fakeymacs_vscode.vscode_focus = "not_terminal"
fakeymacs_vscode.rectangle_mode = False
fakeymacs_vscode.post_processing = None

vscode_target = []
for n in range(10):
    try:
        vscode_setting = getattr(fc, f"vscode_setting{n + 1}")
        if vscode_setting:
            vscode_target += vscode_setting["target"]
    except:
        pass

regex = "|".join([fnmatch.translate(app) for app in vscode_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
vscode_target1 = re.compile(regex)
vscode_target2 = [app for app in vscode_target if type(app) is list]

def is_vscode_target(window):
    global vscode_target_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == True and
            (vscode_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in vscode_target2))):
            vscode_target_status = True
        else:
            vscode_target_status = False

    return vscode_target_status

if fc.use_emacs_ime_mode:
    keymap_vscode = keymap.defineWindowKeymap(check_func=lambda wnd: (is_vscode_target(wnd) and
                                                                      not is_emacs_ime_mode(wnd)))
else:
    keymap_vscode = keymap.defineWindowKeymap(check_func=is_vscode_target)

fakeymacs.keymap_vscode = keymap_vscode

## 共通関数
def define_key_v(keys, command, skip_check=True):
    if skip_check:
        # 設定をスキップするキーの処理を行う
        if "keymap_vscode" in fc.skip_settings_key:
            for skey in fc.skip_settings_key["keymap_vscode"]:
                if fnmatch.fnmatch(keys, skey):
                    print(f"skip settings key : [keymap_vscode] {keys}")
                    return

    define_key(keymap_vscode, keys, command, False)

def define_key_v2(keys, command):
    define_key_v(keys, command, False)

def vscodeExecuteCommand(command, esc=False):
    def _func():
        self_insert_command("f1")()
        princ(command)
        self_insert_command("Enter")()

        if esc:
            # 上記のコマンドが実行できない時にコマンドパレットの表示を消すために入力する
            self_insert_command("Esc")()
    return _func

def vscodeExecuteCommand2(command, esc=False):
    def _func():
        setImeStatus(0)
        vscodeExecuteCommand(command, esc)()
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

pattern1 = re.compile("|".join([rf"(^| - ){v}( -|$)" for v in ["Terminal", "ターミナル"]]))
pattern2 = re.compile("|".join([rf"(^| - ){t}( -|$)" for t in fc.terminal_list_for_direct_input]))

def is_terminal_for_direct_input():
    title = getText()
    if pattern1.search(title) or pattern2.search(title):
        return True
    else:
        return False

## ファイル操作
def find_directory():
    # VSCode Command : File: Open Folder...
    # self_insert_command("C-k", "C-o")() # ターミナルで誤動作するのでショートカットキーは使わない
    vscodeExecuteCommand("workbench.action.files.openFolder")()

def recentf():
    # VSCode Command : File: Open Recent...
    # self_insert_command("C-r")() # ターミナルで誤動作するのでショートカットキーは使わない
    vscodeExecuteCommand("workbench.action.openRecent")()

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
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        kill_line(repeat)
    else:
        self_insert_command("C-k")()

def kill_line_v2():
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        self_insert_command("C-F4")()
    else:
        resetRegion()
        setMark()
        mark(move_end_of_line, True)()
        delay()
        kill_region()

def yank_v():
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        yank()
        delay() # C-u による繰り返し実行時に必要
    else:
        self_insert_command("C-y")()

## バッファ / ウィンドウ操作
def kill_buffer():
    # VS Code Web 画面で動作するように、C-F4 の発行とはしていない（C-F4 がブラウザでキャッチされるため）
    # VSCode Command : View: Close Editor
    vscodeExecuteCommand("workbench.action.closeActiveEditor")()

def switch_to_buffer():
    # VS Code Web 画面で動作するように、C-Tab の発行とはしていない（C-Tab がブラウザでキャッチされるため）
    # VSCode Command : View: Quick Open Privious Recently Used Editor in Group
    vscodeExecuteCommand("VQOPRRUEiG")()
    # vscodeExecuteCommand("workbench.action.quickOpenPreviousRecentlyUsedEditorInGroup")()

def list_buffers():
    # VSCode Command : View: Show All Editors By Most Recently Used
    vscodeExecuteCommand("VSAEBMRU")()
    # vscodeExecuteCommand("workbench.action.showAllEditorsByMostRecentlyUsed")()

## 文字列検索
def isearch_v(direction):
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        isearch(direction)
    else:
        self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()

def isearch_backward():
    isearch_v("backward")

def isearch_forward():
    isearch_v("forward")

## パネル操作
def focus_into_panel():
    # VSCode Command : View: Focus into Panel
    vscodeExecuteCommand("VFiPa")()
    # vscodeExecuteCommand("workbench.action.focusPanel")()

def close_panel():
    # VSCode Command : View: Close Panel
    # vscodeExecuteCommand("VCPa", esc=True)()

    # VSCode Command : View: Hide Panel
    vscodeExecuteCommand("VHP", esc=True)()
    # vscodeExecuteCommand("workbench.action.closePanel")()

def toggle_maximized_panel():
    # VSCode Command : View: Toggle Maximized Panel
    vscodeExecuteCommand("VTMP")()
    # vscodeExecuteCommand("workbench.action.toggleMaximizedPanel")()

## エディタ操作
def delete_window():
    if fakeymacs_vscode.vscode_focus == "not_terminal":
        # VSCode Command : View: Close All Editors in Group
        vscodeExecuteCommand("VCAEiG")()
        # vscodeExecuteCommand("workbench.action.closeEditorsInGroup")()
    else:
        close_panel()
        fakeymacs_vscode.vscode_focus = "not_terminal"

def delete_other_windows():
    if fakeymacs_vscode.vscode_focus == "not_terminal":
        # VSCode Command : View: Close Editors in Other Groups
        vscodeExecuteCommand("VCEiOG")()
        # vscodeExecuteCommand("workbench.action.closeEditorsInOtherGroups")()

        if fc.use_direct_input_in_vscode_terminal:
            close_panel()
    else:
        toggle_maximized_panel()

def split_window_below():
    if fakeymacs_vscode.vscode_focus == "not_terminal":
        # VSCode Command : View: Split Editor Orthogonal
        vscodeExecuteCommand("VSEOr")()
        # self_insert_command("C-k", "C-Yen")() # ターミナルで誤動作するのでショートカットキーは使わない
        # vscodeExecuteCommand("workbench.action.splitEditorOrthogonal")()
    else:
        toggle_maximized_panel()

def split_window_right():
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        # VSCode Command : View: Split Editor
        self_insert_command("C-Yen")()
        # vscodeExecuteCommand("workbench.action.splitEditor")()
    else:
        # VSCode Command : View: Split Terminal
        # self_insert_command("C-S-5")()
        vscodeExecuteCommand("workbench.action.terminal.split")()

def rotate_layout():
    if fakeymacs_vscode.vscode_focus == "not_terminal" and not is_terminal_for_direct_input():
        # VSCode Command : Toggle Vertical/Horizontal Editor Layout
        self_insert_command("A-S-0")()
        # vscodeExecuteCommand("workbench.action.toggleEditorGroupLayout")()

def other_window():
    # VSCode Command : View: Navigate Between Editor Groups
    vscodeExecuteCommand("VNBEdG")()
    # vscodeExecuteCommand("workbench.action.navigateEditorGroups")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs_vscode.vscode_focus = "not_terminal"

def switch_focus(number):
    def _func():
        # VSCode Command : View: Focus Side Bar or n-th Editor Group
        self_insert_command(f"C-{number}")()

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
    # region(vscodeExecuteCommand("editor.action.addSelectionToNextFindMatch"))()

def mark_all_like_this():
    # VSCode Command : Select All Occurrences of Find Match
    region(self_insert_command("C-S-l"))()
    # region(vscodeExecuteCommand("editor.action.selectHighlights"))()

def skip_to_previous_like_this():
    # VSCode Command : Move Last Selection To Previous Find Match
    region(vscodeExecuteCommand("MLSTPFM"))()
    # region(vscodeExecuteCommand("editor.action.moveSelectionToPreviousFindMatch"))()

def skip_to_next_like_this():
    # VSCode Command : Move Last Selection To Next Find Match
    region(vscodeExecuteCommand("MLSTNFM"))()
    # region(self_insert_command("C-k", "C-d"))() # ターミナルで誤動作するのでショートカットキーは使わない
    # region(vscodeExecuteCommand("editor.action.moveSelectionToNextFindMatch"))()

def expand_region():
    # VSCode Command : Expand Selection
    region(self_insert_command("A-S-Right"))()
    # region(vscodeExecuteCommand("editor.action.smartSelect.expand"))()

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
    # VSCode Command : Terminal: Create New Terminal
    vscodeExecuteCommand2("workbench.action.terminal.new")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs_vscode.vscode_focus = "terminal"

def toggle_terminal():
    if fc.use_direct_input_in_vscode_terminal:
        if fakeymacs_vscode.vscode_focus == "not_terminal":
            # VSCode Command : Terminal: Focus Terminal
            vscodeExecuteCommand2("workbench.action.terminal.focus")()

            fakeymacs_vscode.vscode_focus = "terminal"
        else:
            close_panel()
            fakeymacs_vscode.vscode_focus = "not_terminal"
    else:
        # VSCode Command : View: Toggle Terminal
        vscodeExecuteCommand2("workbench.action.terminal.toggleTerminal")()

def create_terminal_in_editor_area():
    # VSCode Command : Terminal: Create New Terminal in Editor Area
    vscodeExecuteCommand2("workbench.action.createTerminalEditor")()

    if fc.use_direct_input_in_vscode_terminal:
        fakeymacs_vscode.vscode_focus = "not_terminal"

## その他
def keyboard_quit_v2():
    if fc.esc_mode_in_keyboard_quit == 1:
        keyboard_quit(esc=True)
        fakeymacs_vscode.post_processing = None
    else:
        if (fakeymacs.last_keys[0] is keymap_vscode and
            fakeymacs.last_keys[1] in ["C-g", "C-A-G"]):
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
    self_insert_command("C-/")()
    # vscodeExecuteCommand("editor.action.commentLine")()

    resetRegion()

def trigger_suggest():
    # VSCode Command : Trigger Suggest
    self_insert_command("C-Space")()
    # vscodeExecuteCommand("editor.action.triggerSuggest")()

def zoom_in():
    # VSCode Command : View: Zoom In
    self_insert_command("C-;")()
    # vscodeExecuteCommand("workbench.action.zoomIn")()

## マルチストロークキーの設定
define_key_v("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_v("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_v("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_v("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

run_once = False
def mergeEmacsMultiStrokeKeymap():
    global run_once
    if not run_once:
        mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "Ctl-x")
        mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-")
        mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-g")
        mergeMultiStrokeKeymap(keymap_vscode, keymap_emacs, "M-g M-")
        run_once = True

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_vscode キーマップにマージする
keymap_vscode.applying_func = mergeEmacsMultiStrokeKeymap

## 「ファイル操作」のキー設定
define_key_v("Ctl-x C-d", reset_search(reset_undo(reset_counter(reset_mark(find_directory)))))
define_key_v("Ctl-x C-r", reset_search(reset_undo(reset_counter(reset_mark(recentf)))))
define_key_v("Ctl-x C-l", reset_search(reset_undo(reset_counter(reset_mark(locate)))))

## 「カーソル移動」のキー設定
define_key_v("M-g p",   reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key_v("M-g M-p", reset_search(reset_undo(reset_counter(reset_mark(previous_error)))))
define_key_v("M-g n",   reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
define_key_v("M-g M-n", reset_search(reset_undo(reset_counter(reset_mark(next_error)))))
define_key_v("Ctl-x `", reset_search(reset_undo(reset_counter(reset_mark(next_error)))))

# define_key_v("A-p", self_insert_command("C-Up"))
# define_key_v("A-n", self_insert_command("C-Down"))

## 「カット / コピー」のキー設定
define_key_v("C-k", reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_line_v))))))
define_key_v("A-k", reset_search(reset_undo(reset_counter(reset_mark(kill_line_v2)))))
define_key_v("C-y", reset_search(reset_undo(reset_counter(reset_mark(repeat(yank_v))))))

## 「バッファ / ウィンドウ操作」のキー設定
define_key_v("Ctl-x k",   reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_v("Ctl-x b",   reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
define_key_v("Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))

## 「文字列検索」のキー設定
define_key_v("C-r", reset_undo(reset_counter(reset_mark(isearch_backward))))
define_key_v("C-s", reset_undo(reset_counter(reset_mark(isearch_forward))))

## 「エディタ操作」のキー設定
define_key_v("Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_window)))))
define_key_v("Ctl-x 1", delete_other_windows)
define_key_v("Ctl-x 2", split_window_below)
define_key_v("Ctl-x 3", split_window_right)
define_key_v("Ctl-x 4", rotate_layout)
define_key_v("Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

if fc.use_ctrl_digit_key_for_digit_argument:
    key = "C-A-{}"
else:
    key = "C-{}"

for n in range(10):
    define_key_v(key.format(n), reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))

## 「矩形選択 / マルチカーソル」のキー設定
define_key_v("C-A-p",   reset_search(reset_undo(reset_counter(rect(repeat(mark_previous_line))))))
define_key_v("C-A-n",   reset_search(reset_undo(reset_counter(rect(repeat(mark_next_line))))))
define_key_v("C-A-b",   reset_search(reset_undo(reset_counter(repeat(mark_backward_char)))))
define_key_v("C-A-f",   reset_search(reset_undo(reset_counter(repeat(mark_forward_char)))))
define_key_v("C-A-S-b", reset_search(reset_undo(reset_counter(reset_rect(repeat(mark_backward_word))))))
define_key_v("C-A-S-f", reset_search(reset_undo(reset_counter(reset_rect(repeat(mark_forward_word))))))
define_key_v("C-A-a",   reset_search(reset_undo(reset_counter(reset_rect(mark_beginning_of_line)))))
define_key_v("C-A-e",   reset_search(reset_undo(reset_counter(reset_rect(mark_end_of_line)))))
define_key_v("C-A-S-e", reset_search(reset_undo(reset_counter(reset_rect(mark_end_of_line)))))
define_key_v("C-A-d",   reset_search(reset_undo(reset_counter(reset_rect(mark_next_like_this)))))
define_key_v("C-A-S-d", reset_search(reset_undo(reset_counter(reset_rect(mark_all_like_this)))))
define_key_v("C-A-s",   reset_search(reset_undo(reset_counter(reset_rect(skip_to_next_like_this)))))
define_key_v("C-A-S-s", reset_search(reset_undo(reset_counter(reset_rect(skip_to_previous_like_this)))))
define_key_v("C-A-x",   reset_search(reset_undo(reset_counter(reset_rect(expand_region)))))
define_key_v("C-A-S-x", reset_search(reset_undo(reset_counter(reset_rect(shrink_region)))))
define_key_v("C-A-u",   reset_search(reset_undo(reset_counter(reset_rect(cursor_undo)))))
define_key_v("C-A-r",   reset_search(reset_undo(reset_counter(reset_rect(cursor_redo)))))
define_key_v("C-A-g",   reset_search(reset_counter(reset_mark(keyboard_quit_v1))))

## 「ターミナル操作」のキー設定
define_key_v("C-S-(243)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key_v("C-S-(244)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
define_key_v("C-(243)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
define_key_v("C-(244)",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
define_key_v("C-A-(248)", reset_search(reset_undo(reset_counter(reset_mark(create_terminal_in_editor_area)))))

if is_japanese_keyboard:
    define_key_v("C-S-@", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    if not fc.use_ctrl_atmark_for_mark:
        define_key_v("C-@", reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
    define_key_v("C-A-@", reset_search(reset_undo(reset_counter(reset_mark(create_terminal_in_editor_area)))))
else:
    define_key_v("C-S-`", reset_search(reset_undo(reset_counter(reset_mark(create_terminal)))))
    define_key_v("C-`",   reset_search(reset_undo(reset_counter(reset_mark(toggle_terminal)))))
    define_key_v("C-A-`", reset_search(reset_undo(reset_counter(reset_mark(create_terminal_in_editor_area)))))

## 「その他」のキー設定
define_key_v("Enter", post(reset_undo(reset_counter(reset_mark(repeat(newline))))))
define_key_v("C-m",   post(reset_undo(reset_counter(reset_mark(repeat(newline))))))
define_key_v("C-g",   reset_search(reset_counter(reset_mark(keyboard_quit_v2))))
define_key_v("M-x",   reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key_v("M-;",   reset_search(reset_undo(reset_counter(reset_mark(comment_dwim)))))

if is_japanese_keyboard:
    define_key_v("C-:", trigger_suggest)
else:
    define_key_v("C-'", trigger_suggest)

if use_usjis_keyboard_conversion:
    define_key_v("C-=", zoom_in)

# --------------------------------------------------------------------------------------------------

# エディタターゲット毎のキーバインドの追加設定

def set_vscode_target(vscode_setting):
    regex = "|".join([fnmatch.translate(app) for app in vscode_setting["target"] if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    target1 = re.compile(regex)
    target2 = [app for app in vscode_setting["target"] if type(app) is list]

    target_status = False

    def is_target(window):
        nonlocal target_status

        if window is not fakeymacs.last_window or fakeymacs.force_update:
            if (vscode_target_status == True and
                (target1.match(getProcessName(window)) or
                 any(checkWindow(*app, window=window) for app in target2))):
                target_status = True
            else:
                target_status = False

        return target_status

    if fc.use_emacs_ime_mode:
        keymap_target = keymap.defineWindowKeymap(check_func=lambda wnd: (is_target(wnd) and
                                                                          not is_emacs_ime_mode(wnd)))
    else:
        keymap_target = keymap.defineWindowKeymap(check_func=is_target)

    ## プレフィックスキーの置き換え設定
    for pkey1, pkey2 in vscode_setting["prefix_key"]:
        define_key(keymap_target, pkey2, keymap.defineMultiStrokeKeymap(f"<VSCode> {pkey1}"))

        for vkey in vkeys():
            key = vkToStr(vkey)
            for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
                mkey = mod1 + mod2 + mod3 + mod4 + key
                define_key(keymap_target, f"{pkey2} {mkey}", self_insert_command4(pkey1, mkey))

    ## キーの置き換え設定
    for key1, key2 in vscode_setting["replace_key"]:
        define_key(keymap_target, key2, self_insert_command(key1))

for n in range(10):
    try:
        vscode_setting = getattr(fc, f"vscode_setting{n + 1}")
        if vscode_setting:
            set_vscode_target(vscode_setting)
    except:
        pass

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"vscode_key\config_personal.py", msg=False), dict(globals(), **locals()))
