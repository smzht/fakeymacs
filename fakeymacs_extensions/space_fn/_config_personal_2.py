# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、次のページの設定に準拠しています。
# https://martin-stone.github.io/touchcursor/help.html

# 本サンプルコードは、キー単体と Shift キーの組み合わせのみのキーの複製を行うバージョンです。
# （ファンクションキーの設定は、_config_personal_1.py と同様、すべてのモディファイアキーと
#   組合せたキーの複製を行なう設定としています。）

# --------------------------------------------------------------------------------------------------

for window_keymap in fc.space_fn_window_keymap_list:

    # SpaceFN 主要キーの設定
    for key1, key0 in [["j",    "Left"],
                       ["l",    "Right"],
                       ["i",    "Up"],
                       ["k",    "Down"],
                       ["u",    "Home"],
                       ["o",    "End"],
                       ["h",    "PageUp"],
                       ["n",    "PageDown"],
                       ["Esc",  "`"],
                       ["Back", "Delete"],
                       ["p",    "PrintScreen"],
                       ["[",    "ScrollLock"],
                       ["]",    "Pause"],
                       ["\\",   "Insert"],
                       ["b",    "Space"],
                       ["/",    "Apps"],
                       ]:
        for mod in ["", "S-"]:
            mkey0 =         mod + key0
            mkey1 = "U0-" + mod + key1
            replicate_key(window_keymap, mkey1, mkey0)

    # ファンクションキーの設定
    for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"]):
        mod   = mod1 + mod2 + mod3

        mkey0 =         mod
        mkey1 = "U0-" + mod
        for i in range(10):
            define_key_fn(window_keymap,
                          mkey1 + f"{(i + 1) % 10}", self_insert_command(mkey0 + vkToStr(VK_F1 + i)))

        define_key_fn(window_keymap, mkey1 + "-", self_insert_command(mkey0 + vkToStr(VK_F11)))

        if is_japanese_keyboard:
            define_key_fn(window_keymap, mkey1 + "^", self_insert_command(mkey0 + vkToStr(VK_F12)))
        else:
            define_key_fn(window_keymap, mkey1 + "=", self_insert_command(mkey0 + vkToStr(VK_F12)))

        mkey0 =           mod
        mkey1 = "U0-S-" + mod
        for i in range(10):
            define_key_fn(window_keymap,
                          mkey1 + f"{(i + 1) % 10}", self_insert_command(mkey0 + vkToStr(VK_F13 + i)))

        define_key_fn(window_keymap, mkey1 + "-", self_insert_command(mkey0 + vkToStr(VK_F23)))

        if is_japanese_keyboard:
            define_key_fn(window_keymap, mkey1 + "^", self_insert_command(mkey0 + vkToStr(VK_F24)))
        else:
            define_key_fn(window_keymap, mkey1 + "=", self_insert_command(mkey0 + vkToStr(VK_F24)))

# --------------------------------------------------------------------------------------------------
