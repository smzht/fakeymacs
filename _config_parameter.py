# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、fakeymacs で設定可能な全てのコンフィグレーションパラメータをまとめたファイルです。
# config_personal.py を作成する際の参考としてください。config_personal.py に名称変更して個人設定
# ファイルとして利用することもできます。

####################################################################################################
## 初期設定
####################################################################################################
# [section-init] -----------------------------------------------------------------------------------

print(startupString())

keymap.editor = r"notepad.exe"
keymap.setFont("ＭＳ ゴシック", 12)

####################################################################################################
## 機能オプションの選択
####################################################################################################
# [section-options] --------------------------------------------------------------------------------

# IMEの設定（次の設定のいずれかを有効にする）
# fc.ime = "old_Microsoft_IME"
fc.ime = "new_Microsoft_IME"
# fc.ime = "Google_IME"
# fc.ime = None

# 日本語キーボード設定をした OS 上で英語キーボードを利用するかどうかを指定する
# （True: 使う、False: 使わない）
# （False に設定した場合でも、OS の設定が日本語キーボードになっていれば、ランチャーメニュー
#   の一番最後に表示されるメニューからキーボード種別を切り替えることができます）
fc.use_usjis_keyboard_conversion = False

# IME の状態をテキスト カーソル インジケーターの色で表現するかどうかを指定する
# （True: 表現する、False: 表現しない）
# （テキスト カーソル インジケーターを利用するには、次のページを参考とし設定を行ってください
#   https://faq.nec-lavie.jp/qasearch/1007/app/servlet/relatedqa?QID=022081）
fc.use_ime_status_cursor_color = False

# IME が ON のときのテキスト カーソル インジケーターの色を指定する
fc.ime_on_cursor_color = 0x00C800 # 濃い緑

# IME が OFF のときのテキスト カーソル インジケーターの色を指定する
fc.ime_off_cursor_color = 0x0000FF # 赤

# Chromium 系ブラウザで発生する問題の対策を行うかどうかを指定する（True: 対策する、False: 対策しない）
# （Chromium 系ブラウザのバージョン 92 では、アドレスバーにカーソルを移動した際、強制的に ASCII入力
#   モードに移行する不具合が発生します。（バージョン 93 で対策済みですが、過去にも度々発生しています。）
#   ・https://did2memo.net/2021/07/22/chrome-japanese-ime-off-issue-chrome-92/
#   さらに Google 日本語入力を利用している場合、keymap.getWindow().getImeStatus() が True を返すため、
#   Emacs 日本語入力モードの挙動がおかしくなります。この対策を行うかどうかを指定します。）
fc.correct_ime_status = False

# 上記の対策を行う Chromium 系ブラウザのプログラム名称を指定する
fc.chromium_browser_list = ["chrome.exe",
                            "msedge.exe",
                            ]

####################################################################################################
## 基本設定
####################################################################################################
# [section-base-1] ---------------------------------------------------------------------------------

# すべてのキーマップを透過（スルー）するアプリケーションソフトを指定する（全ての設定に優先する）
# （keymap_base、keymap_global を含むすべてのキーマップをスルーします）
fc.transparent_target       = []

# すべてのキーマップを透過（スルー）するウィンドウのクラスネームを指定する（全ての設定に優先する）
# （keymap_base、keymap_global を含むすべてのキーマップをスルーします）
fc.transparent_target_class = ["IHWindowClass"]      # Remote Desktop

# Emacs のキーバインドにするウィンドウのクラスネームを指定する（fc.not_emacs_target の設定より優先する）
fc.emacs_target_class   = ["Edit",                   # テキスト入力フィールドなどが該当
                           "Button",                 # ボタン
                           "ComboBox",               # コンボボックス
                           "ListBox",                # リストボックス
                           ]

# Emacs のキーバインドに“したくない”アプリケーションソフトを指定する
# （Keyhac のメニューから「内部ログ」を ON にすると processname や classname を確認することができます）
fc.not_emacs_target     = ["wsl.exe",                # WSL
                           "bash.exe",               # WSL
                           "ubuntu.exe",             # WSL
                           "ubuntu1604.exe",         # WSL
                           "ubuntu1804.exe",         # WSL
                           "ubuntu2004.exe",         # WSL
                           "ubuntu2204.exe",         # WSL
                           "debian.exe",             # WSL
                           "kali.exe",               # WSL
                           "SLES-12.exe",            # WSL
                           "openSUSE-42.exe",        # WSL
                           "openSUSE-Leap-15-1.exe", # WSL
                           "WindowsTerminal.exe",    # Windows Terminal
                           "mintty.exe",             # mintty
                           "Cmder.exe",              # Cmder
                           "ConEmu.exe",             # ConEmu
                           "ConEmu64.exe",           # ConEmu
                           "emacs.exe",              # Emacs
                           "emacs-X11.exe",          # Emacs
                           "emacs-w32.exe",          # Emacs
                           "gvim.exe",               # GVim
                           "xyzzy.exe",              # xyzzy
                           "msrdc.exe",              # WSLg
                           "XWin.exe",               # Cygwin/X
                           "XWin_MobaX.exe",         # MobaXterm/X
                           "XWin_MobaX_1.16.3.exe",  # MobaXterm/X
                           "XWin_MobaX_1.20.4.exe",  # MobaXterm/X
                           "XWin_Cygwin_1.14.5.exe", # MobaXterm/X
                           "XWin_Cygwin_1.16.3.exe", # MobaXterm/X
                           "Xming.exe",              # Xming
                           "vcxsrv.exe",             # VcXsrv
                           "GWSL_vcxsrv.exe",        # GWSL
                           "GWSL_vcxsrv_lowdpi.exe", # GWSL
                           "X410.exe",               # X410
                           "Xpra-Launcher.exe",      # Xpra
                           "putty.exe",              # PuTTY
                           "ttermpro.exe",           # TeraTerm
                           "MobaXterm.exe",          # MobaXterm
                           "TurboVNC.exe",           # TurboVNC
                           "vncviewer.exe",          # UltraVNC
                           "vncviewer64.exe",        # UltraVNC
                           ]

# IME の切り替え“のみをしたい”アプリケーションソフトを指定する
# （指定できるアプリケーションソフトは、not_emacs_target で（除外）指定したものからのみとなります）
fc.ime_target           = ["wsl.exe",                # WSL
                           "bash.exe",               # WSL
                           "ubuntu.exe",             # WSL
                           "ubuntu1604.exe",         # WSL
                           "ubuntu1804.exe",         # WSL
                           "ubuntu2004.exe",         # WSL
                           "ubuntu2204.exe",         # WSL
                           "debian.exe",             # WSL
                           "kali.exe",               # WSL
                           "SLES-12.exe",            # WSL
                           "openSUSE-42.exe",        # WSL
                           "openSUSE-Leap-15-1.exe", # WSL
                           "WindowsTerminal.exe",    # Windows Terminal
                           "mintty.exe",             # mintty
                           "Cmder.exe",              # Cmder
                           "ConEmu.exe",             # ConEmu
                           "ConEmu64.exe",           # ConEmu
                           "gvim.exe",               # GVim
                           "xyzzy.exe",              # xyzzy
                           "putty.exe",              # PuTTY
                           "ttermpro.exe",           # TeraTerm
                           "MobaXterm.exe",          # MobaXterm
                           ]

# キーマップ毎にキー設定をスキップするキーを指定する
# （リストに指定するキーは、define_key の第二引数に指定する記法のキーとしてください。"A-v" や "C-v"
#   のような指定の他に、"M-f" や "Ctl-x d" などの指定も可能です。"M-g*" のようにワイルドカードも
#   利用することができます。ワイルドカード文字をエスケープしたい場合は、[] で括ってください。）
# （ここで指定したキーに新たに別のキー設定をしたいときには、「-2」が付くセクション内で define_key2
#   関数を利用して定義してください）
fc.skip_settings_key    = {"keymap_base"      : ["*W-g"], # ベース Keymap
                           "keymap_global"    : [],       # グローバル Keymap
                           "keymap_emacs"     : [],       # Emacs キーバインド対象アプリ用 Keymap
                           "keymap_vscode"    : [],       # Emacs キーバインド VSCode 拡張用 Keymap
                           "keymap_ime"       : [],       # IME 切り替え専用アプリ用 Keymap
                           "keymap_ei"        : [],       # Emacs 日本語入力モード用 Keymap
                           "keymap_tsw"       : [],       # タスク切り替え画面用 Keymap
                           "keymap_lw"        : [],       # リストウィンドウ用 Keymap
                           }

# Emacs のキーバインドにするアプリケーションソフトで、Emacs キーバインドから除外するキーを指定する
# （リストに指定するキーは、Keyhac で指定可能なマルチストロークではないキーとしてください。
#   Fakeymacs の記法の "M-f" や "Ctl-x d" などの指定はできません。"A-v"、"C-v" などが指定可能です。）
# （ここで指定しなくとも、左右のモディファイアキーを使い分けることで入力することは可能です）
fc.emacs_exclusion_key  = {"chrome.exe"       : ["C-l", "C-t"],
                           "msedge.exe"       : ["C-l", "C-t"],
                           "firefox.exe"      : ["C-l", "C-t"],
                           "Code.exe"         : ["C-S-b", "C-S-f", "C-S-p", "C-S-n", "C-S-a", "C-S-e"],
                           }

# clipboard 監視の対象外とするアプリケーションソフトを指定する
fc.not_clipboard_target = []
fc.not_clipboard_target += ["EXCEL.EXE"] # Microsoft Excel

# clipboard 監視の対象外とするウィンドウのクラスネームを指定する（ワイルドカードの指定可）
fc.not_clipboard_target_class = []
fc.not_clipboard_target_class += ["HwndWrapper*"] # WPF アプリ

# 左右どちらの Ctrl キーを使うかを指定する（"L": 左、"R": 右）
fc.side_of_ctrl_key = "L"

# 左右どちらの Alt キーを使うかを指定する（"L": 左、"R": 右）
fc.side_of_alt_key = "L"

# 左右どちらの Win キーを使うかを指定する（"L": 左、"R": 右）
fc.side_of_win_key = "L"

# C-i キーを Tab キーとして使うかどうかを指定する（True: 使う、False: 使わない）
fc.use_ctrl_i_as_tab = True

# Esc キーを Meta キーとして使うかどうかを指定する（True: 使う、False: 使わない）
# （True（Meta キーとして使う）に設定されている場合、ESC の二回押下で ESC が入力されます）
fc.use_esc_as_meta = False

# C-[ キーを Meta キーとして使うかどうかを指定する（True: 使う、False: 使わない）
# （True（Meta キーとして使う）に設定されている場合、C-[ の二回押下で ESC が入力されます）
fc.use_ctrl_openbracket_as_meta = True

# Ctl-x プレフィックスキーに使うキーを指定する
# （Ctl-x プレフィックスキーのモディファイアキーは、Ctrl または Alt のいずれかから指定してください）
fc.ctl_x_prefix_key = "C-x"
# fc.ctl_x_prefix_key = "A-x"

# スクロールに使うキーの組み合わせ（Up、Down の順）を指定する
# fc.scroll_key = None # PageUp、PageDown キーのみを利用する
fc.scroll_key = ["M-v", "C-v"]

# Emacs 日本語入力モードを使うかどうかを指定する（True: 使う、False: 使わない）
fc.use_emacs_ime_mode = True

# Emacs 日本語入力モードが有効なときに表示するバルーンメッセージを指定する
# fc.emacs_ime_mode_balloon_message = None
fc.emacs_ime_mode_balloon_message = "▲"

# IME の状態を表示するバルーンメッセージを表示するかどうかを指定する（True: 表示する、False: 表示しない）
fc.use_ime_status_balloon = True

# IME の状態を表示するバルーンメッセージの組み合わせ（英数入力、日本語入力）を指定する
fc.ime_status_balloon_message = ["[A]", "[あ]"]

# IME をトグルで切り替えるキーを指定する（複数指定可）
fc.toggle_input_method_key = []
fc.toggle_input_method_key += ["C-Yen"]
fc.toggle_input_method_key += ["C-o"]
# fc.toggle_input_method_key += ["O-LAlt"]

#---------------------------------------------------------------------------------------------------
# IME を切り替えるキーの組み合わせ（disable、enable の順）を指定する（複数指定可）
# （toggle_input_method_key のキー設定より優先します）
fc.set_input_method_key = []

## 日本語キーボードを利用している場合、<無変換> キーで英数入力、<変換> キーで日本語入力となる
fc.set_input_method_key += [["(29)", "(28)"]]

## 日本語キーボードを利用している場合、<Ａ> キーで英数入力、<あ> キーで日本語入力となる
## （https://docs.microsoft.com/ja-jp/windows-hardware/design/component-guidelines/keyboard-japan-ime）
fc.set_input_method_key += [["(26)", "(22)"]]

## LAlt の単押しで英数入力、RAlt の単押しで日本語入力となる
## （JetBrains 製の IDE でこの設定を利用するためには、ツールボタンをオンにする必要があるようです。
##   設定は、View -> Appearance -> Tool Window Bars を有効にしてください。）
# fc.set_input_method_key += [["O-LAlt", "O-RAlt"]]

## C-j や C-j C-j で 英数入力となる（toggle_input_method_key の設定と併せ、C-j C-o で日本語入力となる）
# fc.set_input_method_key += [["C-j", None]]

## C-j で英数入力、C-o で日本語入力となる（toggle_input_method_key の設定より優先）
# fc.set_input_method_key += [["C-j", "C-o"]]

## C-j で英数入力、C-i で日本語入力となる（C-i が Tab として利用できなくなるが、トグルキー C-o との併用可）
# fc.set_input_method_key += [["C-j", "C-i"]]
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# IME の「再変換」を行うキーを指定する

## IME の「再変換」のために利用するキーを設定する（複数指定可）
## （Google 日本語入力を利用する場合、Ctrl キーと組み合わせたキーを設定してください。「確定取り消し」
##   が正常に動作しないアプリケーションソフト（Microsoft Excel、Sakura Editor など）があります。
##   ただし、C-Back キーは設定しないでください。）
## （リージョンを選択した状態で Space キーを押下すると「再変換」が機能します）
fc.reconversion_key = []
fc.reconversion_key += ["C-,"]    # Comma は < のキーでもあり、変換を戻すイメージを持てるので採用
# fc.reconversion_key += ["(28)"]   # <変換> キーを利用する場合でも、本機能を全て使うためには設定が必要
# fc.reconversion_key += ["O-RAlt"] # ワンショットモディファイアの指定も可能

## IME に設定してある「再変換」、「確定取り消し」を行うキーを指定する

## Windows 10 1909 以前の Microsoft IME の場合
if fc.ime == "old_Microsoft_IME":
    fc.ime_reconv_key = "W-/"    # 「再変換」キー
    fc.ime_cancel_key = "C-Back" # 「確定の取り消し」キー
    fc.ime_reconv_region = False # 「再変換」の時にリージョンの選択が必要かどうかを指定する

## Windows 10 2004 以降の 新しい Microsoft IME の場合
## （新しい Microsoft IME には確定取り消し（C-Backspace）の設定が無いようなので、「再変換」のキー
##   を設定しています）
elif fc.ime == "new_Microsoft_IME":
    fc.ime_reconv_key = "W-/"    # 「再変換」キー
    fc.ime_cancel_key = "W-/"    # 「確定の取り消し」キー
    fc.ime_reconv_region = False # 「再変換」の時にリージョンの選択が必要かどうかを指定する

## Google 日本語入力の場合
elif fc.ime == "Google_IME":
    fc.ime_reconv_key = "W-/"    # 「再変換」キー
    fc.ime_cancel_key = "C-Back" # 「確定の取り消し」キー
    fc.ime_reconv_region = True  # 「再変換」の時にリージョンの選択が必要かどうかを指定する

## 上記以外の場合の場合（機能を無効にする）
else:
    fc.reconversion_key = []
    fc.ime_reconv_key = None
    fc.ime_cancel_key = None
    fc.ime_reconv_region = False
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# Emacs 日本語入力モードを利用する際に、IME のショートカットを置き換えるキーの組み合わせ
# （置き換え先、置き換え元）を指定する
# （「ことえり」のキーバインドを利用するための設定例です。Google 日本語入力で「ことえり」の
#   キー設定になっている場合には不要ですが、設定を行っていても問題はありません。）
fc.emacs_ime_mode_key = []
fc.emacs_ime_mode_key += [["C-i", "S-Left"],  # 文節を縮める
                          ["C-o", "S-Right"], # 文節を伸ばす
                          ["C-j", "F6"],      # ひらがなに変換
                          ["C-k", "F7"],      # 全角カタカナに変換
                          ["C-l", "F9"],      # 全角英数に表示切替
                          ["C-;", "F8"]]      # 半角に変換

if is_japanese_keyboard:
    fc.emacs_ime_mode_key += [["C-:", "F10"]] # 半角英数に表示切替
else:
    fc.emacs_ime_mode_key += [["C-'", "F10"]] # 半角英数に表示切替
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# IME の「単語登録」プログラムを利用するための設定を行う

## IME の「単語登録」プログラムを起動するキーを指定する
# fc.word_register_key = None
fc.word_register_key = "C-]"

## IME の「単語登録」プログラムとそのパラメータを指定する

## Microsoft IME の場合
if fc.ime in ["old_Microsoft_IME", "new_Microsoft_IME"]:
    fc.word_register_name = r"C:\Windows\System32\IME\IMEJP\IMJPDCT.EXE"
    fc.word_register_param = ""

## Google 日本語入力の場合
elif fc.ime == "Google_IME":
    fc.word_register_name = r"C:\Program Files (x86)\Google\Google Japanese Input\GoogleIMEJaTool.exe"
    fc.word_register_param = "--mode=word_register_dialog"

## 上記以外の場合の場合（機能を無効にする）
else:
    fc.word_register_key = None
    fc.word_register_name = None
    fc.word_register_param = None
#---------------------------------------------------------------------------------------------------

# Emacs キーバインドを切り替えるキーを指定する
# （Emacs キーバインドを利用するアプリケーションでかつフォーカスが当たっているアプリケーションソフト
#   に対して切り替えが機能します。また、Emacs キーバインドを OFF にしても、IME の切り替えは ime_target
#   に登録したアプリケーションソフトと同様に機能するようにしています。）
# （fc.emacs_target_class 変数に指定したクラスに該当するアプリケーションソフト（Windows10版 Notepad など）
#   は、Emacs キーバインドを切り替えの対象となりません（常に Emacs キーバインドとなります）。）
fc.toggle_emacs_keybind_key = "C-S-Space"

# アプリケーションキーとして利用するキーを指定する
# （修飾キーに Alt は使えないようです）
fc.application_key = None
# fc.application_key = "O-RCtrl"

# 数引数の指定に Ctrl+数字キーを使うかを指定する（True: 使う、False: 使わない）
# （False に指定しても、C-u 数字キーで数引数を指定することができます）
fc.use_ctrl_digit_key_for_digit_argument = False

# F1 から F12 を Alt+数字キー列として使うかを指定する（True: 使う、False: 使わない）
fc.use_alt_digit_key_for_f1_to_f12 = False

# F13 から F24 を Alt-Shift+数字キー列として使うかを指定する（True: 使う、False: 使わない）
fc.use_alt_shift_digit_key_for_f13_to_f24 = False

# 表示しているウィンドウの中で、一番最近までフォーカスがあったウィンドウに移動するキーを指定する
fc.other_window_key = "A-o"

# アクティブウィンドウを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
# （A-Esc キーの動作とは異なり、仮想デスクトップを跨ぎ、最小化されていないウィンドウを順に切り替え
#   ます。初期設定は ["A-p", "A-n"] としていますが、Emacs の shell-mode のキーバインドなどと設定が
#   被る場合には、["A-S-p", "A-S-n"] などの異なる設定とするか、Emacs 側に次の設定を入れて、Emacs 側
#   のキーの設定を置き換えてご利用ください。
#     (define-key key-translation-map (kbd "M-S-p") (kbd "M-p"))
#     (define-key key-translation-map (kbd "M-S-n") (kbd "M-n"))
#  ）
fc.window_switching_key = []
fc.window_switching_key += [["A-p", "A-n"]]
# fc.window_switching_key += [["A-S-p", "A-S-n"]]
# fc.window_switching_key += [["A-Up", "A-Down"]]

# アクティブウィンドウをディスプレイ間で移動するキーの組み合わせ（前、後 の順）を指定する（複数指定可）
# （デフォルトキーは、["W-S-Left", "W-S-Right"]）
fc.window_movement_key_for_displays = []
fc.window_movement_key_for_displays += [[None, "W-o"]]
# fc.window_movement_key_for_displays += [[None, "A-S-o"]]

# デュアルディスプレイにそれぞれ表示されているウィンドウを入れ替えるキーを指定する
fc.transpose_windows_key = "W-t"

# ウィンドウを最大化、リストアするキーの組み合わせ（リストア、最大化 の順）を指定する（複数指定可）
# （マルチディスプレイでの最大化にも対応しています）
fc.window_maximize_key = []
fc.window_maximize_key += [["W-S-q", "W-q"]] # Windows ショートカットキーの W-q の機能は、W-s で代用可
# fc.window_maximize_key += [["W-S-m", "W-m"]] # Windows ショートカットキーの W-m の機能は、W-d で代用可
# fc.window_maximize_key += [["W-S-s", "W-s"]] # Windows ショートカットキーの W-s の機能は、W-q で代用可

# ウィンドウを最小化、リストアするキーの組み合わせ（リストア、最小化 の順）を指定する（複数指定可）
fc.window_minimize_key = []
fc.window_minimize_key += [["A-S-m", "A-m"]]

# 仮想デスクトップを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
# （仮想デスクトップを切り替えた際にフォーカスのあるウィンドウを適切に処理するため、設定するキーは
#   Win キーとの組み合わせとしてください）
# （デフォルトキーは、["W-C-Left", "W-C-Right"]）
fc.desktop_switching_key = []
fc.desktop_switching_key += [["W-b", "W-f"]]
# fc.desktop_switching_key += [["W-Left", "W-Right"]]

# アクティブウィンドウを仮想デスクトップ間で移動するキーの組み合わせ（前、後 の順）を指定する（複数指定可）
# （本機能を利用する場合は、次のページから SylphyHornPlus をインストールしてください。
#   ・https://github.com/hwtnb/SylphyHornPlusWin11/releases
#   SylphyHornPlus は、Microsoft Store からインストール可能な SylphyHorn の Fork で、Windows 11 の
#   対応など、改良が加えられたものとなっています。）
# （アクティブウィンドウを仮想デスクトップ間で移動するためのデフォルトキーは、["W-C-A-Left", "W-C-A-Right"]
#   です。この設定は変更しないでください。）
fc.window_movement_key_for_desktops = []
# fc.window_movement_key_for_desktops += [["W-p", "W-n"]]
# fc.window_movement_key_for_desktops += [["W-Up", "W-Down"]]

# ウィンドウ操作（other_window、restore_window など）の対象としたくないアプリケーションソフトの
# “クラス名称”を指定する
# （re.match 関数（先頭からのマッチ）の正規表現に「|」を使って繋げて指定してください。
#   完全マッチとするためには $ の指定が必要です。）
fc.window_operation_exclusion_class = r"Progman$"

# ウィンドウ操作（other_window、restore_window など）の対象としたくないアプリケーションソフトの
# “プロセス名称”を指定する
# （re.match 関数（先頭からのマッチ）の正規表現に「|」を使って繋げて指定してください。
#   完全マッチとするためには $ の指定が必要です。）
fc.window_operation_exclusion_process = r"RocketDock\.exe$"  # サンプルとして RocketDock.exe を登録

# クリップボードリストを起動するキーを指定する
fc.clipboardList_key = "A-y"

# ランチャーリストを起動するキーを指定する
fc.lancherList_key = "A-l"

# shell_command 関数で起動するアプリケーションソフトを指定する
# （PATH が通っていない場所にあるコマンドは、絶対パスで指定してください）
fc.command_name = r"cmd.exe"

# コマンドのリピート回数の最大値を指定する
fc.repeat_max = 1024

# Microsoft Excel のセル内で改行を選択可能かを指定する（True: 選択可、False: 選択不可）
# （kill_line 関数の挙動を変えるための変数です。Microsoft Excel 2019 以降では True にして
#   ください。）
fc.is_newline_selectable_in_Excel = True

# Ctrl キー単押しで開く Ctrl ボタンを持つアプリケーションソフト（プロセス名称とクラス名称の
# 組み合わせ（ワイルドカード指定可））を指定する
# （Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
#   開く機能があります。その挙動を抑制するアプリケーションソフトのリストを指定してください。）
fc.ctrl_button_app_list = [["WINWORD.EXE",  "_WwG"],
                           ["EXCEL.EXE",    "EXCEL*"],
                           ["POWERPNT.EXE", "mdiClass"],
                           ]

# ゲームなど、キーバインドの設定を極力行いたくないアプリケーションソフト（プロセス名称と
# クラス名称の組み合わせ（ワイルドカード指定可））を指定する
# （keymap_global 以外のすべてのキーマップをスルーします。ゲームなど、Keyhac によるキー設定と
#   相性が悪いアプリケーションソフトを指定してください。keymap_base の設定もスルーするため、
#   英語 -> 日本語キーボード変換の機能が働かなくなることにご留意ください。）
# （msrdc.exe の行の有効化の必要性については、次のコミットの説明を参照してください。
#   https://github.com/smzht/fakeymacs/commit/5ceb921bd754ce348f9cd79b6606086916520945）
fc.game_app_list        = [["ffxiv_dx11.exe", "*"],            # FINAL FANTASY XIV
                           # ["msrdc.exe",      "RAIL_WINDOW"],  # WSLg
                           ]

# [section-base-2] ---------------------------------------------------------------------------------

####################################################################################################
## クリップボードリストの設定
####################################################################################################
# [section-clipboardList-1] ------------------------------------------------------------------------

# クリップボードリストを利用するための設定です。クリップボードリストは fc.clipboardList_key 変数で
# 設定したキーの押下により起動します。クリップボードリストを開いた後、C-f（→）や C-b（←）
# キーを入力することで画面を切り替えることができます。
# （参考：https://github.com/crftwr/keyhac/blob/master/_config.py）

# 定型文
fc.fixed_items = [
    ["---------+ x 8", "---------+" * 8],
    ["メールアドレス", "user_name@domain_name"],
    ["住所",           "〒999-9999 ＮＮＮＮＮＮＮＮＮＮ"],
    ["電話番号",       "99-999-9999"],
]
fc.fixed_items[0][0] = list_formatter.format(fc.fixed_items[0][0])

# 日時
fc.datetime_items = [
    ["YYYY/MM/DD HH:MM:SS", dateAndTime("%Y/%m/%d %H:%M:%S")],
    ["YYYY/MM/DD",          dateAndTime("%Y/%m/%d")],
    ["HH:MM:SS",            dateAndTime("%H:%M:%S")],
    ["YYYYMMDD_HHMMSS",     dateAndTime("%Y%m%d_%H%M%S")],
    ["YYYYMMDD",            dateAndTime("%Y%m%d")],
    ["HHMMSS",              dateAndTime("%H%M%S")],
]
fc.datetime_items[0][0] = list_formatter.format(fc.datetime_items[0][0])

fc.clipboardList_listers = [
    ["定型文", cblister_FixedPhrase(fc.fixed_items)],
    ["日時",   cblister_FixedPhrase(fc.datetime_items)],
]

# [section-clipboardList-2] ------------------------------------------------------------------------

####################################################################################################
## ランチャーリストの設定
####################################################################################################
# [section-lancherList-1] --------------------------------------------------------------------------

# ランチャー用のリストを利用するための設定です。ランチャーリストは lancherList_key 変数で
# 設定したキーの押下により起動します。ランチャーリストを開いた後、C-f（→）や C-b（←）
# キーを入力することで画面を切り替えることができます。
# （参考：https://github.com/crftwr/keyhac/blob/master/_config.py）

# アプリケーションソフト
fc.application_items = [
    ["Notepad",     keymap.ShellExecuteCommand(None, r"notepad.exe", "", "")],
    ["Explorer",    keymap.ShellExecuteCommand(None, r"explorer.exe", "", "")],
    ["Cmd",         keymap.ShellExecuteCommand(None, r"cmd.exe", "", "")],
    ["MSEdge",      keymap.ShellExecuteCommand(None, r"msedge.exe", "", "")],
    ["Chrome",      keymap.ShellExecuteCommand(None, r"chrome.exe", "", "")],
    ["Firefox",     keymap.ShellExecuteCommand(None, r"firefox.exe", "", "")],
    ["Thunderbird", keymap.ShellExecuteCommand(None, r"thunderbird.exe", "", "")],
]
fc.application_items[0][0] = list_formatter.format(fc.application_items[0][0])

# ウェブサイト
fc.website_items = [
    ["Google",          keymap.ShellExecuteCommand(None, r"https://www.google.co.jp/", "", "")],
    ["Facebook",        keymap.ShellExecuteCommand(None, r"https://www.facebook.com/", "", "")],
    ["Twitter",         keymap.ShellExecuteCommand(None, r"https://twitter.com/", "", "")],
    ["Keyhac",          keymap.ShellExecuteCommand(None, r"https://sites.google.com/site/craftware/keyhac-ja", "", "")],
    ["Fakeymacs",       keymap.ShellExecuteCommand(None, r"https://github.com/smzht/fakeymacs", "", "")],
    ["NTEmacs＠ウィキ", keymap.ShellExecuteCommand(None, r"https://w.atwiki.jp/ntemacs/", "", "")],
]
fc.website_items[0][0] = list_formatter.format(fc.website_items[0][0])

fc.lancherList_listers = [
    ["App",     cblister_FixedPhrase(fc.application_items)],
    ["Website", cblister_FixedPhrase(fc.website_items)],
    ["Other",   cblister_FixedPhrase(fc.other_items)],
]

# [section-lancherList-2] --------------------------------------------------------------------------

####################################################################################################
## 拡張機能の設定
####################################################################################################
# [section-extensions] -----------------------------------------------------------------------------

# https://github.com/smzht/fakeymacs/blob/master/fakeymacs_manuals/extensions.org

# --------------------------------------------------------------------------------------------------

# Chrome 系ブラウザで Ctl-x C-b を入力した際、Chrome の拡張機能 Quick Tabs を起動する
if 0:
    fc.chrome_list= ["chrome.exe",
                     "msedge.exe"]
    fc.quick_tabs_shortcut_key = "A-q"
    exec(readConfigExtension(r"chrome_quick_tabs\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# Emacs の shell-command-on-region の機能をサポートする
if 0:
    fc.unix_tool = "WSL"
    # fc.unix_tool = "MSYS2"
    # fc.unix_tool = "Cygwin"
    # fc.unix_tool = "BusyBox"
    # fc.bash_options = []
    fc.bash_options = ["-l"]
    exec(readConfigExtension(r"shell_command_on_region\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# VSCode 用のキーの設定を行う
if 1:
    fc.vscode_target  = ["Code.exe"]
    fc.vscode_target += ["chrome.exe",
                         "msedge.exe",
                         "firefox.exe",
                         ]

    # fc.vscode_prefix_key = [["C-;", "C-A-;"]]
    fc.use_ctrl_atmark_for_mark = False
    fc.use_direct_input_in_vscode_terminal = False
    fc.esc_mode_in_keyboard_quit = 1

    # VSCode Extension 用のキーの設定を行う
    fc.vscode_dired = False
    fc.vscode_recenter = False
    fc.vscode_recenter2 = False
    fc.vscode_occur = False
    fc.vscode_quick_select = True
    fc.vscode_input_sequence = True
    fc.vscode_insert_numbers = True
    fc.vscode_keyboard_macro = False
    fc.vscode_filter_text = False

    exec(readConfigExtension(r"vscode_key\config.py"), dict(globals(), **locals()))
    # vscode_extensions\config.py は、vscode_key\config.py 内部から呼ばれている

# --------------------------------------------------------------------------------------------------

# Everything を起動するキーを指定する
if 0:
    exec(readConfigExtension(r"everything\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# ブラウザをポップアップしてから、ブラウザのショートカットキーを入力するキーを設定する
if 0:
    fc.browser_list= ["chrome.exe",
                      "msedge.exe",
                      "firefox.exe"]
    exec(readConfigExtension(r"browser_key\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 指定したアプリケーションソフトに F2（編集モード移行）を割り当てるキーを設定する
if 0:
    exec(readConfigExtension(r"edit_mode\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# Emacs の場合、IME 切り替え用のキーを C-\ に置き換える
if 0:
    exec(readConfigExtension(r"real_emacs\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 英語キーボード設定をした OS 上で日本語キーボードを利用する場合の設定を行う
if 0:
    fc.change_keyboard_startup = "US"
    # fc.change_keyboard_startup = "JP"
    exec(readConfigExtension(r"change_keyboard\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 日本語キーボード設定をした OS 上で日本語キーボードを英語配列で利用する場合の設定を行う
if 0:
    fc.change_keyboard2_startup = "US"
    # fc.change_keyboard2_startup = "JP"
    exec(readConfigExtension(r"change_keyboard2\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# クリップボードに格納したファイルもしくはフォルダのパスを emacsclient で開く
if 0:
    fc.emacsclient_name = r"<emacsclient プログラムをインストールしている Windows のパス>\wslclient-n.exe"
    exec(readConfigExtension(r"emacsclient\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 指定したキーを押下したときに IME の状態を表示する
if 0:
    fc.pop_ime_balloon_key = ["C-;"]
    # fc.pop_ime_balloon_key = ["O-" + fc.side_of_ctrl_key + "Ctrl"] # Ctrl キーの単押し
    exec(readConfigExtension(r"pop_ime_balloon\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 60% US キーボードのキー不足（Delete キー、Backquote キー不足）の対策を行う
if 0:
    exec(readConfigExtension(r"compact_keyboard\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 半角と全角の入力を間違えた際、入力モードの切り替えと入力文字の変換を行う
if 0:
    exec(readConfigExtension(r"zenkaku_hankaku\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# Emacs キーバインドを利用しない設定のアプリで、メニューの操作用の Emacs キーバインドを設定する
if 0:
    fc.menu_target= ["ttermpro.exe", # TeraTerm
                     ]
    exec(readConfigExtension(r"menu_key\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 現在アクティブなウィンドウと同じプロセスのウィンドウを順に切り替えるキーを設定する
if 0:
    exec(readConfigExtension(r"window_switching_key\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# YouTube で Space による停止、再生が正しく機能しないことの暫定的な対策を行う
if 1:
    exec(readConfigExtension(r"youtube_space_key\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 旧 Microsoft IME を使って文節長を変更した際、文節の表示が正しく行われないアプリの対策を行う
if 1:
    exec(readConfigExtension(r"bunsetsu_correction\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------

# 拡張機能を追加する場合は、ここに挿入してください

# [section-extension-space_fn] ---------------------------------------------------------------------

# SpaceFN を実現する設定を行う
if 0:
    fc.space_fn_key = "Space"
    # fc.space_fn_key = "(29)" # 「無変換」キー
    # fc.space_fn_window_keymap_list = [keymap_emacs]
    # fc.space_fn_window_keymap_list += [keymap_ime]
    # fc.space_fn_window_keymap_list += [keymap_ei]
    # fc.space_fn_window_keymap_list += [fakeymacs.keymap_vscode]
    exec(readConfigExtension(r"space_fn\config.py"), dict(globals(), **locals()))

# --------------------------------------------------------------------------------------------------
