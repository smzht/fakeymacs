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

user_key = "(200)"
space_fn_key_func = getKeyAction(fc.space_fn_key)

is_space_fn_mode = False

def define_key_fn(window_keymap, keys, command):
    func = getKeyAction(keys.replace("U0-", ""))

    def _func():
        global is_space_fn_mode

        if fakeymacs.last_keys[1] == user_key:
            is_space_fn_mode = True
        elif user_key in fakeymacs.last_keys[1]:
            is_space_fn_mode = False

        if is_space_fn_mode:
            command()
        else:
            func()

    define_key(window_keymap, keys, _func)

def replicate_key(window_keymap, keys, original_key):
    define_key_fn(window_keymap, keys, getKeyAction(original_key))

is_space_fn_key_replaced = False

def replace_space_fn_key(window):
    global is_space_fn_key_replaced

    if fakeymacs.is_base_target:
        if not is_space_fn_key_replaced:
            keymap.replaceKey(fc.space_fn_key, user_key)
            is_space_fn_key_replaced = True
    else:
        if is_space_fn_key_replaced:
            keymap.replaceKey(fc.space_fn_key, fc.space_fn_key)
            is_space_fn_key_replaced = False

    return False

keymap.defineWindowKeymap(check_func=replace_space_fn_key)

keymap.defineModifier(user_key, "User0")

for window_keymap in keymap.window_keymap_list:

    # fc.space_fn_key を使うキーに割り当てられている設定を user_key を使うキーに設定する
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod   = mod1 + mod2 + mod3 + mod4
        mkey0 = mod + fc.space_fn_key
        mkey1 = mod + user_key
        func = getKeyCommand(window_keymap,  mkey0)
        if func:
            define_key(window_keymap, mkey1, func)

# fc.space_fn_key を使う全てのキーの入力パターンを user_key を使うキーに設定する
for mod1, mod2, mod3, mod4 in itertools.product(["", "LW-", "RW-"],
                                                ["", "LA-", "RA-"],
                                                ["", "LC-", "RC-"],
                                                ["", "S-"]):
    mod   = mod1 + mod2 + mod3 + mod4
    mkey0 = mod + fc.space_fn_key
    mkey1 = mod + user_key
    if not getKeyCommand(keymap_base,  mkey1):
        define_key(keymap_base, mkey1, self_insert_command(mkey0))

# 全てのキーの入力パターンを SpaceFN 用のモディファイアキーを使うキーに設定する
for vkey in vkeys():
    key = vkToStr(vkey)
    for mod1, mod2, mod3 in itertools.product(["", "A-"], ["", "C-"], ["", "S-"]):
        mod   = mod1 + mod2 + mod3
        mkey0 =         mod + key
        mkey1 = "U0-" + mod + key
        define_key_fn(keymap_base, mkey1, self_insert_command(mkey0))

# US と JIS のキーボード変換の機能を有効にしている場合は、変換が必要となるキーを、左右両方の
# モディファイアキーの全てのパターンで SpaceFN 用のモディファイアキーを使うキーに設定する
if use_usjis_keyboard_conversion:
    for us_key, jis_list in usjis_key_table.items():
        if jis_list[0]:
            for mod1, mod2 in itertools.product(["", "LA-", "RA-"], ["", "LC-", "RC-"]):
                mod   = mod1 + mod2
                mkey0 =         mod + us_key
                mkey1 = "U0-" + mod + us_key
                if not getKeyCommand(keymap_base, mkey1):
                    define_key(keymap_base, mkey1, self_insert_command(mkey0))

for window_keymap in fc.space_fn_window_keymap_list:

    # SpaceFN 用のワンショットモディファイアキーの設定を行う
    if fc.space_fn_use_one_shot_function:
        define_key(window_keymap, "O-" + user_key, space_fn_key_func)
    define_key(window_keymap, user_key, lambda: None)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
