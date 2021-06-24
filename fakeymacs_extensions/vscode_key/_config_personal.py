# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで vscode_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

def toggle_editor_layout():
    # VSCode Command : Toggle Vertical/Horizontal Editor Layout
    self_insert_command("A-S-0")()
    # vscodeExecuteCommand("workbench.action.toggleEditorGroupLayout")()

define_key3(keymap_emacs, "Ctl-x 4", toggle_editor_layout)

def recentf():
    # VSCode Command : File: Open Recent...
    self_insert_command("C-r")()
    # vscodeExecuteCommand("workbench.action.openRecent")()

# 本設定を行わなくとも、C-q C-r を利用することで対応は可能
define_key3(keymap_emacs, "Ctl-x C-r", reset_search(reset_undo(reset_counter(reset_mark(recentf)))))
