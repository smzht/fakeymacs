# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 指定したキーを押下したときに IME の状態を表示する
####################################################################################################

try:
    # 設定されているか？
    fc.pop_ime_balloon_key
except:
    # IME の状態を表示する機能を追加するキーを指定する
    fc.pop_ime_balloon_key = ["C-l"]

def pop_ime_balloon(window_keymap, key):
    # 定義済みの関数を抽出する
    func = getKeyCommand(window_keymap, key)
    if func is None:
        if key.startswith("O-"):
            func = lambda: None
        else:
            func = keymap.InputKeyCommand(key)

    def _func():
        func()
        # IME の状態を表示する
        popImeBalloon()
    return _func

for key in fc.pop_ime_balloon_key:
    define_key(keymap_emacs, key, pop_ime_balloon(keymap_emacs, key))
    define_key(keymap_ime,   key, pop_ime_balloon(keymap_ime,   key))
