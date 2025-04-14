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

try:
    vscode_prefix_key = fc.vscode_prefix_key[0][1]
except:
    vscode_prefix_key = None

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
    # Command Title と省略形
    quick_select_command = {'"' : ["Quick Select: Select inside double quote",     "QSSIdq" ],
                            "'" : ["Quick Select: Select inside single quote",     "QSSisiq"],
                            ";" : ["Quick Select: Select inside either quote",     "QSSieq" ],
                            ":" : ["Quick Select: Switch quotes",                  "QSSwq"  ],
                            "`" : ["Quick Select: Select inside back tick",        "QSSibt" ],
                            "(" : ["Quick Select: Select inside parenthesis",      "QSSip"  ],
                            ")" : ["Quick Select: Select outside parenthesis",     "QSSop"  ],
                            "[" : ["Quick Select: Select inside square brackets",  "QSSisb" ],
                            "]" : ["Quick Select: Select outside square brackets", "QSSosb" ],
                            "{" : ["Quick Select: Select inside curly brackets",   "QSSicb" ],
                            "}" : ["Quick Select: Select outside curly brackets",  "QSSocb" ],
                            "<" : ["Quick Select: Select inside angled brackets",  "QSSiab" ],
                            ">" : ["Quick Select: Select inside tag",              "QSSita" ],
                            }

    for key in quick_select_command:
        quick_select = vscodeExecuteCommand(quick_select_command[key][1])

        if vscode_prefix_key:
            define_key_v(f"{vscode_prefix_key} {key}", reset_rect(region(quick_select)))

# --------------------------------------------------------------------------------------------------

if fc.vscode_input_sequence:
    def input_sequence():
        fakeymacs_vscode.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-0")()

    if not fc.use_ctrl_digit_key_for_digit_argument:
        define_key_v("C-A-0", reset_rect(input_sequence))

    if vscode_prefix_key:
        define_key_v(f"{vscode_prefix_key} 0", reset_rect(input_sequence))

# --------------------------------------------------------------------------------------------------

if fc.vscode_insert_numbers:
    def insert_numbers():
        fakeymacs_vscode.post_processing = lambda: region(lambda: None)()
        self_insert_command3("C-A-n")()

    if vscode_prefix_key:
        define_key_v(f"{vscode_prefix_key} n", reset_rect(insert_numbers))

# --------------------------------------------------------------------------------------------------

if fc.vscode_keyboard_macro:
    def keyboard_macro_start():
        self_insert_command("C-A-r")()

    def keyboard_macro_stop():
        self_insert_command("C-A-r")()

    def keyboard_macro_play():
        def _keyboard_macro_play():
            self_insert_command("C-A-p")()
            delay(0.1)

        keymap.delayedCall(_keyboard_macro_play, 0)

    define_key_v("Ctl-x (", keyboard_macro_start)
    define_key_v("Ctl-x )", keyboard_macro_stop)
    define_key_v("Ctl-x e", reset_search(reset_undo(reset_counter(repeat(keyboard_macro_play)))))

# --------------------------------------------------------------------------------------------------

if fc.vscode_filter_text:
    def filter_text_in_place():
        # VSCode Command : FilterText: Filter text in-place
        vscodeExecuteCommand("FFtip")()
        # self_insert_command("C-k", "C-f")()
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
