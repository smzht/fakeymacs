# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## VSCode Extension 用のキーの設定を行う
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
    # Search in Current File Extension を利用するかどうかを指定する
    fc.vscode_occur = False

try:
    # 設定されているか？
    fc.vscode_quick_select
except:
    # Quick and Simple Text Selection Extension を利用するかどうかを指定する
    fc.vscode_quick_select = False

try:
    # 設定されているか？
    fc.vscode_input_sequence
except:
    # vscode-input-sequence を利用するかどうかを指定する
    fc.vscode_input_sequence = False

try:
    # 設定されているか？
    fc.vscode_insert_numbers
except:
    # Insert Numbers を利用するかどうかを指定する
    fc.vscode_insert_numbers = False

# --------------------------------------------------------------------------------------------------

if fc.vscode_dired:
    def dired():
        # VSCode Command : Open dired buffer
        vscodeExecuteCommand("Odb")()
        # vscodeExecuteCommand("extension.dired.open")()

    define_key3(keymap_emacs, "Ctl-x d",  reset_search(reset_undo(reset_counter(reset_mark(dired)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_recenter:
    def recenter():
        # VSCode Command : Center Editor Window
        self_insert_command("C-l")()
        # vscodeExecuteCommand("center-editor-window.center")()

    define_key(keymap_vscode, "C-l", reset_search(reset_undo(reset_counter(recenter))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_occur:
    def occur():
        # VSCode Command : Search in Current File
        vscodeExecuteCommand("SiCF")()
        # vscodeExecuteCommand("search-in-current-file.searchInCurrentFile")()

    define_key3(keymap_emacs, "Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(occur)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_quick_select:
    if is_japanese_keyboard:
        quick_select_keys = {'"' : "S-2",
                             "'" : "S-7",
                             ";" : "Semicolon",
                             ":" : "Colon",
                             "`" : "S-Atmark",
                             "(" : "S-8",
                             ")" : "S-9",
                             "[" : "OpenBracket",
                             "]" : "CloseBracket",
                             "{" : "S-OpenBracket",
                             "}" : "S-CloseBracket",
                             "<" : "S-Comma",
                             ">" : "S-Period"
                            }
    else:
        quick_select_keys = {'"' : "S-Quote",
                             "'" : "Quote",
                             ";" : "Semicolon",
                             ":" : "S-Semicolon",
                             "`" : "BackQuote",
                             "(" : "S-9",
                             ")" : "S-0",
                             "[" : "OpenBracket",
                             "]" : "CloseBracket",
                             "{" : "S-OpenBracket",
                             "}" : "S-CloseBracket",
                             "<" : "S-Comma",
                             ">" : "S-Period"
                            }

    for key in quick_select_keys.values():
        mkey = "C-A-k {}".format(key)
        define_key(keymap_vscode, mkey, reset_rect(region(getKeyCommand(keymap_vscode, mkey))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_input_sequence:
    def input_sequence():
        fakeymacs.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-0")()

    if not fc.use_ctrl_digit_key_for_digit_argument:
        define_key(keymap_vscode, "C-A-0", reset_rect(input_sequence))

    define_key(keymap_vscode, "C-A-k 0", reset_rect(input_sequence))

# --------------------------------------------------------------------------------------------------

if fc.vscode_insert_numbers:
    def insert_numbers():
        fakeymacs.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-n")()

    define_key(keymap_vscode, "C-A-k n", reset_rect(insert_numbers))

# --------------------------------------------------------------------------------------------------
