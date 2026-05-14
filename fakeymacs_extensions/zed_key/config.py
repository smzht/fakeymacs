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
        princ(command)
        self_insert_command("Enter")()
    return _func

## カーソル移動
def move_beginning_of_line():
    zedExecuteCommand("editor:move to start of excerpt")()

def move_end_of_line():
    zedExecuteCommand("editor:move to end of excerpt")()

## ウィンドウ操作
def delete_window():
    self_insert_command("C-w")()

def delete_other_windows():
    # 正常に動かない
    self_insert_command("C-A-S-t")()

def split_window_below():
    self_insert_command("C-k", "Down")()

def split_window_right():
    self_insert_command("C-k", "Right")()

def other_window():
    zedExecuteCommand("workspace:activate next pane")()

## その他
def execute_extended_command():
    self_insert_command3("C-S-p")()

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

## 「カーソル移動」のキー設定
define_key_z("M-<", reset("suc", mark(beginning_of_buffer, False)))
define_key_z("M->", reset("suc", mark(end_of_buffer, True)))

## 「ウィンドウ操作」のキー設定
define_key_z("Ctl-x 0", reset("sucm", delete_window))
define_key_z("Ctl-x 1", delete_other_windows)
define_key_z("Ctl-x 2", split_window_below)
define_key_z("Ctl-x 3", split_window_right)
define_key_z("Ctl-x o", reset("sucm", other_window))

## 「その他」のキー設定
define_key_z("M-x", reset("sucm", execute_extended_command))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"zed_key\config_personal.py", msg=False), dict(globals(), **locals()))
