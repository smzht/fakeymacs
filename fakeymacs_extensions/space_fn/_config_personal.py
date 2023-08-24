# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで space_fn Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# 本サンプルコードは、次のページの設定に準拠しています。
# https://martin-stone.github.io/touchcursor/help.html

# --------------------------------------------------------------------------------------------------

def define_key_f(keys, command):
    define_key(keymap_emacs, keys, command)

# スペースを連続して入力するためのキーの設定
define_key_f("U0-s", reset_undo(reset_counter(reset_mark(repeat(space)))))

# 「カーソル移動」のキー設定
define_key_f("U0-j", reset_search(reset_undo(reset_counter(mark(repeat(backward_char), False)))))
define_key_f("U0-l", reset_search(reset_undo(reset_counter(mark(repeat(forward_char), True)))))
define_key_f("U0-i", reset_search(reset_undo(reset_counter(mark(repeat(previous_line), False)))))
define_key_f("U0-k", reset_search(reset_undo(reset_counter(mark(repeat(next_line), True)))))

define_key_f("S-U0-j", reset_search(reset_undo(reset_counter(mark2(repeat(backward_char), False)))))
define_key_f("S-U0-l", reset_search(reset_undo(reset_counter(mark2(repeat(forward_char), True)))))
define_key_f("S-U0-i", reset_search(reset_undo(reset_counter(mark2(repeat(previous_line), False)))))
define_key_f("S-U0-k", reset_search(reset_undo(reset_counter(mark2(repeat(next_line), True)))))

define_key_f("U0-u", reset_search(reset_undo(reset_counter(mark(move_beginning_of_line, False)))))
define_key_f("U0-o", reset_search(reset_undo(reset_counter(mark(move_end_of_line, True)))))

# 「カット / コピー / 削除 / アンドゥ」のキー設定
define_key_f("U0-p", reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_backward_char))))))
define_key_f("U0-m", reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_char))))))

# 「スクロール」のキー設定
define_key_f("U0-h", reset_search(reset_undo(reset_counter(mark(scroll_up, False)))))
define_key_f("U0-n", reset_search(reset_undo(reset_counter(mark(scroll_down, True)))))

# ファンクションキーの設定
for i in range(10):
    define_key_f(f"U0-{(i + 1) % 10}", self_insert_command(vkToStr(VK_F1 + i)))

define_key_f("U0--", self_insert_command(vkToStr(VK_F11)))

if is_japanese_keyboard:
    define_key_f("U0-^", self_insert_command(vkToStr(VK_F12)))
else:
    define_key_f("U0-=", self_insert_command(vkToStr(VK_F12)))

# --------------------------------------------------------------------------------------------------
