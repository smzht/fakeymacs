# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで vscode_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def toggle_editor_layout():
    # VSCode Command : Toggle Vertical/Horizontal Editor Layout
    self_insert_command("A-S-0")()
    # vscodeExecuteCommand("workbench.action.toggleEditorGroupLayout")()

define_key3(keymap_emacs, "Ctl-x 4", toggle_editor_layout)

# --------------------------------------------------------------------------------------------------

def open_folder():
    # VSCode Command : File: Open Folder...
    self_insert_command("C-k", "C-o")()
    # vscodeExecuteCommand("workbench.action.files.openFolder")()

# 本設定を行わなくとも、C-A-k C-o を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(open_folder)))))

# --------------------------------------------------------------------------------------------------

def open_recent():
    # VSCode Command : File: Open Recent...
    self_insert_command("C-r")()
    # vscodeExecuteCommand("workbench.action.openRecent")()

# 本設定を行わなくとも、C-q C-r を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-r", reset_search(reset_undo(reset_counter(reset_mark(open_recent)))))

# --------------------------------------------------------------------------------------------------

def quick_open():
    # VSCode Command : Go to File...
    self_insert_command("C-p")()
    # vscodeExecuteCommand("workbench.action.quickOpen")()

# 本設定を行わなくとも、C-q C-p を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-p", reset_search(reset_undo(reset_counter(reset_mark(quick_open)))))

# --------------------------------------------------------------------------------------------------
