# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ２つのディスプレイに表示されているウィンドウを入れ替えるキーを指定する
####################################################################################################

try:
    # 設定されているか？
    fc.transpose_windows_key
except:
    # Everything を起動するキーを指定する
    fc.transpose_windows_key = "A-t"

def transpose_windows():
    move_window_to_next_display()
    other_window()
    delay()
    move_window_to_previous_display()

define_key(keymap_global, fc.transpose_windows_key, transpose_windows)
