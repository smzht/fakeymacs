# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## SpaceFn を実現する設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.space_fn_key
except:
    # SpaceFn 用のモディファイアキーを指定する
    fc.space_fn_key = "Space"

try:
    # 設定されているか？
    fc.space_fn_window_keymap_list
except:
    # SpaceFn 用を適用するキーマップリストを指定する
    fc.space_fn_window_keymap_list = [keymap_emacs, keymap_ime]

keymap.defineModifier(fc.space_fn_key, "User0")

for window_keymap in fc.space_fn_window_keymap_list:
    mkey0 = fc.space_fn_key
    mkey1 = "O-" + fc.space_fn_key

    func = getKeyCommand(window_keymap, mkey0)
    if func:
        define_key(window_keymap, mkey1, func)
    else:
        define_key(window_keymap, mkey1, self_insert_command(mkey0))

    define_key(window_keymap, mkey0, lambda: None)

def define_key_f(keys, command):
    for window_keymap in fc.space_fn_window_keymap_list:
        define_key(window_keymap, keys, command)

def replicate_key(keys, originalKeys):
    for window_keymap in fc.space_fn_window_keymap_list:
        func = getKeyCommand(window_keymap, originalKeys)
        if func:
            define_key(window_keymap, keys, func)
        else:
            define_key(window_keymap, keys, self_insert_command(originalKeys))

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
