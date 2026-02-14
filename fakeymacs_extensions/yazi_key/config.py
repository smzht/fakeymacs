####################################################################################################
## Yazi 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.yazi_target
except:
    # Yazi 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.yazi_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", ["Yazi: *", "* Yazi: *"]],
                      ]

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.yazi_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
yazi_target1 = re.compile(regex)
yazi_target2 = [app for app in fc.yazi_target if type(app) is list]

def is_yazi(window):
    global yazi_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == False and
            (yazi_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in yazi_target2))):
            yazi_status = True
        else:
            yazi_status = False

    return yazi_status

if fc.use_emacs_ime_mode:
    keymap_yazi = keymap.defineWindowKeymap(check_func=lambda wnd: (is_yazi(wnd) and
                                                                    not is_emacs_ime_mode(wnd)))
else:
    keymap_yazi = keymap.defineWindowKeymap(check_func=is_yazi_target)

## 共通関数
def define_key_y(keys, command):
    define_key(keymap_yazi, keys, command)

## カーソル移動
def backward_char():
    self_insert_command("Left")()

def forward_char():
    self_insert_command("Right")()

def previous_line():
    self_insert_command("Up")()

def next_line():
    self_insert_command("Down")()

def beginning_of_buffer():
    self_insert_command("g", "g")()

def end_of_buffer():
    self_insert_command("S-g")()

def scroll_up():
    self_insert_command("C-u")()

def scroll_down():
    self_insert_command("C-d")()

## 文字列検索
def isearch(direction):
    if fakeymacs.is_searching is None:
        self_insert_command("/")()
        fakeymacs.is_searching = False

    elif fakeymacs.is_searching is True:
        self_insert_command({"backward":"S-n", "forward":"n"}[direction])()

def isearch_backward():
    isearch("backward")

def isearch_forward():
    isearch("forward")

## その他
def keyboard_quit():
    escape()

    if fakeymacs.is_searching == False:
        fakeymacs.is_searching = None

def kill_emacs():
    self_insert_command("q")()

## マルチストロークキーの設定
define_key_y("Ctl-x", keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_y("M-",    keymap.defineMultiStrokeKeymap("Esc"))

## Esc キーの設定
if fc.use_esc_as_meta:
    define_key_y("Esc Esc", escape)
else:
    define_key_y("Esc",  escape)

if fc.use_ctrl_openbracket_as_meta:
    define_key_y("C-[ C-[",  escape)
else:
    define_key_y("C-[",  escape)

## 「カーソル移動」のキー設定
define_key_y("C-b", backward_char)
define_key_y("C-f", forward_char)
define_key_y("C-p", previous_line)
define_key_y("C-n", next_line)
define_key_y("M-<", beginning_of_buffer)
define_key_y("M->", end_of_buffer)
if fc.scroll_key:
    define_key_y(fc.scroll_key[0], scroll_up)
    define_key_y(fc.scroll_key[1], scroll_down)

## 「文字列検索」のキー設定
define_key_y("C-r", isearch_backward)
define_key_y("C-s", isearch_forward)

## 「その他」のキー設定
define_key_y("Enter",     newline)
define_key_y("C-m",       newline)
define_key_y("C-g",       reset_search(keyboard_quit))
define_key_y("Ctl-x C-c", kill_emacs)

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"yazi_key\config_personal.py", msg=False), dict(globals(), **locals()))
