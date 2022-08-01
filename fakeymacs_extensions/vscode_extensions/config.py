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
    fc.vscode_recenter2
except:
    # Recenter Top Bottom Extension を利用するかどうかを指定する
    fc.vscode_recenter2 = False

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

try:
    # 設定されているか？
    fc.vscode_keyboard_macro
except:
    # Keyboard Macro Beta を利用するかどうかを指定する
    fc.vscode_keyboard_macro = False

try:
    # 設定されているか？
    fc.vscode_filter_text
except:
    # Filter Text を利用するかどうかを指定する
    fc.vscode_filter_text = False

# --------------------------------------------------------------------------------------------------

if fc.vscode_dired:
    def dired():
        # VSCode Command : Open dired buffer
        vscodeExecuteCommand("Odb")()
        # vscodeExecuteCommand("extension.dired.open")()

    define_key_v("Ctl-x d",  reset_search(reset_undo(reset_counter(reset_mark(dired)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_recenter:
    def recenter():
        # VSCode Command : Center Editor Window
        self_insert_command("C-l")()
        # vscodeExecuteCommand("center-editor-window.center")()

    define_key_v("C-l", reset_search(reset_undo(reset_counter(recenter))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_recenter2:
    def recenter2():
        # VSCode Command : Recenter Top Bottom
        vscodeExecuteCommand("RTB")()
        # vscodeExecuteCommand("recenterTopBottom")()

    define_key_v("C-l", reset_search(reset_undo(reset_counter(recenter2))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_occur:
    def occur():
        # VSCode Command : Search in Current File
        vscodeExecuteCommand("SiCF")()
        # vscodeExecuteCommand("search-in-current-file.searchInCurrentFile")()

    define_key_v("Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(occur)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_quick_select:
    # 日本語キーボードのキー設定に齟齬があるようなので、それを是正する
    quick_select_jis_keys = {'"' : "S-Caret",
                             "'" : "Caret",
                             ";" : "Colon",
                             ":" : "S-Colon",
                             "`" : "Atmark",
                             "(" : "S-9",
                             ")" : "S-0",
                             "[" : "OpenBracket",
                             "]" : "CloseBracket",
                             "{" : "S-OpenBracket",
                             "}" : "S-CloseBracket",
                             "<" : "S-Comma",
                             ">" : "S-Period",
                             }

    for key in quick_select_jis_keys:
        if os_keyboard_type == "JP":
            ikey = quick_select_jis_keys[key]
            usjis_conv = False
        else:
            ikey = key
            usjis_conv = True

        define_key_v("C-A-k {}".format(key),
                     reset_rect(region(self_insert_command_v("C-k", ikey, usjis_conv=usjis_conv))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_input_sequence:
    def input_sequence():
        fakeymacs_vscode.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-0")()

    if not fc.use_ctrl_digit_key_for_digit_argument:
        define_key_v("C-A-0", reset_rect(input_sequence))

    define_key_v("C-A-k 0", reset_rect(input_sequence))

# --------------------------------------------------------------------------------------------------

if fc.vscode_insert_numbers:
    def insert_numbers():
        fakeymacs_vscode.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-n")()

    define_key_v("C-A-k n", reset_rect(insert_numbers))

# --------------------------------------------------------------------------------------------------

if fc.vscode_keyboard_macro:
    def keyboard_macro_start():
        self_insert_command("C-A-r")()

    def keyboard_macro_stop():
        self_insert_command("C-A-r")()

    def keyboard_macro_play():
        def playMacro():
            self_insert_command("C-A-p")()
            delay(0.1)

        keymap.delayedCall(playMacro, 0)

    define_key_v("Ctl-x (", keyboard_macro_start)
    define_key_v("Ctl-x )", keyboard_macro_stop)
    define_key_v("Ctl-x e", reset_search(reset_undo(reset_counter(repeat(keyboard_macro_play)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_filter_text:
    def filter_text_in_place():
        # VSCode Command : FilterText: Filter text in-place
        self_insert_command("C-k", "C-f")()
        # vscodeExecuteCommand("extension.filterTextInplace")()

    def run_filter_through_selected_text():
        # VSCode Command : FilterText: Run filter through selected text
        vscodeExecuteCommand("FRftst")()
        # vscodeExecuteCommand("extension.filterText")()

    def shell_command_on_region():
        if fakeymacs.is_universal_argument:
            filter_text_in_place()
        else:
            run_filter_through_selected_text()

    define_key_v("M-|", reset_search(reset_undo(reset_counter(reset_mark(shell_command_on_region)))))

# --------------------------------------------------------------------------------------------------
