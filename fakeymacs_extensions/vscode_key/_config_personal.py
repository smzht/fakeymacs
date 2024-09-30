# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで vscode_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

def toggle_panel():
    # VSCode Command : View: Tggole Panel
    self_insert_command("C-j")()
    # vscodeExecuteCommand("workbench.action.togglePanel")()

# 本設定を行わなくとも、C-q C-j を利用することで対応は可能
define_key_v("Ctl-x C-j", toggle_panel)

# --------------------------------------------------------------------------------------------------

# VSCode Extension 用のキーの設定を行う
if 1:
    fc.vscode_dired = False
    fc.vscode_recenter = False
    fc.vscode_recenter2 = False
    fc.vscode_occur = False
    fc.vscode_quick_select = True
    fc.vscode_input_sequence = True
    fc.vscode_insert_numbers = True
    fc.vscode_keyboard_macro = False
    fc.vscode_filter_text = False

    exec(readConfigExtension(r"vscode_key\vscode_extensions\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------
