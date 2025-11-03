####################################################################################################
## Midnight Commander 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.mc_target
except:
    # Midnight Commander 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.mc_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "mc *"],
                    [None, "ConsoleWindowClass", "mc *"],
                    ]

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.mc_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
mc_target1 = re.compile(regex)
mc_target2 = [app for app in fc.mc_target if type(app) is list]

def is_mc(window):
    global mc_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == False and
            (mc_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in mc_target2))):
            mc_status = True
        else:
            mc_status = False

    return mc_status

if fc.use_emacs_ime_mode:
    keymap_mc = keymap.defineWindowKeymap(check_func=lambda wnd: (is_mc(wnd) and
                                                                  not is_emacs_ime_mode(wnd)))
else:
    keymap_mc = keymap.defineWindowKeymap(check_func=is_mc_target)

## 共通関数
def define_key_m(keys, command):
    define_key(keymap_mc, keys, command)

## カーソル移動
def beginning_of_buffer():
    self_insert_command("Home")()

def end_of_buffer():
    self_insert_command("End")()

## パネル操作
def other_window():
    self_insert_command("Tab")()

## マルチストロークキーの設定
define_key_m("Ctl-x", keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
define_key_m("M-",    keymap.defineMultiStrokeKeymap("Esc"))

for vkey in vkeys():
    key = vkToStr(vkey)

    if key == "Escape":
        continue

    define_key_m(f"M-{key}",   self_insert_command4(f"A-{key}"))
    define_key_m(f"M-S-{key}", self_insert_command4(f"A-S-{key}"))

    for mod1, mod2 in itertools.product(["", "C-"], ["", "S-"]):
        mkey = mod1 + mod2 + key
        define_key_m(f"Ctl-x {mkey}", self_insert_command4("C-x", mkey))

## Esc キーの設定
define_key_m(f"Esc Esc", self_insert_command4("Esc","Esc"))
define_key_m(f"C-[ C-[", self_insert_command4("Esc","Esc"))

## 「カーソル移動」のキー設定
define_key_m("M-<", beginning_of_buffer)
define_key_m("M->", end_of_buffer)

## 「パネル操作」のキー設定
define_key_m("Ctl-x o", other_window)

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"mc_key\config_personal.py", msg=False), dict(globals(), **locals()))
