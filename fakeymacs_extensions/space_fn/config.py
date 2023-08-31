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

fakeymacs.is_space_fn_mode = None

def define_key_fn(window_keymap, keys, command):
    func = getKeyCommand(window_keymap, keys.replace("U0-", ""))
    if func is None:
        func = self_insert_command(keys.replace("U0-", ""))

    def _func():
        if fakeymacs.last_keys[1] == fc.space_fn_key:
            fakeymacs.is_space_fn_mode = True
        elif fc.space_fn_key in fakeymacs.last_keys[1]:
            fakeymacs.is_space_fn_mode = False

        if fakeymacs.is_space_fn_mode:
            command()
        else:
            func()

    define_key(window_keymap, keys, _func)

def replicate_key(window_keymap, keys, original_keys):
    func = getKeyCommand(window_keymap, original_keys)
    if func is None:
        func = self_insert_command(original_keys)
    define_key_fn(window_keymap, keys, func)

keymap.defineModifier(fc.space_fn_key, "User0")

for window_keymap in fc.space_fn_window_keymap_list:

    # SpaceFN 用のモディファイアキーを除く、全てのキーパターンの設定を行う
    for vkey in vkeys():
        key = vkToStr(vkey)
        if key != keyStrNormalization(fc.space_fn_key):
            for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
                mkey0 =         mod1 + mod2 + mod3 + mod4 + key
                mkey1 = "U0-" + mod1 + mod2 + mod3 + mod4 + key
                define_key_fn(window_keymap, mkey1, self_insert_command(mkey0))

    # SpaceFN 用のワンショットモディファイアキーの設定を行う
    if fc.space_fn_use_one_shot_function:
        func = getKeyCommand(window_keymap, fc.space_fn_key)
        if func is None:
            func = self_insert_command(fc.space_fn_key)
        define_key(window_keymap, "O-" + fc.space_fn_key, func)
    define_key(window_keymap, fc.space_fn_key, lambda: None)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
