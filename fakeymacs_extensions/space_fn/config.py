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
    # SpaceFn を適用するキーマップを指定する
    fc.space_fn_window_keymap_list = [keymap_emacs, keymap_ime]

try:
    # 設定されているか？
    fc.space_fn_use_one_shot_function
except:
    # SpaceFn 用のモディファイアキーの単押しで、元のキーの機能を利用するかどうかを指定する
    # （True: 使う、False: 使わない）
    fc.space_fn_use_one_shot_function = True

def replicate_key(window_keymap, keys, originalKeys):
    func = getKeyCommand(window_keymap, originalKeys)
    if func:
        define_key(window_keymap, keys, func)
    else:
        define_key(window_keymap, keys, self_insert_command(originalKeys))

keymap.defineModifier(fc.space_fn_key, "User0")

mkey0 = fc.space_fn_key
mkey1 = "O-" + fc.space_fn_key

for window_keymap in fc.space_fn_window_keymap_list:
    if fc.space_fn_use_one_shot_function:
        replicate_key(window_keymap, mkey1, mkey0)
    define_key(window_keymap, mkey0, lambda: None)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
