# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## YouTube で Space による停止、再生が正しく機能しないことの暫定的な対策を行う
####################################################################################################

try:
    # 設定されているか？
    fc.youtube_browser_list
except:
    # 本対策を行うブラウザのプログラム名称を指定する
    fc.youtube_browser_list = ["chrome.exe",
                               "msedge.exe",
                               "firefox.exe",
                               ]

def space():
    if (fc.ime_reconv_key is None or
        fakeymacs.forward_direction is None):
        if (keymap.getWindow().getProcessName() in fc.youtube_browser_list and
            " - YouTube " in keymap.getWindow().getText()):
            self_insert_command("D-Space")()
        else:
            self_insert_command("Space")()
    else:
        reconversion()

define_key(keymap_emacs, "Space", reset_undo(reset_counter(reset_mark(repeat(space)))))
