# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## CapsLock キーを Ctrl キーとして使うための設定を行う
####################################################################################################

user2_vkey = 236 # リモートデスクトップ接続先に渡る仮想キーコードを選択する必要有り
user2_key = keyhac_keymap.KeyCondition.vkToStr(user2_vkey)

keymap.replaceKey("CapsLock", user2_key)
keymap.replaceKey(240, user2_key)

if os_keyboard_type == "US":
    keymap.replaceKey(241, user2_key)
    keymap.replaceKey(242, user2_key)

keymap.defineModifier(user2_key, "User2")

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
        capslockUp(shiftUp(f"U-{user2_key}"))()
        keymap.modifier &= ~keymap.vk_mod_map[user2_vkey]
    return _func

def postProcessing2(key):
     def _func():
         keymap.InputKeyCommand(key)()
         if not fakeymacs.capslock_down:
             capslockUp(shiftUp(f"U-{user2_key}"))()
             keymap.modifier &= ~keymap.vk_mod_map[user2_vkey]
     return _func

def setCapslock(window_keymap):
    if os_keyboard_type == "JP":
        window_keymap[     user2_key  ] = capslockDown(shiftDown(f"D-{user2_key}"))
        window_keymap[f"U-{user2_key}"] = capslockUp  (shiftUp  (f"U-{user2_key}"))

        window_keymap[  f"U0-{user2_key}"] = capslockDown(shiftDown(f"D-U0-{user2_key}"))
        window_keymap[f"U-U0-{user2_key}"] = capslockUp  (shiftUp  (f"U-U0-{user2_key}"))

        window_keymap["U-LShift"] = shiftUp("U-LShift") # for Remote Desktop
        window_keymap["U-RShift"] = shiftUp("U-RShift") # for Remote Desktop

        window_keymap["U-U2-LShift"] = shiftDown("U-U2-LShift")
        window_keymap["U-U2-RShift"] = shiftDown("U-U2-RShift")

        window_keymap[f"C-{user2_key}"] = "S-CapsLock" # CapsLock の切り替え
    else:
        window_keymap[     user2_key  ] = capslockDown(keymap.InputKeyCommand(f"D-{user2_key}"))
        window_keymap[f"U-{user2_key}"] = capslockUp  (keymap.InputKeyCommand(f"U-{user2_key}"))

        window_keymap[  f"U0-{user2_key}"] = capslockDown(keymap.InputKeyCommand(f"D-U0-{user2_key}"))
        window_keymap[f"U-U0-{user2_key}"] = capslockUp  (keymap.InputKeyCommand(f"U-U0-{user2_key}"))

        window_keymap["U-U2-LShift"] = postProcessing("U-U2-LShift")
        window_keymap["U-U2-RShift"] = postProcessing("U-U2-RShift")

        window_keymap[f"C-{user2_key}"] = "CapsLock" # CapsLock の切り替え

    window_keymap["U-U2-LCtrl"] = postProcessing("U-U2-LCtrl")
    window_keymap["U-U2-RCtrl"] = postProcessing("U-U2-RCtrl")
    window_keymap["U-U2-LAlt"]  = postProcessing("U-U2-LAlt")
    window_keymap["U-U2-RAlt"]  = postProcessing("U-U2-RAlt")
    window_keymap["U-U2-LWin"]  = postProcessing("U-U2-LWin")
    window_keymap["U-U2-RWin"]  = postProcessing("U-U2-RWin")
    window_keymap["U-U2-(200)"] = postProcessing2("U-U2-(200)") # for space_fn Extension

def replicateKey(window_keymap):
    for key in list(window_keymap.keymap):
        key = str(key)
        command = window_keymap[key]
        if re.search(rf"(^|-)({fc.side_of_ctrl_key}|)C-", key):
            key2 = re.sub(rf"(^|-)({fc.side_of_ctrl_key}|)C-", r"\1U2-", key)
            window_keymap[key2] = command

        if isinstance(command, keyhac_keymap.WindowKeymap):
            replicateKey(command)
            setCapslock(command)

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
        mkey = "U2-" + mod1 + mod2 + mod3 + key
        keymap_remote[mkey] = remote_command(mkey)

for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "A-"], ["", "S-"]):
    mkey = mod1 + mod2 + mod3 + user2_key
    keymap_remote[     mkey  ] = f"D-{mkey}"
    keymap_remote[f"U-{mkey}"] = f"U-{mkey}"

setCapslock(keymap_remote)
keymap_remote[f"C-{user2_key}"] = f"C-{user2_key}" # CapsLock の切り替え

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
                    if (keymap.record_seq[-1] == (user2_vkey, True) and
                        keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], True) and
                        keymap.record_seq[-3] == (ctl_x_prefix_vkey[1], False) and
                        keymap.record_seq[-4] == (user2_vkey, False)):
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
                            keymap.record_seq[-2] == (user2_vkey, True) and
                            keymap.record_seq[-3] == (VK_LSHIFT, False) and
                            keymap.record_seq[-4] == (ctl_x_prefix_vkey[1], True) and
                            keymap.record_seq[-5] == (ctl_x_prefix_vkey[1], False) and
                            keymap.record_seq[-6] == (VK_LSHIFT, True) and
                            keymap.record_seq[-7] == (VK_LSHIFT, False) and
                            keymap.record_seq[-8] == (user2_vkey, False)):
                            for _ in range(8):
                                keymap.record_seq.pop()

    define_key(keymap_emacs, "Ctl-x )", kmacro_end_macro2)
