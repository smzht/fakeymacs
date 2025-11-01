# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Obsidian 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.obsidian_language
except:
    # Obsidian に設定している表示言語を指定する（US: English、JP: 日本語）
    # fc.obsidian_language = "US"
    fc.obsidian_language = "JP"

try:
    # 設定されているか？
    fc.obsidian_target
except:
    # Obsidian 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.obsidian_target = ["Obsidian.exe",
                          ["chrome.exe",  "Chrome_WidgetWin_1", ["Obsidian", "Obsidian および他*"]],
                          ["msedge.exe",  "Chrome_WidgetWin_1", ["Obsidian", "Obsidian および他*"]],
                          ["firefox.exe", "MozillaWindowClass", "Obsidian — Mozilla Firefox"],
                          ["mstsc.exe",   "RAIL_WINDOW",        ["Obsidian (リモート)",
                                                                 "Obsidian および他*"]],
                          ]

try:
    # 設定されているか？
    fc.obsidian_replace_key
except:
    # 置き換えするキーの組み合わせ（置き換え元のキー、置き換え先のキー）を指定する（複数指定可）
    # （参考：https://blog.astha.jp/post-3925/）
    fc.obsidian_replace_key = [["C-A-Left",  "C-A-p"], # Obsidian Command : Navigate back
                               ["C-A-Right", "C-A-n"], # Obsidian Command : Navigate forward
                               ["C-S-f", "C-A-s"],     # Obsidian Command : Search: Search in all files
                               ["C-t", "C-t"],         # Obsidian Command : New tab
                               ["C-k", "C-A-k"],       # Obsidian Command : Insert Markdown link
                               ["C-e", "C-A-e"],       # Obsidian Command : Toggle reading view
                               ["C-l", "C-A-l"],       # Obsidian Command : Toggle checkbox status
                               ["C-b", "C-A-b"],       # Obsidian Command : Toggle bold
                               ["C-i", "C-A-i"],       # Obsidian Command : Toggle Italic
                               ["C-g", "C-A-g"],       # Obsidian Command : Graph view: Open graph view
                               ["C-,", "C-A-,"],       # Obsidian Command : Open settings
                               ]

# Quick Switcher: Open quick switcher で C-Enter のキー操作が RCtrl で動作しない対策
fc.obsidian_replace_key += [["RC-Enter", "C-Enter"]]

try:
    # 設定されているか？
    fc.obsidian_command_dict
except:
    # Obsidian の Command pallet で利用するコマンドを指定する（key: 英語コマンド、value: 日本語コマンド）
    fc.obsidian_command_dict = {"Close current tab"         : "現在のタブを閉じる",
                                "Go to next tab"            : "次のタブに移動",
                                "Close this tab group"      : "このタブグループを閉じる",
                                "Close all other tabs"      : "他のタブをすべて閉じる",
                                "Split down"                : "下に分割",
                                "Split right"               : "右に分割",
                                "Focus on tab group"        : "タブグループにフォーカス",
                                "Files: Show file explorer" : "ファイル: ファイルエクスプローラを表示",
                                "Zoom in"                   : "ズームイン",
                                }

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.obsidian_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
obsidian_target1 = re.compile(regex)
obsidian_target2 = [app for app in fc.obsidian_target if type(app) is list]

def is_obsidian(window):
    global obsidian_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == True and
            (obsidian_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in obsidian_target2))):
            obsidian_status = True
        else:
            obsidian_status = False

    return obsidian_status

if fc.use_emacs_ime_mode:
    keymap_obsidian = keymap.defineWindowKeymap(check_func=lambda wnd: (is_obsidian(wnd) and
                                                                        not is_emacs_ime_mode(wnd)))
else:
    keymap_obsidian = keymap.defineWindowKeymap(check_func=is_obsidian_target)

## 共通関数
def define_key_o(keys, command):
    define_key(keymap_obsidian, keys, command)

def obsidianExecuteCommand(command, esc=False):
    if fc.obsidian_language == "JP":
        command = fc.obsidian_command_dict[command]

    def _func():
        self_insert_command("C-p")()
        princ(command)
        self_insert_command("Enter")()

        if esc:
            # 上記のコマンドが実行できない時にコマンドパレットの表示を消すために入力する
            self_insert_command("Esc")()
    return _func

def obsidianExecuteCommand2(command, esc=False):
    def _func():
        setImeStatus(0)
        obsidianExecuteCommand(command, esc)()
    return _func

## バッファ / ウィンドウ操作
def kill_buffer():
    # Obsidian Command : Close current tab
    self_insert_command("C-w")()

def kill_buffer_o():
    # Obsidian-remote 画面で動作するように、C-w の発行とはしていない
    # Obsidian Command : Close current tab
    obsidianExecuteCommand("Close current tab")()

def switch_to_buffer():
    # ブラウザで動作するように、C-Tab の発行とはしていない（C-Tab がブラウザでキャッチされるため）
    # Obsidian Command : Go to next tab
    obsidianExecuteCommand("Go to next tab")()

## エディタ操作
def delete_window():
    # Obsidian Command : Close this tab group
    obsidianExecuteCommand("Close this tab group")()

def delete_other_windows():
    # Obsidian Command : Close all other tabs
    # （other tab groups が close する他、this tab group の other tabs も close となります）
    obsidianExecuteCommand("Close all other tabs", esc=True)()

def split_window_below():
    # Obsidian Command : Split down
    obsidianExecuteCommand("Split down", esc=True)()

def split_window_right():
    # Obsidian Command : Split right
    obsidianExecuteCommand("Split right", esc=True)()

def other_window():
    # Obsidian Command : Focus on tab group ...
    # （tab group が２分割の状態のときのみ正常に動作します（３分割以上では正常に動作しません））
    obsidianExecuteCommand("Focus on tab group", esc=True)()

def switch_focus(number):
    if number == 0:
        def _func():
            # Obsidian Command : Files: Show file explorer
            obsidianExecuteCommand("Files: Show file explorer")()
    else:
        def _func():
            # Obsidian Command : Go to tab #n or last tab
            self_insert_command(f"C-{number}")()
    return _func

## その他
def execute_extended_command():
    # Obsidian Command : Command palette: Open command palette
    self_insert_command3("C-p")()

def comment_dwim():
    # Obsidian Command : Toggle comment
    self_insert_command("C-/")()

def zoom_in():
    # Obsidian Command : Zoom in
    obsidianExecuteCommand("Zoom in")()

## マルチストロークキーの設定
define_key_o("Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_o("M-",     keymap.defineMultiStrokeKeymap("Esc"))
define_key_o("M-g",    keymap.defineMultiStrokeKeymap("M-g"))
define_key_o("M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

run_once = False
def mergeEmacsMultiStrokeKeymap():
    global run_once
    if not run_once:
        mergeMultiStrokeKeymap(keymap_obsidian, keymap_emacs, "Ctl-x")
        mergeMultiStrokeKeymap(keymap_obsidian, keymap_emacs, "M-")
        mergeMultiStrokeKeymap(keymap_obsidian, keymap_emacs, "M-g")
        mergeMultiStrokeKeymap(keymap_obsidian, keymap_emacs, "M-g M-")
        run_once = True

## keymap_emacs キーマップのマルチストロークキーの設定を keymap_obsidian キーマップにマージする
keymap_obsidian.applying_func = mergeEmacsMultiStrokeKeymap

## 「バッファ / ウィンドウ操作」のキー設定
define_key_o("M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_o("Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer_o)))))
define_key_o("Ctl-x b", reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))

## 「エディタ操作」のキー設定
define_key_o("Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_window)))))
define_key_o("Ctl-x 1", delete_other_windows)
define_key_o("Ctl-x 2", split_window_below)
define_key_o("Ctl-x 3", split_window_right)
define_key_o("Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

if fc.use_ctrl_digit_key_for_digit_argument:
    for n in range(10):
        define_key_o(f"C-A-{n}", reset_search(reset_undo(reset_counter(reset_mark(switch_focus(n))))))
else:
    define_key_o(f"C-0", reset_search(reset_undo(reset_counter(reset_mark(switch_focus(0))))))

## 「その他」のキー設定
define_key_o("M-x", reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))
define_key_o("M-;", reset_search(reset_undo(reset_counter(reset_mark(comment_dwim)))))

if os_keyboard_type == "JP":
    if use_usjis_keyboard_conversion:
        define_key_o("C-=", zoom_in)
    else:
        define_key_o("C-S-;", zoom_in)

## キーの置き換え設定
for key1, key2 in fc.obsidian_replace_key:
    define_key_o(key2, self_insert_command(key1))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"obsidian_key\config_personal.py", msg=False), dict(globals(), **locals()))
