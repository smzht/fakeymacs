# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## SpaceFN を実現する設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.space_fn_key
except:
    # SpaceFN 用のモディファイアキーを指定する
    fc.space_fn_key = "Space"

try:
    # 設定されているか？
    fc.space_fn_window_keymap_list
except:
    # SpaceFN を適用するキーマップを指定する
    fc.space_fn_window_keymap_list = [keymap_emacs, keymap_ime]

    try:
        # vscode_key Extension は有効か？
        fakeymacs.keymap_vscode

        fc.space_fn_window_keymap_list += [fakeymacs.keymap_vscode]
    except:
        pass

try:
    # 設定されているか？
    fc.space_fn_use_one_shot_function
except:
    # SpaceFN 用のモディファイアキーの単押しで、元のキーの機能を利用するかどうかを指定する
    # （True: 使う、False: 使わない）
    fc.space_fn_use_one_shot_function = True

replace_key = "(200)"
fakeymacs.is_space_fn_mode = None

def define_key_fn(window_keymap, keys, command):
    func = getKeyAction(keys.replace("U0-", ""))

    def _func():
        if fakeymacs.last_keys[1] == replace_key:
            fakeymacs.is_space_fn_mode = True
        elif replace_key in fakeymacs.last_keys[1]:
            fakeymacs.is_space_fn_mode = False

        if fakeymacs.is_space_fn_mode:
            command()
        else:
            func()

    define_key(window_keymap, keys, _func)

def replicate_key(window_keymap, keys, original_key):
    func = getKeyAction(original_key)
    define_key_fn(window_keymap, keys, func)

keymap.replaceKey(fc.space_fn_key, replace_key)
keymap.defineModifier(replace_key, "User0")

# fc.space_fn_key を使う全てのキーを replace_key を使うキーに複製する
for window_keymap in keymap.window_keymap_list:
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod = mod1 + mod2 + mod3 + mod4
        func = getKeyCommand(window_keymap,  mod + fc.space_fn_key)
        if func:
            define_key(window_keymap, mod + replace_key, func)

func = getKeyAction(fc.space_fn_key)

for window_keymap in fc.space_fn_window_keymap_list:

    # 全てのキーの入力パターンを SpaceFN 用のモディファイアキーを使うキーに複製する
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
            mkey0 =         mod1 + mod2 + mod3 + mod4 + key
            mkey1 = "U0-" + mod1 + mod2 + mod3 + mod4 + key
            define_key_fn(window_keymap, mkey1, self_insert_command(mkey0)) # Windows 本来のキーを発行する

    # SpaceFN 用のワンショットモディファイアキーの設定を行う
    if fc.space_fn_use_one_shot_function:
        define_key(window_keymap, "O-" + replace_key, func)
    define_key(window_keymap, replace_key, lambda: None)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
