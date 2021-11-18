# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザをポップアップしてから C-l、C-t を入力するキーを設定する
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
    # アドレスバーに移動するキーを指定する（IME は OFF）
    fc.browser_key1 = "C-A-l"

try:
    # 設定されているか？
    fc.browser_key2
except:
    # 新しいタブを開いてそのタブのアドレスバーに移動するキーを指定する（IME は OFF）
    fc.browser_key2 = "C-A-t"

try:
    # 設定されているか？
    fc.browser_key3
except:
    # アドレスバーに移動するキーを指定する（IME は ON）
    fc.browser_key3 = "C-A-i"

# ブラウザをポップアップしてから指定したキーを実行する。

def browser_popup(key, ime_status):
    def _func():
        for window in getWindowList():
            if window.getProcessName() in fc.browser_list:
                popWindow(window)()
                delay()
                self_insert_command(key)()
                keymap.delayedCall(lambda: keymap.getWindow().setImeStatus(ime_status), 100)
                return

        # fc.browser_list に定義するブラウザが起動していない場合、fc.browser_list の最初
        # に定義するブラウザを起動する
        keymap.ShellExecuteCommand(None, fc.browser_list[0], "", "")()

    return _func

define_key(keymap_global, fc.browser_key1, browser_popup("C-l", 0))
define_key(keymap_global, fc.browser_key2, browser_popup("C-t", 0))
define_key(keymap_global, fc.browser_key3, browser_popup("C-l", 1))
