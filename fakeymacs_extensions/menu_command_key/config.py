# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## アプリでショートカットキーが設定されていないメニューコマンドにキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.menu_command_key
except:
    # 実行するアプリ、メニューのコマンドID、割り当てるキーの組み合わせを指定する（複数指定可）
    fc.menu_command_key = [["chrome.exe", 35024, "C-A-r"], # 現在のタブの右隣に新しいタブを開く
                           ["msedge.exe", 35024, "C-A-r"], # 現在のタブの右隣に新しいタブを開く
                           ]

# --------------------------------------------------------------------------------------------------

for process_name, command_id, key in fc.menu_command_key:
    define_key3(keymap_global, key,
                lambda x=command_id:   keymap.getWindow().postMessage(0x0111, x),
                lambda x=process_name: getProcessName() == x)
