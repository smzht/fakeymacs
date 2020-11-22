# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## chrome 系ブラウザで Ctrl-x C-b を入力した際、chrome の機能拡張 quick tabs を起動する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    fc.browser_list= ["chrome.exe",
                      "msedge.exe"]

def list_buffers(func=list_buffers):
    if (checkWindow("chrome.exe", "Chrome_WidgetWin_1") or # Chrome
        checkWindow("msedge.exe", "Chrome_WidgetWin_1")):  # MSEode
        self_insert_command3("C-e")()
    else:
        func()

define_key(keymap_emacs, "Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))
