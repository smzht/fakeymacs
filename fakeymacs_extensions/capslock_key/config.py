# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## CapsLock キーを Ctrl キーとして使うための設定を行う
####################################################################################################

user_vkey = 236 # リモートデスクトップ接続先に渡る仮想キーコードを選択する必要有り
user_key = keyhac_keymap.KeyCondition.vkToStr(user_vkey)

keymap.replaceKey("CapsLock", user_key)
keymap.replaceKey(240, user_key)

if os_keyboard_type == "US":
    keymap.replaceKey(241, user_key)
    keymap.replaceKey(242, user_key)

keymap.defineModifier(user_key, "RUser3")

fakeymacs.capslock_down = False

def capslockDown(func):
    def _func():
        func()
        fakeymacs.capslock_down = True
    return _func

def capslockUp(func):
    def _func():
        func()
        fakeymacs.capslock_down = False
    return _func

def shiftDown(key):
    def _func():
        keymap.InputKeyCommand(key)()
        keymap.InputKeyCommand("D-Shift")()
        fakeymacs.shift_down2 = True
    return _func

def shiftUp(key):
    def _func():
        keymap.InputKeyCommand(key)()
        if fakeymacs.shift_down2:
            keymap.InputKeyCommand("U-Shift")()
            fakeymacs.shift_down2 = False
    return _func

def postProcessing(key):
    def _func():
        keymap.InputKeyCommand(key)()
        capslockUp(shiftUp(f"U-{user_key}"))()
        keymap.modifier &= ~keymap.vk_mod_map[user_vkey]
    return _func

def postProcessing2(key):
     def _func():
         keymap.InputKeyCommand(key)()
         if not fakeymacs.capslock_down:
             capslockUp(shiftUp(f"U-{user_key}"))()
             keymap.modifier &= ~keymap.vk_mod_map[user_vkey]
     return _func

def setCapslock(window_keymap):
    if os_keyboard_type == "JP":
        window_keymap[     user_key  ] = capslockDown(shiftDown(f"D-{user_key}"))
        window_keymap[f"U-{user_key}"] = capslockUp  (shiftUp  (f"U-{user_key}"))

        window_keymap[  f"U0-{user_key}"] = capslockDown(shiftDown(f"D-U0-{user_key}"))
        window_keymap[f"U-U0-{user_key}"] = capslockUp  (shiftUp  (f"U-U0-{user_key}"))

        window_keymap["U-LShift"] = shiftUp("U-LShift") # for Remote Desktop
        window_keymap["U-RShift"] = shiftUp("U-RShift") # for Remote Desktop

        window_keymap["U-RU3-LShift"] = shiftDown("U-RU3-LShift")
        window_keymap["U-RU3-RShift"] = shiftDown("U-RU3-RShift")

        window_keymap[f"C-{user_key}"] = "S-CapsLock" # CapsLock の切り替え
    else:
        window_keymap[     user_key  ] = capslockDown(keymap.InputKeyCommand(f"D-{user_key}"))
        window_keymap[f"U-{user_key}"] = capslockUp  (keymap.InputKeyCommand(f"U-{user_key}"))

        window_keymap[  f"U0-{user_key}"] = capslockDown(keymap.InputKeyCommand(f"D-U0-{user_key}"))
        window_keymap[f"U-U0-{user_key}"] = capslockUp  (keymap.InputKeyCommand(f"U-U0-{user_key}"))

        window_keymap["U-RU3-LShift"] = postProcessing("U-RU3-LShift")
        window_keymap["U-RU3-RShift"] = postProcessing("U-RU3-RShift")

        window_keymap[f"C-{user_key}"] = "CapsLock" # CapsLock の切り替え

    window_keymap["U-RU3-LCtrl"] = postProcessing("U-RU3-LCtrl")
    window_keymap["U-RU3-RCtrl"] = postProcessing("U-RU3-RCtrl")
    window_keymap["U-RU3-LAlt"]  = postProcessing("U-RU3-LAlt")
    window_keymap["U-RU3-RAlt"]  = postProcessing("U-RU3-RAlt")
    window_keymap["U-RU3-LWin"]  = postProcessing("U-RU3-LWin")
    window_keymap["U-RU3-RWin"]  = postProcessing("U-RU3-RWin")
    window_keymap["U-RU3-(200)"] = postProcessing2("U-RU3-(200)") # for space_fn Extension

wk_history = set()
pattern = re.compile(rf"(^|-)({fc.side_of_ctrl_key}|)C-")

def replicateKey(window_keymap):
    wk_history.add(window_keymap)

    for key in list(window_keymap.keymap):
        key = str(key)
        handler = window_keymap[key]

        if pattern.search(key):
            key2 = pattern.sub(r"\1RU3-", key)

            if type(handler) is str:
                window_keymap[key2] = InputKeyCommand(handler, usjis_conv=False)
            elif type(handler) in [list, tuple]:
                window_keymap[key2] = InputKeyCommand(*handler, usjis_conv=False)
            else:
                window_keymap[key2] = handler

        if isinstance(handler, keyhac_keymap.WindowKeymap):
            if handler not in wk_history:
                replicateKey(handler)
                setCapslock(handler)

for window_keymap in keymap.window_keymap_list:
    replicateKey(window_keymap)

setCapslock(keymap_base)

# --------------------------------------------------------------------------------------------------

keymap_remote = keymap.defineWindowKeymap(class_name="IHWindowClass")

def remote_command(key):
    def _func():
        key_list = [key]
        if fakeymacs.shift_down2:
            key_list = ["U-Shift"] + key_list + ["D-Shift"]
        keymap.InputKeyCommand(*key_list)()
    return _func

for vkey in vkeys():
    key = vkToStr(vkey)
    for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "A-"], ["", "S-"]):
        mkey = "RU3-" + mod1 + mod2 + mod3 + key
        keymap_remote[mkey] = remote_command(mkey)

for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "A-"], ["", "S-"]):
    mkey = mod1 + mod2 + mod3 + user_key
    keymap_remote[     mkey  ] = f"D-{mkey}"
    keymap_remote[f"U-{mkey}"] = f"U-{mkey}"

setCapslock(keymap_remote)
keymap_remote[f"C-{user_key}"] = f"C-{user_key}" # CapsLock の切り替え

# --------------------------------------------------------------------------------------------------

if fc.ctl_x_prefix_key and ctl_x_prefix_vkey[0] in [VK_LCONTROL, VK_RCONTROL]:
    def kmacro_end_macro2():
        kmacro_end_macro()
        if os_keyboard_type == "US":
            if len(keymap.record_seq) >= 4:
                if (((keymap.record_seq[-1] == (VK_CAPITAL, True) and
                      keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], True)) or
                     (keymap.record_seq[-1] == (ctl_x_prefix_vkey[1], True) and
                      keymap.record_seq[-2] == (VK_CAPITAL, True))) and
                    keymap.record_seq[-3] == (ctl_x_prefix_vkey[1], False)):
                    for _ in range(3):
                        keymap.record_seq.pop()
                    if keymap.record_seq[-1] == (VK_CAPITAL, False):
                        for i in range(len(keymap.record_seq) - 1, -1, -1):
                            if keymap.record_seq[i] == (VK_CAPITAL, False):
                                keymap.record_seq.pop()
                            else:
                                break
                    else:
                        # CapsLock の入力が連続して行われる場合があるための対処
                        keymap.record_seq.append((VK_CAPITAL, True))
                else:
                    # Remote Desktop を利用する場合の対策
                    if (keymap.record_seq[-1] == (user_vkey, True) and
                        keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], True) and
                        keymap.record_seq[-3] == (ctl_x_prefix_vkey[1], False) and
                        keymap.record_seq[-4] == (user_vkey, False)):
                        for _ in range(4):
                            keymap.record_seq.pop()
        else:
            if len(keymap.record_seq) >= 2:
                if keymap.record_seq[-1] == (VK_CAPITAL, True):
                    keymap.record_seq.pop()
                if (keymap.record_seq[-1] == (ctl_x_prefix_vkey[1], True) and
                    keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], False)):
                    for _ in range(2):
                        keymap.record_seq.pop()
                    for i in range(len(keymap.record_seq) - 1, -1, -1):
                        if keymap.record_seq[i] == (VK_CAPITAL, False):
                            keymap.record_seq.pop()
                        else:
                            break
                else:
                    # Remote Desktop を利用する場合の対策
                    if len(keymap.record_seq) >= 8:
                        if (keymap.record_seq[-1] == (VK_LSHIFT, True) and
                            keymap.record_seq[-2] == (user_vkey, True) and
                            keymap.record_seq[-3] == (VK_LSHIFT, False) and
                            keymap.record_seq[-4] == (ctl_x_prefix_vkey[1], True) and
                            keymap.record_seq[-5] == (ctl_x_prefix_vkey[1], False) and
                            keymap.record_seq[-6] == (VK_LSHIFT, True) and
                            keymap.record_seq[-7] == (VK_LSHIFT, False) and
                            keymap.record_seq[-8] == (user_vkey, False)):
                            for _ in range(8):
                                keymap.record_seq.pop()

    define_key(keymap_emacs, "Ctl-x )", kmacro_end_macro2)
