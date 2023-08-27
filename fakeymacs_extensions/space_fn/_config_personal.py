# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、次のページの設定に準拠しています。
# https://martin-stone.github.io/touchcursor/help.html

# --------------------------------------------------------------------------------------------------

for window_keymap in fc.space_fn_window_keymap_list:

    # スペースを連続して入力するためのキーの設定
    replicate_key(window_keymap, "U0-s", "O-Space")

    # 「カーソル移動」のキー設定
    replicate_key(window_keymap, "U0-j", "Left")
    replicate_key(window_keymap, "U0-l", "Right")
    replicate_key(window_keymap, "U0-i", "Up")
    replicate_key(window_keymap, "U0-k", "Down")

    replicate_key(window_keymap, "U0-S-j", "S-Left")
    replicate_key(window_keymap, "U0-S-l", "S-Right")
    replicate_key(window_keymap, "U0-S-i", "S-Up")
    replicate_key(window_keymap, "U0-S-k", "S-Down")

    replicate_key(window_keymap, "U0-u", "Home")
    replicate_key(window_keymap, "U0-o", "End")

    # 「カット / コピー / 削除 / アンドゥ」のキー設定
    replicate_key(window_keymap, "U0-p", "Back")
    replicate_key(window_keymap, "U0-m", "Delete")

    # 「スクロール」のキー設定
    replicate_key(window_keymap, "U0-h", "PageUp")
    replicate_key(window_keymap, "U0-n", "PageDown")

    # ファンクションキーの設定
    for i in range(10):
        define_key(window_keymap, f"U0-{(i + 1) % 10}", self_insert_command(vkToStr(VK_F1 + i)))

    define_key(window_keymap, "U0--", self_insert_command(vkToStr(VK_F11)))

    if is_japanese_keyboard:
        define_key(window_keymap, "U0-^", self_insert_command(vkToStr(VK_F12)))
    else:
        define_key(window_keymap, "U0-=", self_insert_command(vkToStr(VK_F12)))

# --------------------------------------------------------------------------------------------------
