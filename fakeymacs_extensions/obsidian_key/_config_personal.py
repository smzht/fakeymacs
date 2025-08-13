# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで obsidian_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def reveal_current_file():
    # Obsidian Command : Files: Reveal current file in navigation
    obsidianExecuteCommand("fircfin")()

define_key_o("C-A-f", reveal_current_file)

# --------------------------------------------------------------------------------------------------
