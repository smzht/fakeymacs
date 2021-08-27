# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザ用のキーの設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe"]

try:
    # 設定されているか？
    fc.browser_key1
except:
    # アドレスバーに移動するキーを指定する
    fc.browser_key1 = "C-A-l"

try:
    # 設定されているか？
    fc.browser_key2
except:
    # 新しいタブを開いてそのタブのアドレスバーに移動するキーを指定する
    fc.browser_key2 = "C-A-t"

# ブラウザをポップアップしてから指定したキーを実行する。また、IME を OFF にする。

def browser_popup(key, ime_status=0):
    def _func():
        for window in getWindowList():
            if window.getProcessName() in fc.browser_list:
                popWindow(window)()
                self_insert_command(key)()
                keymap.delayedCall(lambda: keymap.getWindow().setImeStatus(ime_status), 100)
                return

        # fc.browser_list に定義するブラウザが起動していない場合、fc.browser_list の最初
        # に定義するブラウザを起動する
        keymap.ShellExecuteCommand(None, fc.browser_list[0], "", "")()

    return _func

define_key(keymap_global, fc.browser_key1, browser_popup("C-l"))
define_key(keymap_global, fc.browser_key2, browser_popup("C-t"))
