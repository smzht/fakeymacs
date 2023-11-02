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

def is_youtube():
    if (keymap.getWindow().getProcessName() in fc.youtube_browser_list and
        " - YouTube " in keymap.getWindow().getText()):
        return True
    else:
        return False

def youtube_space():
    if (fc.ime_reconv_key is None or
        fakeymacs.forward_direction is None):
        try:
            if fakeymacs.space_fn_key_up:
                self_insert_command("Space")()
            else:
                self_insert_command("D-Space")()
        except:
            self_insert_command("D-Space")()
    else:
        reconversion()

define_key3(keymap_emacs, "Space", reset_undo(reset_counter(reset_mark(repeat(youtube_space)))), is_youtube)
