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
    fc.space_fn_use_oneshot_function
except:
    # SpaceFN 用のモディファイアキーの単押しで、元のキーの機能を利用するかどうかを指定する
    # （True: 使う、False: 使わない）
    fc.space_fn_use_oneshot_function = True

try:
    # 設定されているか？
    fc.space_fn_delay_seconds
except:
    # SpaceFN 用のモディファイアキーが押下されてから、SpacdFN の機能が働くようになるまでの秒数を指定する
    fc.space_fn_delay_seconds = 0.15

user0_key = "(200)"
user3_key = "(201)"
space_fn_key_action = getKeyAction(fc.space_fn_key)

keymap.defineModifier(user0_key, "User0")
keymap.defineModifier(user3_key, "User3")

is_space_fn_mode = False
space_fn_key_oneshot = False
space_fn_key_down_time = 0

def space_fn_key_down():
    global space_fn_key_oneshot
    global space_fn_key_down_time
    space_fn_key_oneshot = True
    space_fn_key_down_time = time.time()

def space_fn_key_up():
    if space_fn_key_oneshot:
        space_fn_key_action()

def space_fn_command(func):
    def _func():
        global space_fn_key_oneshot
        space_fn_key_oneshot = False
        func()
    return _func

def define_key_fn(window_keymap, keys, command, space_fn_key_output=False):
    key_list = kbd(keys)[0]

    if "U0-" not in key_list[0]:
        return

    keys1 = keys.replace("U0-", "U1-", 1)

    if callable(command):
        _command1 = command
    else:
        define_key(window_keymap, keys1, command)
        _command1 = lambda: keymap.enterMultiStroke(command)

    if len(key_list) == 1:
        func = getKeyAction(keys.replace("U0-", ""))

        def _command2():
            global is_space_fn_mode
            global space_fn_key_oneshot

            space_fn_key_oneshot = False

            # fc.space_fn_key から押した場合
            if fakeymacs.last_keys[1] == user0_key:
                is_space_fn_mode = True

            # fc.space_fn_key 以外のモディファイアキーから押した場合
            elif user0_key in fakeymacs.last_keys[1]:
                is_space_fn_mode = False

            # 上記のどちらかの状態の継続
            else:
                pass

            # print(time.time() - space_fn_key_down_time)

            if is_space_fn_mode:
                if not fc.space_fn_use_oneshot_function:
                    _command1()

                elif time.time() - space_fn_key_down_time >= fc.space_fn_delay_seconds:
                    if space_fn_key_output:
                        if fakeymacs.last_keys[1] == user0_key:
                            space_fn_key_action()
                    _command1()
                else:
                    space_fn_key_action()
                    func()
                    is_space_fn_mode = False
            else:
                func()

        define_key(window_keymap, keys, _command2)
    else:
        define_key(window_keymap, keys1, _command1)

def replicate_key(window_keymap, key, original_key):
    define_key_fn(window_keymap, key, getKeyAction(original_key))

def replace_space_fn_key(replace):
    if replace:
        keymap.replaceKey(fc.space_fn_key, user0_key)
    else:
        keymap.replaceKey(fc.space_fn_key, fc.space_fn_key)

    return False

keymap_space_fn = keymap.defineWindowKeymap(check_func=lambda wnd: replace_space_fn_key(False))
keymap.window_keymap_list.remove(keymap_space_fn)
keymap.window_keymap_list.insert(0, keymap_space_fn)

for window_keymap in fc.space_fn_window_keymap_list:
    window_keymap.applying_func = lambda: replace_space_fn_key(True)

# すべてのキーマップに対し、fc.space_fn_key を使うキーに割り当てられている設定を user0_key を使うキーに設定する
for window_keymap in keymap.window_keymap_list:
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod   = mod1 + mod2 + mod3 + mod4
        mkey0 = mod + fc.space_fn_key
        mkey1 = mod + user0_key
        func = getKeyCommand(window_keymap,  mkey0)
        if func:
            define_key(window_keymap, mkey1, space_fn_command(func))

# keymap_base キーマップに対し、fc.space_fn_key を使う全てのキーの入力パターンを user0_key を使うキーに設定する
for mod1, mod2, mod3, mod4 in itertools.product(["", "LW-", "RW-"], ["", "LA-", "RA-"],
                                                ["", "LC-", "RC-"], ["", "S-"]):
    mod   = mod1 + mod2 + mod3 + mod4
    mkey0 = mod + fc.space_fn_key
    mkey1 = mod + user0_key
    if not getKeyCommand(keymap_base,  mkey1):
        define_key(keymap_base, mkey1, space_fn_command(self_insert_command(mkey0)))

# keymap_base キーマップに対し、全てのキーの入力パターンを SpaceFN 用のモディファイアキーを使うキーに設定する
for vkey in vkeys():
    key = vkToStr(vkey)
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod   = mod1 + mod2 + mod3 + mod4
        mkey0 =         mod + key
        mkey1 = "U0-" + mod + key
        define_key_fn(keymap_base, mkey1, self_insert_command(mkey0))

# SpaceFN を使うキーマップに対し、key rollover の対策を行う
for window_keymap in fc.space_fn_window_keymap_list:
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod in ["", "S-"]:
            mkey0 =         mod + key
            mkey1 = "U0-" + mod + key
            define_key_fn(window_keymap, mkey1, self_insert_command(mkey0), True)

    define_key(window_keymap, user0_key, space_fn_key_down)
    if fc.space_fn_use_oneshot_function:
        define_key(window_keymap, "U-" + user0_key, space_fn_key_up)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
