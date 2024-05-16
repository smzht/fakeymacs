# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## アプリでショートカットキーが設定されていないメニューコマンドにキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.menu_command_key
except:
    # 実行するアプリのリスト、メニューのコマンドID、割り当てるキーの組み合わせを指定する（複数指定可）
    fc.menu_command_key = [[["chrome.exe",
                             "msedge.exe"], 35024, "C-A-r"], # 現在のタブの右側に新たなタブを開く
                           ]

for app_list, command_id, key in fc.menu_command_key:
    define_key3(keymap_global, key,
                lambda: keymap.getWindow().postMessage(0x0111, command_id),
                lambda: keymap.getWindow().getProcessName() in app_list)
