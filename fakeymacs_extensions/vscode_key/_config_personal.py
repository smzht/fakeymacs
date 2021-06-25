# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで vscode_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def rotate_layout():
    # VSCode Command : Toggle Vertical/Horizontal Editor Layout
    self_insert_command("A-S-0")()
    # vscodeExecuteCommand("workbench.action.toggleEditorGroupLayout")()

define_key3(keymap_emacs, "Ctl-x 4", rotate_layout)

# --------------------------------------------------------------------------------------------------

def find_directory():
    # VSCode Command : File: Open Folder...
    self_insert_command("C-k", "C-o")()
    # vscodeExecuteCommand("workbench.action.files.openFolder")()

# 本設定を行わなくとも、C-A-k C-o を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-d", reset_search(reset_undo(reset_counter(reset_mark(find_directory)))))

# --------------------------------------------------------------------------------------------------

def recentf():
    # VSCode Command : File: Open Recent...
    self_insert_command("C-r")()
    # vscodeExecuteCommand("workbench.action.openRecent")()

# 本設定を行わなくとも、C-q C-r を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-r", reset_search(reset_undo(reset_counter(reset_mark(recentf)))))

# --------------------------------------------------------------------------------------------------

def locate():
    # VSCode Command : Go to File...
    self_insert_command("C-p")()
    # vscodeExecuteCommand("workbench.action.quickOpen")()

# 本設定を行わなくとも、C-q C-p を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-l", reset_search(reset_undo(reset_counter(reset_mark(locate)))))

# --------------------------------------------------------------------------------------------------
