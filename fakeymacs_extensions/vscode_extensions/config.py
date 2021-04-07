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

def define_key3(window_keymap, keys, command):
    define_key(window_keymap, keys,
               makeKeyCommand(window_keymap, keys, command, lambda: checkWindow("Code.exe", None)))

def vscodeExecuteCommand(command):
    def _func():
        self_insert_command("f1")()
        princ(command)
        self_insert_command("Enter")()
    return _func

if fc.vscode_dired:
    def dired():
        # VSCode Command : Open dired buffer
        reset_search(reset_undo(reset_counter(reset_mark(vscodeExecuteCommand("extension.dired.open")))))()

    define_key3(keymap_emacs, "Ctl-x d", dired)

if fc.vscode_recenter:
    def recenter():
        # VSCode Command : Center Editor Window
        reset_search(reset_undo(reset_counter(self_insert_command("C-l"))))()

    define_key3(keymap_emacs, "C-l", recenter)

if fc.vscode_occur:
    def occur():
        # VSCode Command : Search in Current File
        reset_search(reset_undo(reset_counter(reset_mark(vscodeExecuteCommand("search-in-current-file.searchInCurrentFile")))))()

    define_key3(keymap_emacs, "Ctl-x C-o", occur)
