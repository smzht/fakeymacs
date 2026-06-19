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
    fc.space_fn_window_keymap_list = [keymap_emacs]
    fc.space_fn_window_keymap_list += [keymap_ime]
    fc.space_fn_window_keymap_list += [keymap_lw]

try:
    # 設定されているか？
    fc.space_fn_use_oneshot_function
except:
    # SpaceFN 用のモディファイアキーの単押しで、元のキーの機能を利用するかどうかを指定する
    # （True: 使う、False: 使わない）
    fc.space_fn_use_oneshot_function = True

try:
    # 設定されているか？
    fc.space_fn_use_repeat_function
except:
    # SpaceFN 用のモディファイアキーの長押しで、元のキーのリピート入力を行うかどうかを指定する
    # （1: 単押し無しでも行う、2: 一度単押しした後であれば行う、3: 行わない）
    fc.space_fn_use_repeat_function = 2

try:
    # 設定されているか？
    fc.space_fn_function_time1
except:
    # SpaceFN 用のモディファイアキーが押されてから次のキーが押されるまでの時間で、SpaceFN の機能が
    # 必ず働くようになるまでの時間を秒数で指定する
    fc.space_fn_function_time1 = 0.2

try:
    # 設定されているか？
    fc.space_fn_function_time2
except:
    # SpaceFN 用のモディファイアキーと別なキーが同時に押された場合、最後のキーが押されてから
    # 一定時間内に SpaceFN 用のモディファイアキーが離されたときは押されたキーをそのまま入力する
    # 仕様としており、その時間を秒数で指定する
    fc.space_fn_function_time2 = 0.1

# --------------------------------------------------------------------------------------------------

user_key = "(200)"
space_fn_key_action = getKeyAction(fc.space_fn_key)

keymap.defineModifier(user_key, "User0")

class FakeymacsSpaceFN:
    pass

fakeymacs_spacefn = FakeymacsSpaceFN()

fakeymacs_spacefn.is_space_fn_mode = False
fakeymacs_spacefn.function_time1 = fc.space_fn_function_time1
fakeymacs_spacefn.fn_key_oneshot = False
fakeymacs_spacefn.fn_key_repeat = False
fakeymacs_spacefn.fn_key_down_time = 0
fakeymacs_spacefn.fn_key_up_time = 0
fakeymacs_spacefn.fn_key_output = False
fakeymacs_spacefn.fn_key_replacement = False

def space_fn_key_down():
    fakeymacs_spacefn.function_time1 = fc.space_fn_function_time1
    fakeymacs_spacefn.fn_key_oneshot = True
    fakeymacs_spacefn.fn_key_down_time = time.time()
    fakeymacs_spacefn.fn_key_output = False

    if (fc.space_fn_use_repeat_function == 1 or
        (fc.space_fn_use_repeat_function == 2 and
         fakeymacs.last_keys[1] == "U-" + user_key and
         (time.time() - fakeymacs_spacefn.fn_key_up_time) < fc.space_fn_function_time1)):
        fakeymacs_spacefn.fn_key_repeat = True
    else:
        fakeymacs_spacefn.fn_key_repeat = False

fakeymacs.space_fn_key_up = False

def space_fn_key_up():
    fakeymacs_spacefn.fn_key_down_time = 0
    if fakeymacs_spacefn.fn_key_oneshot:
        fakeymacs.space_fn_key_up = True
        space_fn_key_action()
        fakeymacs.space_fn_key_up = False
        fakeymacs_spacefn.fn_key_up_time = time.time()

def space_fn_key_repeat():
    if fakeymacs_spacefn.fn_key_oneshot:
        if fakeymacs_spacefn.fn_key_repeat:
            space_fn_command(space_fn_key_action)()
    else:
        space_fn_key_action()

def space_fn_command(func):
    def _func():
        fakeymacs_spacefn.fn_key_oneshot = False
        func()
    return _func

def execute_delayed_command():
    if fakeymacs.delayed_command:
        _command = fakeymacs.delayed_command
        fakeymacs.delayed_command = None
        _command()

def define_key_fn(window_keymap, keys, command, space_fn_key_output=False):
    key_list = kbd(keys)[0]

    if "U0-" not in key_list[0]:
        return

    keys1 = keys.replace("U0-", "RU0-", 1)

    if callable(command):
        _command1 = command
    else:
        define_key(window_keymap, keys1, command)
        _command1 = lambda: keymap.enterMultiStroke(command)

    if len(key_list) == 1:
        func = getKeyAction(keys.replace("U0-", ""))

        def _command2():
            # fc.space_fn_key から押した場合で fc.space_fn_key のリピート入力がされていない場合
            if (fakeymacs.last_keys[1] in [user_key, "U0-" + user_key] and
                fakeymacs_spacefn.fn_key_oneshot):
                fakeymacs_spacefn.is_space_fn_mode = True

            # fc.space_fn_key 以外のモディファイアキーから押した場合
            elif user_key in fakeymacs.last_keys[1]:
                fakeymacs_spacefn.is_space_fn_mode = False

            # 上記のどちらかの状態の継続
            else:
                pass

            fakeymacs_spacefn.fn_key_oneshot = False

            def _command3():
                if fakeymacs_spacefn.fn_key_down_time == 0:
                    space_fn_key_action()
                    func()
                else:
                    if not fakeymacs_spacefn.fn_key_output:
                        if space_fn_key_output:
                            space_fn_key_action()
                        fakeymacs_spacefn.fn_key_output = True
                    _command1()

            if fakeymacs_spacefn.is_space_fn_mode:
                if not fc.space_fn_use_oneshot_function:
                    _command1()

                elif (time.time() - fakeymacs_spacefn.fn_key_down_time) < fakeymacs_spacefn.function_time1:
                    fakeymacs.delayed_command = _command3
                    keymap.delayedCall(execute_delayed_command, int(fc.space_fn_function_time2 * 1000))
                    fakeymacs_spacefn.function_time1 = 0
                else:
                    _command3()
            else:
                func()

        define_key(window_keymap, keys, _command2)
    else:
        define_key(window_keymap, keys1, _command1)

def replicate_key(window_keymap, key, original_key):
    define_key_fn(window_keymap, key, getKeyAction(original_key))

def set_space_fn_key_replacement(replace):
    fakeymacs.space_fn_key_replacement = replace
    return False

def replace_space_fn_key(window):
    if fakeymacs.is_base_target and fakeymacs.space_fn_key_replacement:
        if not fakeymacs_spacefn.fn_key_replacement:
            keymap.replaceKey(fc.space_fn_key, user_key)
            fakeymacs_spacefn.fn_key_replacement = True
    else:
        if fakeymacs_spacefn.fn_key_replacement:
            keymap.modifier &= ~keyhac_keymap.MODKEY_USER0_L
            keymap.replaceKey(fc.space_fn_key, fc.space_fn_key)
            fakeymacs_spacefn.fn_key_replacement = False
    return False

keymap_spacefn1 = keymap.defineWindowKeymap(check_func=lambda wnd: set_space_fn_key_replacement(False))
keymap.window_keymap_list.remove(keymap_spacefn1)
keymap.window_keymap_list.insert(0, keymap_spacefn1)
keymap_spacefn2 = keymap.defineWindowKeymap(check_func=lambda wnd: replace_space_fn_key(wnd))

def applying_func(func):
    def _func():
        func()
        set_space_fn_key_replacement(True)
    return _func

for window_keymap in fc.space_fn_window_keymap_list:
    if window_keymap.applying_func:
        window_keymap.applying_func = applying_func(window_keymap.applying_func)
    else:
        window_keymap.applying_func = lambda: set_space_fn_key_replacement(True)

# すべてのキーマップに対し、fc.space_fn_key を使うキーに割り当てられている設定を user_key を使うキーに設定する
for window_keymap in keymap.window_keymap_list:
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod   = mod1 + mod2 + mod3 + mod4
        mkey0 = mod + fc.space_fn_key
        mkey1 = mod + user_key
        func = getKeyCommand(window_keymap, mkey0)
        if func:
            define_key(window_keymap, mkey1, space_fn_command(func))

# keymap_base キーマップに対し、fc.space_fn_key を使う全てのキーの入力パターンを user_key を使うキーに設定する
for mod1, mod2, mod3, mod4 in itertools.product(["", "LW-", "RW-"], ["", "LA-", "RA-"],
                                                ["", "LC-", "RC-"], ["", "S-"]):
    mod   = mod1 + mod2 + mod3 + mod4
    mkey0 = mod + fc.space_fn_key
    mkey1 = mod + user_key
    if not getKeyCommand(keymap_base, mkey1):
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

    define_key(window_keymap, user_key, space_fn_key_down)
    if fc.space_fn_use_oneshot_function:
        define_key(window_keymap, "U-" + user_key, space_fn_key_up)
        if fc.space_fn_use_repeat_function != 3:
            define_key(window_keymap, "U0-" + user_key, space_fn_key_repeat)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
