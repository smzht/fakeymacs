# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## C-Enter に F2（編集モード移行）を割り当てる
####################################################################################################

fc.edit_mode_target = [["EXCEL.EXE",    "EXCEL*"],
                       ["explorer.exe", "DirectUIHWND"]]

def is_edit_mode_target(window):
    for processName, className in fc.edit_mode_target:
        if checkWindow(processName, className, window):
            return True
    return False

keymap_edit_mode = keymap.defineWindowKeymap(check_func=is_edit_mode_target)

define_key(keymap_edit_mode, "C-Enter", self_insert_command("F2"))
