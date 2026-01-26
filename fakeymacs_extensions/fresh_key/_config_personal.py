# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで fresh_key Extension の機能拡張ファイル
# として機能します。

# --------------------------------------------------------------------------------------------------

fc.fresh_command_dict["Toggle File Explorer"] = ["tofiex", "エ切"]

def toggle_file_explorer():
    freshExecuteCommand("Toggle File Explorer")()

define_key_f("Ctl-x C-e", reset_search(reset_undo(reset_counter(reset_mark(toggle_file_explorer)))))

# ファイルエクスプローラにフォーカスを当てる（C-e）機能は、C-q C-e で OK

# --------------------------------------------------------------------------------------------------
