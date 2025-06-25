# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ブラウザをポップアップしてから、ブラウザのショートカットキーを入力するキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.browser_list
except:
    # 本機能を適用するブラウザのプログラム名称を指定する
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe",
                      ]

try:
    # 設定されているか？
    fc.browser_url
except:
    # ブラウザが起動していない場合に開く URL を指定する
    # fc.browser_url = r"https://www.google.com/"
    fc.browser_url = r"https://"

try:
    # 設定されているか？
    fc.browser_key
except:
    # 利用するキーの組み合わせ（利用者が入力するキー、ブラウザに発行するキー、IME の状態）を指定する
    fc.browser_key = [["C-A-j", "C-l", 0], # アドレスバーに移動する（IME は OFF）
                      ["C-A-t", "C-t", 0], # 新しいタブを開く（IME は OFF）
                      ["C-A-o", "C-n", 0], # 新しいウィンドウを開く（IME は OFF）
                      ]

# --------------------------------------------------------------------------------------------------

# ブラウザをポップアップしてから指定したキーを実行する
def browser_popup(key, ime_status, browser_list=fc.browser_list):
    def _func():
        def _inputKey():
            escape() # 検索状態になっていた場合に Esc で解除する
            self_insert_command(key)()
            setImeStatus(ime_status)

        if getProcessName() in browser_list:
            _inputKey()
        else:
            for window in getWindowList():
                if window.getProcessName() in browser_list:
                    popWindow(window)()
                    keymap.delayedCall(_inputKey, 50)
                    break
            else:
                # browser_list に設定されているブラウザが起動していない場合、browser_url を開く
                keymap.ShellExecuteCommand(None, fc.browser_url, "", "")()
    return _func

for key1, key2, ime in fc.browser_key:
    define_key(keymap_global, key1, browser_popup(key2, ime))

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"browser_key\config_personal.py", msg=False), dict(globals(), **locals()))
