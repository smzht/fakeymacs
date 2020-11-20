# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザ向けのキー C-l、C-t を発行した際、IME を disable する処理を追加する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    fc.browser_list= ["chrome.exe",
                      "msedge.exe"]

def is_browser(window):
    if keymap.getWindow().getProcessName() in fc.browser_list:
        return True
    else:
        return False

keymap_browser = keymap.defineWindowKeymap(check_func=is_browser)

def self_insert_command3(*keys):
    func = self_insert_command(*keys)
    def _func():
        func()
        disable_input_method()
    return _func

define_key(keymap_browser, "C-l", self_insert_command3("C-l"))
define_key(keymap_browser, "C-t", self_insert_command3("C-t"))
