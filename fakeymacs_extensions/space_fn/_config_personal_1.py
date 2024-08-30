# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、Ctrl キー、Alt キー、Win キーとの組み合わせも含め、できるだけ完全なキーの
# 複製を行うバージョンです。

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
        for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
            mod   = mod1 + mod2 + mod3 + mod4
            mkey0 =         mod + key0
            mkey1 = "U0-" + mod + key1
            replicate_key(window_keymap, mkey1, mkey0)

    # ファンクションキーの設定
    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mod = "U0-" + mod1 + mod2 + mod3 + mod4

        for i in range(10):
            define_key_fn(window_keymap,
                          mod + f"{(i + 1) % 10}", self_insert_command(mod + vkToStr(VK_F1 + i)))

        define_key_fn(window_keymap, mod + "-", self_insert_command(mod + vkToStr(VK_F11)))

        if is_japanese_keyboard:
            define_key_fn(window_keymap, mod + "^", self_insert_command(mod + vkToStr(VK_F12)))
        else:
            define_key_fn(window_keymap, mod + "=", self_insert_command(mod + vkToStr(VK_F12)))

# --------------------------------------------------------------------------------------------------
