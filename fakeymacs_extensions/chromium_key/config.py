# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## chromium 系ブラウザでショートカットキーが設定されていないメニューコマンドにキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.chromium_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.chromium_list = ["chrome.exe",
                        "msedge.exe"]

try:
    # 設定されているか？
    fc.chromium_command
except:
    # chromium 系ブラウザで実行するコマンドID とキーの組み合わせを指定する（複数指定可）
    fc.chromium_command = [[35024, "C-A-r"], # 現在のタブの右側に新たなタブを開く
                           ]

# chromium 系ブラウザのメニューコマンドの ID は、次のページで確認できます
# https://chromium.googlesource.com/chromium/src/+/HEAD/chrome/app/chrome_command_ids.h

for command_id, key in fc.chromium_command:
    define_key3(keymap_global, key,
                lambda: keymap.getWindow().postMessage(0x0111, command_id),
                lambda: keymap.getWindow().getProcessName() in fc.chromium_list)
