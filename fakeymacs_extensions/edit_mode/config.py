# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 指定したアプリケーションソフトに F2（編集モード移行）を割り当てるキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.edit_mode_key
except:
    # F2（編集モード移行）を割り当てるキーを指定する
    fc.edit_mode_key = "C-Enter"

try:
    # 設定されているか？
    fc.edit_mode_target
except:
    # 本機能を割り当てるアプリケーションソフト（プロセス名称、クラス名称、ウィンドウタイトルのリスト
    # （ワイルドカード指定可、リストの後ろの項目から省略可））を指定する
    fc.edit_mode_target = [["EXCEL.EXE",    "EXCEL*",       "?*"],
                           ["explorer.exe", "DirectUIHWND"],
                           ]

# --------------------------------------------------------------------------------------------------

def is_edit_mode_target(window):
    global edit_mode_target_status

    if window is not fakeymacs.last_window:
        if any(checkWindow(*app, window=window) for app in fc.edit_mode_target):
            edit_mode_target_status = True
        else:
            edit_mode_target_status = False

    return edit_mode_target_status

keymap_edit_mode = keymap.defineWindowKeymap(check_func=is_edit_mode_target)

define_key(keymap_edit_mode, fc.edit_mode_key, self_insert_command("F2"))
