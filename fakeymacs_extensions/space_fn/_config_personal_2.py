# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、次のページの設定に準拠しています。
# https://martin-stone.github.io/touchcursor/help.html

# 本サンプルコードは、キー単体と Shift キーの組み合わせのみのキーの複製を行うバージョンです。

# --------------------------------------------------------------------------------------------------

for window_keymap in fc.space_fn_window_keymap_list:

    # スペースを連続して入力するためのキーの設定
    replicate_key(window_keymap, "U0-s", "Space")

    # キーの複製
    for key1, key0 in [["j", "Left"],
                       ["l", "Right"],
                       ["i", "Up"],
                       ["k", "Down"],
                       ["u", "Home"],
                       ["o", "End"],
                       ["y", "Insert"],
                       ["p", "Back"],
                       ["m", "Delete"],
                       ["h", "PageUp"],
                       ["n", "PageDown"],
                       ]:
        for mod in ["", "S-"]:
            mkey0 =         mod + key0
            mkey1 = "U0-" + mod + key1
            replicate_key(window_keymap, mkey1, mkey0)

    # ファンクションキーの設定
    mkey = "U0-"
    for i in range(10):
        define_key_fn(window_keymap,
                      mkey + f"{(i + 1) % 10}", self_insert_command(vkToStr(VK_F1 + i)))

    define_key_fn(window_keymap, mkey + "-", self_insert_command(vkToStr(VK_F11)))

    if is_japanese_keyboard:
        define_key_fn(window_keymap, mkey + "^", self_insert_command(vkToStr(VK_F12)))
    else:
        define_key_fn(window_keymap, mkey + "=", self_insert_command(vkToStr(VK_F12)))

    mkey = "U0-S-"
    for i in range(10):
        define_key_fn(window_keymap,
                      mkey + f"{(i + 1) % 10}", self_insert_command(vkToStr(VK_F13 + i)))

    define_key_fn(window_keymap, mkey + "-", self_insert_command(vkToStr(VK_F23)))

    if is_japanese_keyboard:
        define_key_fn(window_keymap, mkey + "^", self_insert_command(vkToStr(VK_F24)))
    else:
        define_key_fn(window_keymap, mkey + "=", self_insert_command(vkToStr(VK_F24)))

# --------------------------------------------------------------------------------------------------
