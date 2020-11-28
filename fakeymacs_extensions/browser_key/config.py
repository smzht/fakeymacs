# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザ向けのキー C-l、C-t を入力した際、IME を disable する処理を追加する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe"]

def is_browser(window):
    if keymap.getWindow().getProcessName() in fc.browser_list:
        return True
    else:
        return False

keymap_browser = keymap.defineWindowKeymap(check_func=is_browser)

define_key(keymap_browser, "C-l", self_insert_command3("C-l"))
define_key(keymap_browser, "C-t", self_insert_command3("C-t"))
