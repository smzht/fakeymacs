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
    def dired(func=dired):
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Open dired buffer
            vscodeExecuteCommand("Op-di-bu")
        else:
            func()

    define_key(keymap_emacs, "Ctl-x d", reset_search(reset_undo(reset_counter(reset_mark(dired)))))

if fc.vscode_recenter:
    def recenter(func=recenter):
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Center Editor Window
            self_insert_command("C-l")()
        else:
            func()

    define_key(keymap_emacs, "C-l", reset_search(reset_undo(reset_counter(recenter))))

if fc.vscode_occur:
    def occur():
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Search in Current File
            vscodeExecuteCommand("Se-in-Cu-Fi")

    define_key(keymap_emacs, "Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(occur)))))
