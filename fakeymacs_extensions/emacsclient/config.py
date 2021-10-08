# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## クリップボードに格納したファイルもしくはフォルダのパスを emacsclient で開く
####################################################################################################

try:
    # 設定されているか？
    fc.emacsclient_key
except:
    # emacsclient を起動するキーを指定する
    fc.emacsclient_key = "C-Period"

try:
    # 設定されているか？
    fc.emacsclient_name

    # emacsclient プログラムの起動
    def emacsclient():
        clipboard_text = getClipboardText()
        if clipboard_text:
            path = re.sub("\n|\r", "", clipboard_text.strip())
            path = re.sub(r'(\\+)"', r'\1\1"', path)
            path = re.sub('"', r'\"', path)
            path = re.sub('^', '"', path)
            keymap.ShellExecuteCommand(None, fc.emacsclient_name, path, "")()

    define_key(keymap_emacs, fc.emacsclient_key, emacsclient)

except:
    print("fc.emacsclient_name を設定してください")
