# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 現在アクティブなウィンドウと同じプロセスのウィンドウを順に切り替えるキーを設定する
####################################################################################################

try:
    # 設定されているか？
    fc.window_switching_key2
except:
    # ウィンドウを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    fc.window_switching_key2 = [["A-S-p", "A-S-n"]]

def windowList():
    return getWindowList(None, keymap.getWindow().getProcessName())

for previous_key, next_key in fc.window_switching_key2:
    define_key(keymap_global, previous_key, previous_window(windowList))
    define_key(keymap_global, next_key,     next_window(windowList))
