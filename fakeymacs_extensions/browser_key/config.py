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

for browser in fc.browser_list:
    try:
        fc.emacs_exclusion_key[browser].remove("C-l")
    except:
        pass
    try:
        fc.emacs_exclusion_key[browser].remove("C-t")
    except:
        pass

def browser_key(window_keymap, key):
    # 新規に実行する関数を定義する
    func1 = self_insert_command3(key)

    # 以前に定義した関数を抽出する
    func2 = keyFunc(window_keymap, key)

    def _func():
        if keymap.getWindow().getProcessName() in fc.browser_list:
            func1()
        else:
            func2()
    return _func

define_key(keymap_emacs, "C-l", browser_key(keymap_emacs, "C-l"))
define_key(keymap_emacs, "C-t", browser_key(keymap_emacs, "C-t"))

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
