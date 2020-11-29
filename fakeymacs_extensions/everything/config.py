# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Everything を起動するキーを指定する
####################################################################################################

try:
    # 設定されているか？
    fc.everything_key
except:
    # Everything を起動するキーを指定する
    fc.everything_key = "C-A-v"

try:
    # 設定されているか？
    fc.everything_name
except:
    # Everything プログラムを指定する
    fc.everything_name = r"C:\Program Files\Everything\everything.exe"

def everything():
    keymap.ShellExecuteCommand(None, fc.everything_name, "", "")()

define_key(keymap_global, fc.everything_key, everything)
