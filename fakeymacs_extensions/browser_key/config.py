# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザ向けのキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe"]

## ブラウザ向けのキー C-l、C-t を入力した際、IME を disable する処理を追加する

def is_browser(window):
    if keymap.getWindow().getProcessName() in fc.browser_list:
        return True
    else:
        return False

keymap_browser = keymap.defineWindowKeymap(check_func=is_browser)

define_key(keymap_browser, "C-l", self_insert_command3("C-l"))
define_key(keymap_browser, "C-t", self_insert_command3("C-t"))

## C-A-l、C-A-t を入力した際、ブラウザをポップアップしてから C-l、C-t の機能を実行する

def browser_popup(key):
    def _func():
        for window in getWindowList():
            if window.getProcessName() in fc.browser_list:
                popWindow(window)()
                keymap.delayedCall(self_insert_command3(key), 100)
                return

        # fc.browser_list に定義するブラウザが起動していない場合、fc.browser_list の最初
        # に定義するブラウザを起動する
        keymap.ShellExecuteCommand(None, fc.browser_list[0], "", "")()

    return _func

define_key(keymap_global, "C-A-l", browser_popup("C-l"))
define_key(keymap_global, "C-A-t", browser_popup("C-t"))
