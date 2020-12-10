# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode で Extension のインストールが必要な機能の設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.vscode_dired
except:
    # vscode-dired Extension を利用するかどうかを指定する
    fc.vscode_dired = False

try:
    # 設定されているか？
    fc.vscode_recenter
except:
    # Center Editor Window Extension を利用するかどうかを指定する
    fc.vscode_recenter = False

try:
    # 設定されているか？
    fc.vscode_occur
except:
    # Search in Current File Extension  を利用するかどうかを指定する
    fc.vscode_occur = False

if fc.vscode_dired:
    def dired(window_keymap, key):
        # 新規に実行する関数を定義する（VSCode Command : Open dired buffer）
        func1 = reset_search(reset_undo(reset_counter(reset_mark(vscodeExecuteCommand("Op-di-bu")))))

        # 以前に定義した関数を抽出する
        func2 = getKeyCommand(window_keymap, key)

        def _func():
            if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
                func1()
            else:
                func2()
        return _func

    define_key(keymap_emacs, "Ctl-x d", dired(keymap_emacs, "Ctl-x d"))

if fc.vscode_recenter:
    def recenter(window_keymap, key):
        # 新規に実行する関数を定義する（VSCode Command : Center Editor Window）
        func1 = reset_search(reset_undo(reset_counter(self_insert_command("C-l"))))

        # 以前に定義した関数を抽出する
        func2 = getKeyCommand(window_keymap, key)

        def _func():
            if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
                func1()
            else:
                func2()
        return _func

    define_key(keymap_emacs, "C-l", recenter(keymap_emacs, "C-l"))

if fc.vscode_occur:
    def occur():
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Search in Current File
            vscodeExecuteCommand("Se-in-Cu-Fi")()

    define_key(keymap_emacs, "Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(occur)))))
