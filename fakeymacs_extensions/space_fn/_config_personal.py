# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、次のページの設定に準拠しています。
# https://martin-stone.github.io/touchcursor/help.html

# モディファイアキーは、U0- と S- のみが利用できます。

# --------------------------------------------------------------------------------------------------

# スペースを連続して入力するためのキーの設定
replicate_key("U0-s", "Space")

# 「カーソル移動」のキー設定
replicate_key("U0-j", "Left")
replicate_key("U0-l", "Right")
replicate_key("U0-i", "Up")
replicate_key("U0-k", "Down")

replicate_key("U0-S-j", "S-Left")
replicate_key("U0-S-l", "S-Right")
replicate_key("U0-S-i", "S-Up")
replicate_key("U0-S-k", "S-Down")

replicate_key("U0-u", "Home")
replicate_key("U0-o", "End")

# 「カット / コピー / 削除 / アンドゥ」のキー設定
replicate_key("U0-p", "Back")
replicate_key("U0-m", "Delete")

# 「スクロール」のキー設定
replicate_key("U0-h", "PageUp")
replicate_key("U0-n", "PageDown")

# ファンクションキーの設定
for i in range(10):
    replicate_key(f"U0-{(i + 1) % 10}", self_insert_command(vkToStr(VK_F1 + i)))

replicate_key("U0--", self_insert_command(vkToStr(VK_F11)))

if is_japanese_keyboard:
    replicate_key("U0-^", self_insert_command(vkToStr(VK_F12)))
else:
    replicate_key("U0-=", self_insert_command(vkToStr(VK_F12)))

# --------------------------------------------------------------------------------------------------
