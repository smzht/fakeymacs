# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## SpaceFn を実現する設定を行う
####################################################################################################

keymap.replaceKey("Space", 200)
keymap.defineModifier(200, "User0")

for keymap_i in keymap.window_keymap_list:
    for mod1, mod2, mod3, mod4 in itertools.product(["", "LW-", "RW-"],  ["", "LA-", "RA-"],
                                                    ["", "LC-", "RC-"],  ["", "S-"]):
        mod   = mod1 + mod2 + mod3 + mod4
        mkey0 = mod + "Space"
        mkey1 = mod + "O-(200)"
        mkey2 = mod + "(200)"

        if keymap_i is keymap_emacs and mod in ["", "S-"]:
            # keymap_base で mkey2 がキャッチされるのを防ぐ対策
            define_key(keymap_i, mkey2, lambda: None)

            mkey = mkey1
        else:
            mkey = mkey2

        func = getKeyCommand(keymap_i, mkey0)
        if func:
            define_key(keymap_i, mkey, func)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
