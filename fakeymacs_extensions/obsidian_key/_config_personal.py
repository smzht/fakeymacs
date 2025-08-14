# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで obsidian_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def show_file_explorer():
    # Obsidian Command : Files: Show file explorer
    obsidianExecuteCommand("f:sf")()

define_key_o("C-A-f", show_file_explorer)

# --------------------------------------------------------------------------------------------------
