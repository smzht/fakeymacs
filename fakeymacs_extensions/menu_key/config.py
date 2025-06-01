# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Emacs キーバインドを利用しない設定のアプリで、メニューの操作用の Emacs キーバインドを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.menu_target
except:
    # 本機能を適用するアプリのプログラム名称を指定する
    fc.menu_target= ["ttermpro.exe", # TeraTerm
                     ]

# --------------------------------------------------------------------------------------------------

def is_menu_target(window):
    global menu_target_status

    if window is not fakeymacs.last_window or fakeymacs.force_update:
        if (fakeymacs.is_emacs_target == False and
            window.getProcessName() in fc.menu_target):
            menu_target_status = True
        else:
            menu_target_status = False

    return menu_target_status

keymap_menu = keymap.defineWindowKeymap(check_func=is_menu_target)

def is_menu():
    window = Window.find("#32768", None)
    if window and window.getOwner() == keymap.getWindow():
        return True
    else:
        return False

def define_key_m(keys, command):
    define_key(keymap_menu, keys, makeKeyCommand(keymap_base, keys, command, is_menu))

define_key_m("C-[", escape)
define_key_m("C-b", backward_char)
define_key_m("C-f", forward_char)
define_key_m("C-p", previous_line)
define_key_m("C-n", next_line)
define_key_m("C-m", newline)
define_key_m("C-g", escape)
