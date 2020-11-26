# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Chrome 系ブラウザで Ctrl-x C-b を入力した際、Chrome の拡張機能 Quick Tabs を起動する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe"]

def list_buffers(func=list_buffers):
    if keymap.getWindow().getProcessName() in fc.browser_list:
        self_insert_command3("C-e")()
    else:
        func()

define_key(keymap_emacs, "Ctl-x C-b", reset_search(reset_undo(reset_counter(reset_mark(list_buffers)))))
