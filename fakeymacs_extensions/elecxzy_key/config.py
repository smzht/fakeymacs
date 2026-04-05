# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## elecxzy 用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.elecxzy_target
except:
    # elecxzy 用のキーバインドを利用するアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.elecxzy_target = ["elecxzy.exe",
                         ]

# --------------------------------------------------------------------------------------------------

regex = "|".join([fnmatch.translate(app) for app in fc.elecxzy_target if type(app) is str])
if regex == "": regex = "$." # 絶対にマッチしない正規表現
elecxzy_target1 = re.compile(regex)
elecxzy_target2 = [app for app in fc.elecxzy_target if type(app) is list]

def is_elecxzy(window):
    global mc_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == False and
            (elecxzy_target1.match(getProcessName(window)) or
             any(checkWindow(*app, window=window) for app in elecxzy_target2))):
            mc_status = True
        else:
            mc_status = False

    return mc_status

if fc.use_emacs_ime_mode:
    keymap_elecxzy = keymap.defineWindowKeymap(check_func=lambda wnd: (is_elecxzy(wnd) and
                                                                  not is_emacs_ime_mode(wnd)))
else:
    keymap_elecxzy = keymap.defineWindowKeymap(check_func=is_elecxzy_target)

## 共通関数
def define_key_e(keys, command):
    define_key(keymap_elecxzy, keys, command)

## マルチストロークキーの設定
define_key_e("M-", keymap.defineMultiStrokeKeymap("Esc"))

for vkey in vkeys():
    key = vkToStr(vkey)

    if key == "Escape":
        continue

    for mod1, mod2 in itertools.product(["", "C-"], ["", "S-"]):
        mkey = mod1 + mod2 + key
        define_key_e(f"M-{mkey}",   self_insert_command(f"A-{mkey}"))

## Esc キーの設定
if fc.use_esc_as_meta:
    define_key_e("Esc Esc", self_insert_command("Esc","Esc"))

if fc.use_ctrl_openbracket_as_meta:
    define_key_e("C-[ C-[", self_insert_command("Esc","Esc"))
else:
    define_key_e("C-[", self_insert_command("Esc"))

# --------------------------------------------------------------------------------------------------

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"elecxzy_key\config_personal.py", msg=False), dict(globals(), **locals()))
