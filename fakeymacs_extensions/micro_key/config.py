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

## バッファ / ウィンドウ操作
def kill_buffer():
    self_insert_command("C-q")()

## エディタ操作
def delete_window():
    self_insert_command("C-q")()

def split_window_below():
    microExecuteCommand("hsplit")()

def split_window_right():
    microExecuteCommand("vsplit")()

def other_window():
    self_insert_command("C-w")()

## その他
def execute_extended_command():
    self_insert_command3("C-e")()

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

## 「バッファ / ウィンドウ操作」のキー設定
define_key_u("M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
define_key_u("Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))

## 「エディタ操作」のキー設定
define_key_u("Ctl-x 0", reset_search(reset_undo(reset_counter(reset_mark(delete_window)))))
define_key_u("Ctl-x 2", reset_search(reset_undo(reset_counter(reset_mark(split_window_below)))))
define_key_u("Ctl-x 3", reset_search(reset_undo(reset_counter(reset_mark(split_window_right)))))
define_key_u("Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

## 「その他」のキー設定
define_key_u("M-x", reset_search(reset_undo(reset_counter(reset_mark(execute_extended_command)))))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"micro_key\config_personal.py", msg=False), dict(globals(), **locals()))
