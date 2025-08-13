# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで obsidian_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def search_in_all_files():
    # Obsidian Command : Search: Search in all files
    self_insert_command("C-S-f")()

define_key_o("C-A-s", search_in_all_files)

# --------------------------------------------------------------------------------------------------
