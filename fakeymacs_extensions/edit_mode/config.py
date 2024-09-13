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
    # 本機能を割り当てるアプリケーションソフトを指定する
    fc.edit_mode_target = [["EXCEL.EXE",    "EXCEL*",       "?*"],
                           ["explorer.exe", "DirectUIHWND", None]]

# --------------------------------------------------------------------------------------------------

def is_edit_mode_target(window):
    for process_name, class_name, text in fc.edit_mode_target:
        if checkWindow(process_name, class_name, text, window):
            return True
    return False

keymap_edit_mode = keymap.defineWindowKeymap(check_func=is_edit_mode_target)

define_key(keymap_edit_mode, fc.edit_mode_key, self_insert_command("F2"))
