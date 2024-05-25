# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Chrome 系ブラウザで Ctl-x C-b を入力した際、Chrome の拡張機能 QuicKey を起動する
####################################################################################################

try:
    # 設定されているか？
    fc.chrome_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.chrome_list = ["chrome.exe",
                      "msedge.exe"]

try:
    # 設定されているか？
    fc.quickey_shortcut_key
except:
    # QuicKey を起動するショートカットキーを指定する
    fc.quickey_shortcut_key = "A-q"

define_key3(keymap_emacs, "Ctl-x C-b",
            reset_search(reset_undo(reset_counter(reset_mark(self_insert_command3(fc.quickey_shortcut_key))))),
            lambda: keymap.getWindow().getProcessName() in fc.chrome_list)
