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
    # 設定されているか？
    fc.space_fn_use_one_shot_function
except:
    # SpaceFN 用のモディファイアキーの単押しで、元のキーの機能を利用するかどうかを指定する
    # （True: 使う、False: 使わない）
    fc.space_fn_use_one_shot_function = True

def replicate_key(window_keymap, keys, original_keys):
    func = getKeyCommand(window_keymap, original_keys)
    if func:
        define_key(window_keymap, keys, func)
    else:
        define_key(window_keymap, keys, self_insert_command(original_keys))

keymap.defineModifier(fc.space_fn_key, "User0")

# US と JIS のキーボード変換の機能を有効にしている場合は、変換が必要となるキーを keymap_base
# に登録する
if use_usjis_keyboard_conversion:
    for us_key, jis_list in usjis_key_table.items():
        if jis_list[0]:
            for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"]):
                mkey0 =         mod1 + mod2 + mod3 + us_key
                mkey1 = "U0-" + mod1 + mod2 + mod3 + us_key
                define_key(keymap_base, mkey1, self_insert_command(mkey0))

mkey0 = fc.space_fn_key
mkey1 = "O-" + fc.space_fn_key

for window_keymap in fc.space_fn_window_keymap_list:
    if fc.space_fn_use_one_shot_function:
        replicate_key(window_keymap, mkey1, mkey0)
    define_key(window_keymap, mkey0, lambda: None)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
