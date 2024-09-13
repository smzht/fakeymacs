# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Boss だ！
####################################################################################################

try:
    # 設定されているか？
    fc.boss_key
except:
    # 本機能を利用するためのキーを指定する
    fc.boss_key = "W-a"

try:
    # 設定されているか？
    fc.boss_open_app
except:
    # 全てのウィンドウを閉じた後に新たに開く URL、プログラムなどを指定する
    # （不要であれば、None を指定する）
    fc.boss_open_app = "https://www.google.com/"
    # fc.boss_open_app = "notepad.exe"
    # fc.boss_open_app = None

# --------------------------------------------------------------------------------------------------

def boss():
    # 全てのウィンドウを最小化する
    self_insert_command("W-d")()

    if fc.boss_open_app:
        delay(0.1)
        keymap.ShellExecuteCommand(None, fc.boss_open_app, "", "")()

define_key(keymap_global, fc.boss_key, boss)
