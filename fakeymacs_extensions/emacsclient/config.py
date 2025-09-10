# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## クリップボードに格納したファイルもしくはフォルダのパスを emacsclient で開く
####################################################################################################

try:
    # 設定されているか？
    fc.emacsclient_key
except:
    # emacsclient を起動するキーを指定する
    fc.emacsclient_key = "C-A-."

try:
    # 設定されているか？
    fc.remove_space
except:
    # パスに含まれているスペースを除去するかどうかを指定する（True: 除去する、False: 除去しない）
    fc.remove_space = False

# --------------------------------------------------------------------------------------------------

try:
    # 設定されているか？
    fc.emacsclient_name

    # emacsclient プログラムの起動
    def emacsclient():
        clipboard_text = getClipboardText()
        if clipboard_text:
            path = re.sub("\n|\r", "", clipboard_text.strip())
            if fc.remove_space:
                path = re.sub(" ", "", path)
            path = re.sub(r'(\\+)"', r'\1\1"', path)
            path = re.sub('"', r'\"', path)
            path = re.sub('^', '"', path)
            keymap.ShellExecuteCommand(None, fc.emacsclient_name, path, "")()

    define_key(keymap_global, fc.emacsclient_key, emacsclient)

except:
    print("fc.emacsclient_name を設定してください")
