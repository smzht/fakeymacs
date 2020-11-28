# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Chrome 系ブラウザで Ctrl-x C-b を入力した際、Chrome の拡張機能 Quick Tabs を起動する
####################################################################################################

try:
    # 設定されているか？
    fc.chrome_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.chrome_list= ["chrome.exe",
                     "msedge.exe"]

def list_buffers(window_keymap, keys):
    # 新規に実行する関数を定義する
    func1 = reset_search(reset_undo(reset_counter(reset_mark(self_insert_command3("C-e")))))

    # 以前に定義した関数を抽出する
    func2 = keyFunc(window_keymap, keys)

    def _func():
        if keymap.getWindow().getProcessName() in fc.chrome_list:
            func1()
        else:
            func2()
    return _func

define_key(keymap_emacs, "Ctl-x C-b", list_buffers(keymap_emacs, "Ctl-x C-b"))
