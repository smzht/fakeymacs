# -*- mode: python; coding: utf-8-with-signature-dos -*-

#########################################################################
##                              Fakeymacs
#########################################################################
##  Windows の操作を Emacs のキーバインドで行うための設定（Keyhac版）
#########################################################################

fakeymacs_version = "20220726_01"

import time
import os.path
import re
import fnmatch
import copy
import datetime
import ctypes
import pyauto
import winreg
import itertools

import keyhac_keymap
from keyhac import *

def configure(keymap):

    ####################################################################################################
    ## 初期設定
    ####################################################################################################

    keymap.editor = r"notepad.exe"
    keymap.setFont("ＭＳ ゴシック", 12)

    # カスタマイズパラメータを格納するクラスを定義する
    class FakeymacsConfig:
        pass

    fc = fakeymacs_config = FakeymacsConfig()

    # Fakeymacs を制御する変数を格納するクラスを定義する
    class Fakeymacs:
        pass

    fakeymacs = Fakeymacs()

    # OS に設定しているキーボードタイプの設定を行う
    # （http://tokovalue.jp/function/GetKeyboardType.htm）
    if ctypes.windll.user32.GetKeyboardType(0) == 7:
        os_keyboard_type = "JP"
    else:
        os_keyboard_type = "US"

    # 個人設定ファイルを読み込む
    try:
        with open(dataPath() + r"\config_personal.py", "r", encoding="utf-8-sig") as f:
            config_personal = f.read()
    except:
        print("個人設定ファイル config_personal.py は存在しないため、読み込みしていません")
        config_personal = ""

    def readConfigPersonal(section):
        if config_personal:
            # https://www.zu-min.com/archives/614
            m = re.search(r"(#\s{}.*?)(#\s\[section-|\Z)".format(re.escape(section)), config_personal,
                          flags=re.DOTALL)
            try:
                config_section = m.group(1)
                config_section = re.sub(r"^##.*", r"", config_section, flags=re.MULTILINE)
            except:
                print("個人設定ファイルのセクション {} の読み込みに失敗しました".format(section))
                config_section = ""
        else:
            config_section = ""

        return config_section

    def readConfigExtension(config_file, msg=True):
        try:
            with open(dataPath() + r"\fakeymacs_extensions\\" + config_file, "r", encoding="utf-8-sig") as f:
                config_extension = f.read()
        except:
            if msg:
                print("拡張機能ファイル {} の読み込みに失敗しました".format(config_file))
            config_extension = ""

        return config_extension

    def startupString():
        startup_string_formatter = "Fakeymacs version {}:\n  https://github.com/smzht/fakeymacs\n"
        return startup_string_formatter.format(fakeymacs_version)

    # 個人設定ファイルのセクション [section-init] を読み込んで実行する
    exec(readConfigPersonal("[section-init]"), dict(globals(), **locals()))


    ####################################################################################################
    ## 機能オプションの選択
    ####################################################################################################

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
    #   さらに Google日本語入力を利用している場合、keymap.getWindow().getImeStatus() が True を返すため、
    #   Emacs日本語入力モードの挙動がおかしくなります。この対策を行うかどうかを指定します。）
    fc.correct_ime_status = False

    # 上記の対策を行う Chromium 系ブラウザのプログラム名称を指定する
    fc.chromium_browser_list = ["chrome.exe",
                                "msedge.exe",
                                ]

    # 個人設定ファイルのセクション [section-options] を読み込んで実行する
    exec(readConfigPersonal("[section-options]"), dict(globals(), **locals()))


    ####################################################################################################
    ## 基本設定
    ####################################################################################################

    ###########################################################################
    ## キーボード関連変数の設定
    ###########################################################################

    if os_keyboard_type == "JP":
        try:
            if keymap.fakeymacs_keyboard == "JP":
                is_japanese_keyboard = True
                use_usjis_keyboard_conversion = False
            else:
                is_japanese_keyboard = False
                use_usjis_keyboard_conversion = True
        except:
            if fc.use_usjis_keyboard_conversion:
                is_japanese_keyboard = False
                use_usjis_keyboard_conversion = True
            else:
                is_japanese_keyboard = True
                use_usjis_keyboard_conversion = False
    else:
        is_japanese_keyboard = False
        use_usjis_keyboard_conversion = False


    ###########################################################################
    ## カスタマイズパラメータの設定
    ###########################################################################

    # すべてのキーマップを透過（スルー）するアプリケーションソフトを指定する
    fc.transparent_target   = ["mstsc.exe",                     # Remote Desktop
                               "MouseWithoutBordersHelper.exe", # Mouse Without Borders
                               ]

    # Emacs のキーバインドにするウィンドウのクラスネームを指定する（全ての設定に優先する）
    fc.emacs_target_class   = ["Edit"]                   # テキスト入力フィールドなどが該当

    # Emacs のキーバインドに“したくない”アプリケーションソフトを指定する
    # （Keyhac のメニューから「内部ログ」を ON にすると processname や classname を確認することができます）
    fc.not_emacs_target     = ["wsl.exe",                # WSL
                               "bash.exe",               # WSL
                               "ubuntu.exe",             # WSL
                               "ubuntu1604.exe",         # WSL
                               "ubuntu1804.exe",         # WSL
                               "ubuntu2004.exe",         # WSL
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
    #   利用することができます。）
    # （ここで指定したキーに新たに別のキー設定をしたいときには、define_key2 関数を利用してください）
    fc.skip_settings_key    = {"keymap_global"    : [], # 全画面共通 Keymap
                               "keymap_emacs"     : [], # Emacs キーバインド対象アプリ用 Keymap
                               "keymap_ime"       : [], # IME 切り替え専用アプリ用 Keymap
                               "keymap_ei"        : [], # Emacs 日本語入力モード用 Keymap
                               "keymap_tsw"       : [], # タスク切り替え画面用 Keymap
                               "keymap_lw"        : [], # リストウィンドウ用 Keymap
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

    # 左右どちらの Ctrlキーを使うかを指定する（"L": 左、"R": 右）
    fc.side_of_ctrl_key = "L"

    # 左右どちらの Altキーを使うかを指定する（"L": 左、"R": 右）
    fc.side_of_alt_key = "L"

    # 左右どちらの Winキーを使うかを指定する（"L": 左、"R": 右）
    fc.side_of_win_key = "L"

    # C-iキーを Tabキーとして使うかどうかを指定する（True: 使う、False: 使わない）
    fc.use_ctrl_i_as_tab = True

    # Escキーを Metaキーとして使うかどうかを指定する（True: 使う、False: 使わない）
    # （True（Metaキーとして使う）に設定されている場合、ESC の二回押下で ESC が入力されます）
    fc.use_esc_as_meta = False

    # Ctl-xプレフィックスキーに使うキーを指定する
    # （Ctl-xプレフィックスキーのモディファイアキーは、Ctrl または Alt のいずれかから指定してください）
    fc.ctl_x_prefix_key = "C-x"

    # スクロールに使うキーの組み合わせ（Up、Down の順）を指定する
    # fc.scroll_key = None # PageUp、PageDownキーのみを利用する
    fc.scroll_key = ["M-v", "C-v"]

    # Emacs日本語入力モードを使うかどうかを指定する（True: 使う、False: 使わない）
    fc.use_emacs_ime_mode = True

    # Emacs日本語入力モードが有効なときに表示するバルーンメッセージを指定する
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
    ## （Google日本語入力を利用する場合、Ctrl キーと組み合わせたキーを設定してください。「確定取り消し」
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

    ## Google日本語入力の場合
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
    # Emacs日本語入力モードを利用する際に、IME のショートカットを置き換えるキーの組み合わせ
    # （置き換え先、置き換え元）を指定する
    # （Microsoft IME で「ことえり」のキーバインドを利用するための設定例です。Google日本語入力で
    #   「ことえり」のキー設定になっている場合には不要ですが、設定を行っていても問題はありません。）
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

    ## Google日本語入力の場合
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
    # （emacs_target_class 変数に指定したクラス（初期値：Edit）に該当するアプリケーションソフト（Windows
    #   10版 Notepad など）は、Emacs キーバインドを切り替えの対象となりません（常に Emacs キーバインドと
    #   なります）。）
    fc.toggle_emacs_keybind_key = "C-S-Space"

    # アプリケーションキーとして利用するキーを指定する
    # （修飾キーに Alt は使えないようです）
    fc.application_key = None
    # fc.application_key = "O-RCtrl"
    # fc.application_key = "W-m"

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

    # ウィンドウを最小化、リストアするキーの組み合わせ（リストア、最小化 の順）を指定する（複数指定可）
    fc.window_minimize_key = []
    fc.window_minimize_key += [["A-S-m", "A-m"]]

    # 仮想デスクトップを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （仮想デスクトップを切り替えた際にフォーカスのあるウィンドウを適切に処理するため、設定するキーは
    #   Winキーとの組み合わせとしてください）
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
    fc.is_newline_selectable_in_Excel = False

    # Ctrl キー単押しで開く Ctrl ボタンを持つアプリケーションソフト（プロセス名称とクラス名称の
    # 組み合わせ（ワイルドカード指定可））を指定する
    # （Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
    #   開く機能があります。その挙動を抑制するアプリケーションソフトのリストを指定してください。）
    fc.ctrl_button_app_list = [["WINWORD.EXE",  "_WwG"],
                               ["EXCEL.EXE",    "EXCEL*"],
                               ["POWERPNT.EXE", "mdiClass"],
                               ]

    # ゲームなど、キーバインドの設定を極力行いたくないアプリケーションソフトを指定する
    # （keymap_global 以外のすべてのキーマップをスルーします。ゲームなど、Keyhac によるキー設定と
    #   相性が悪いアプリケーションソフトを指定してください。keymap_base の設定もスルーするため、
    #   英語 -> 日本語キーボード変換の機能が働かなくなることにご留意ください。）
    fc.game_app_list        = ["ffxiv_dx11.exe",         # FINAL FANTASY XIV
                               ]

    # 個人設定ファイルのセクション [section-base-1] を読み込んで実行する
    exec(readConfigPersonal("[section-base-1]"), dict(globals(), **locals()))


    ###########################################################################
    ## ウィンドウフォーカスが変わった時、すぐに Keyhac に検知させるための設定
    ###########################################################################

    # IME の状態をテキスト カーソル インジケーターの色で表現するときに必要となる設定
    # （https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook）
    # （https://sites.google.com/site/agkh6mze/howto/winevent）
    # （https://stackoverflow.com/questions/15849564/how-to-use-winapi-setwineventhook-in-python）
    # （https://github.com/Danesprite/windows-fun/blob/master/window%20change%20listener.py）
    # （https://tutorialmore.com/questions-652366.htm）
    # （https://www.nicovideo.jp/watch/sm20797948）

    def setWinEventHook():
        EVENT_SYSTEM_FOREGROUND = 0x0003
        WINEVENT_OUTOFCONTEXT   = 0x0000
        WINEVENT_SKIPOWNPROCESS = 0x0002

        user32 = ctypes.windll.user32
        ole32 = ctypes.windll.ole32

        try:
            # 設定されているか？
            keymap.fakeymacs_hook

            # reload 時の対策
            user32.UnhookWinEvent(keymap.fakeymacs_hook)
            ole32.CoUninitialize()
        except:
            pass

        ole32.CoInitialize(None)

        WinEventProcType = ctypes.WINFUNCTYPE(
            None,
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.HWND,
            ctypes.wintypes.LONG,
            ctypes.wintypes.LONG,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.DWORD
        )

        def callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
            if keymap.hook_enabled:
                delay(0.1)
                keymap._updateFocusWindow()
            else:
                setCursorColor(False)

        # この設定は必要（この設定がないと、Keyhac が落ちる場合がある）
        global WinEventProc

        WinEventProc = WinEventProcType(callback)

        user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        keymap.fakeymacs_hook = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            WinEventProc,
            0,
            0,
            WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS
        )

    # ウィンドウが切り替わるときのイベントフックを設定する
    setWinEventHook()


    ###########################################################################
    ## 日本語キーボード設定をした OS 上で英語キーボードを利用するための設定
    ###########################################################################

    if use_usjis_keyboard_conversion:
        str_vk_table = copy.copy(keyhac_keymap.KeyCondition.str_vk_table_common)
        for name in keyhac_keymap.KeyCondition.str_vk_table_jpn:
            del str_vk_table[name]
        str_vk_table.update(keyhac_keymap.KeyCondition.str_vk_table_std)

        vk_str_table = copy.copy(keyhac_keymap.KeyCondition.vk_str_table_common)
        for vk in keyhac_keymap.KeyCondition.vk_str_table_jpn:
            del vk_str_table[vk]
        vk_str_table.update(keyhac_keymap.KeyCondition.vk_str_table_std)

        def usjisTableSwap(swap):
            if swap:
                keyhac_keymap.KeyCondition.str_vk_table = str_vk_table
                keyhac_keymap.KeyCondition.vk_str_table = vk_str_table
            else:
                # table_common は table_jpn で update した状態となっているためこれで良い
                keyhac_keymap.KeyCondition.str_vk_table = keyhac_keymap.KeyCondition.str_vk_table_common
                keyhac_keymap.KeyCondition.vk_str_table = keyhac_keymap.KeyCondition.vk_str_table_common

        def usjisFilter(func, *param):
            usjisTableSwap(1)
            rtn = func(*param)
            usjisTableSwap(0)
            return rtn
    else:
        def usjisFilter(func, *param):
            rtn = func(*param)
            return rtn

    usjis_key_table = {"S-2"            : [["S-2"],                           "Atmark"        ], # @
                       "S-6"            : [["S-6"],                           "Caret"         ], # ^
                       "S-7"            : [["S-7"],                           "S-6"           ], # &
                       "S-8"            : [["S-8"],                           "S-Colon"       ], # *
                       "S-9"            : [["S-9"],                           "S-8"           ], # (
                       "S-0"            : [["S-0"],                           "S-9"           ], # )
                       "S-Minus"        : [["S-Minus"],                       "S-BackSlash"   ], # _
                       "Plus"           : [["Caret"],                         "S-Minus"       ], # =
                       "S-Plus"         : [["S-Caret"],                       "S-Semicolon"   ], # +
                       "OpenBracket"    : [["Atmark"],                        "OpenBracket"   ], # [
                       "S-OpenBracket"  : [["S-Atmark"],                      "S-OpenBracket" ], # {
                       "CloseBracket"   : [["OpenBracket"],                   "CloseBracket"  ], # ]
                       "S-CloseBracket" : [["S-OpenBracket"],                 "S-CloseBracket"], # }
                       "BackSlash"      : [["CloseBracket"],                  "Yen"           ], # \
                       "S-BackSlash"    : [["S-CloseBracket"],                "S-Yen"         ], # |
                       "S-Semicolon"    : [["S-Semicolon"],                   "Colon"         ], # :
                       "Quote"          : [["Colon"],                         "S-7"           ], # '
                       "S-Quote"        : [["S-Colon"],                       "S-2"           ], # "
                       "BackQuote"      : [["(243)", "(244)", "(248)"],       "S-Atmark"      ], # `
                       "S-BackQuote"    : [["S-(243)", "S-(244)", "S-(248)"], "S-Caret"       ], # ~
                       "(243)"          : [[],                                "(243)"         ],
                       "S-(243)"        : [[],                                "S-(243)"       ],
                       "(244)"          : [[],                                "(244)"         ],
                       "S-(244)"        : [[],                                "S-(244)"       ],
                       }

    def keyStrNormalization(key):
        nkey = usjisFilter(str, usjisFilter(keyhac_keymap.KeyCondition.fromString, key))
        if "D-" not in key:
            nkey = nkey.replace("D-", "")
        return nkey

    def usjisPos(key):
        key = keyStrNormalization(key)
        key_list = []
        match_flg = False
        if use_usjis_keyboard_conversion:
            for us_key in usjis_key_table:
                if re.search(r"(^|[^S]-){}$".format(re.escape(us_key)), key):
                    for jis_key in usjis_key_table[us_key][0]:
                        key_list.append(key.replace(us_key, jis_key))
                    match_flg = True
                    break
        if not match_flg:
            key_list.append(key)
        return key_list

    def usjisInput(key):
        key = keyStrNormalization(key)
        if use_usjis_keyboard_conversion:
            for us_key in usjis_key_table:
                if re.search(r"(^|[^S]-){}$".format(re.escape(us_key)), key):
                    jis_key = usjis_key_table[us_key][1]
                    key = key.replace(us_key, jis_key)
                    break
        return key


    ###########################################################################
    ## 基本機能の設定
    ###########################################################################

    fakeymacs.not_emacs_keybind = []
    fakeymacs.ime_cancel = False
    fakeymacs.last_window = None
    fakeymacs.clipboard_hook = True
    fakeymacs.last_keys = [None, None]
    fakeymacs.correct_ime_status = False
    fakeymacs.window_list = []

    def is_base_target(window):
        process_name = window.getProcessName()
        class_name   = window.getClassName()

        if window is not fakeymacs.last_window:
            if (process_name in fc.not_clipboard_target or
                any([checkWindow(None, c, None, window) for c in fc.not_clipboard_target_class])):
                # クリップボードの監視用のフックを無効にする
                keymap.clipboard_history.enableHook(False)
                fakeymacs.clipboard_hook = False
            else:
                # クリップボードの監視用のフックを有効にする
                keymap.clipboard_history.enableHook(True)
                fakeymacs.clipboard_hook = True

            if fc.correct_ime_status:
                if fc.ime == "Google_IME":
                    if process_name in fc.chromium_browser_list:
                        fakeymacs.correct_ime_status = True
                    else:
                        fakeymacs.correct_ime_status = False

            fakeymacs.ctrl_button_app = False
            for app in fc.ctrl_button_app_list:
                if checkWindow(*app):
                    fakeymacs.ctrl_button_app = True
                    break

            # Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
            # 開く機能がある。その挙動を抑制するための対策。
            if fakeymacs.ctrl_button_app:
                if fc.side_of_ctrl_key == "L":
                    keymap_base["D-LCtrl"] = "D-LCtrl", "(255)"
                else:
                    keymap_base["D-RCtrl"] = "D-RCtrl", "(255)"
            else:
                if fc.side_of_ctrl_key == "L":
                    keymap_base["D-LCtrl"] = "D-LCtrl"
                else:
                    keymap_base["D-RCtrl"] = "D-RCtrl"

        if (process_name in fc.transparent_target or
            (class_name not in fc.emacs_target_class and
             process_name in fc.game_app_list)):
            fakeymacs.is_keymap_decided = True
            return False
        else:
            fakeymacs.is_keymap_decided = False
            return True

    def is_emacs_target(window):
        last_window  = fakeymacs.last_window
        process_name = window.getProcessName()
        class_name   = window.getClassName()

        if window is not last_window:
            if process_name in fc.emacs_exclusion_key:
                fakeymacs.exclution_key = [keyStrNormalization(addSideOfModifierKey(specialCharToKeyStr(key)))
                                           for key in fc.emacs_exclusion_key[process_name]]
            else:
                fakeymacs.exclution_key = []

            reset_undo(reset_counter(reset_mark(lambda: None)))()
            fakeymacs.ime_cancel = False
            fakeymacs.last_window = window

        if is_task_switching_window(window):
            fakeymacs.is_keymap_decided = True
            return False

        if is_list_window(window):
            fakeymacs.is_keymap_decided = True
            return False

        if window is not last_window:
            showImeStatus(window.getImeStatus(), window=window)

        if (fakeymacs.is_keymap_decided == True or
            (class_name not in fc.emacs_target_class and
             (process_name in fakeymacs.not_emacs_keybind or
              process_name in fc.not_emacs_target))):
            fakeymacs.keybind = "not_emacs"
            return False
        else:
            fakeymacs.is_keymap_decided = True
            fakeymacs.keybind = "emacs"
            return True

    def is_ime_target(window):
        if (fakeymacs.is_keymap_decided == False and
            (window.getProcessName() in fakeymacs.not_emacs_keybind or
             window.getProcessName() in fc.ime_target)):
            return True
        else:
            return False

    keymap_base = keymap.defineWindowKeymap(check_func=is_base_target)

    if fc.use_emacs_ime_mode:
        keymap_emacs = keymap.defineWindowKeymap(check_func=lambda wnd: is_emacs_target(wnd) and not is_emacs_ime_mode(wnd))
        keymap_ime   = keymap.defineWindowKeymap(check_func=lambda wnd: is_ime_target(wnd)   and not is_emacs_ime_mode(wnd))
    else:
        keymap_emacs = keymap.defineWindowKeymap(check_func=is_emacs_target)
        keymap_ime   = keymap.defineWindowKeymap(check_func=is_ime_target)

    # mark がセットされると True になる
    fakeymacs.is_marked = False

    # リージョンを拡張する際に、順方向に拡張すると True、逆方向に拡張すると False になる
    fakeymacs.forward_direction = None

    # 検索が開始されると True になる
    fakeymacs.is_searching = False

    # キーボードマクロの play 中 は True になる
    fakeymacs.is_playing_kmacro = False

    # universal-argument コマンドが実行されると True になる
    fakeymacs.is_universal_argument = False

    # digit-argument コマンドが実行されると True になる
    fakeymacs.is_digit_argument = False

    # コマンドのリピート回数を設定する
    fakeymacs.repeat_counter = 1

    # undo のモードの時 True になる（redo のモードの時 False になる）
    fakeymacs.is_undo_mode = True

    # ウィンドウのリストアが最小化した順番の逆順となるように制御する
    fakeymacs.reverse_window_to_restore = False

    # Ctl-xプレフィックスキーを構成するキーの仮想キーコードを設定する
    if fc.ctl_x_prefix_key:
        keyCondition = usjisFilter(keyhac_keymap.KeyCondition.fromString, fc.ctl_x_prefix_key)

        if keyCondition.mod == MODKEY_CTRL:
            if fc.side_of_ctrl_key == "L":
                ctl_x_prefix_vkey = [VK_LCONTROL, keyCondition.vk]
            else:
                ctl_x_prefix_vkey = [VK_RCONTROL, keyCondition.vk]

        elif keyCondition.mod == MODKEY_ALT:
            if fc.side_of_alt_key == "L":
                ctl_x_prefix_vkey = [VK_LMENU, keyCondition.vk]
            else:
                ctl_x_prefix_vkey = [VK_RMENU, keyCondition.vk]
        else:
            print("Ctl-xプレフィックスキーのモディファイアキーは、Ctrl または Alt のいずれかから指定してください")

    ##################################################
    ## Emacs キーバインドの切り替え
    ##################################################

    def toggle_emacs_keybind():
        class_name   = keymap.getWindow().getClassName()
        process_name = keymap.getWindow().getProcessName()

        if (class_name not in fc.emacs_target_class and
            process_name not in fc.not_emacs_target):
            if process_name in fakeymacs.not_emacs_keybind:
                fakeymacs.not_emacs_keybind.remove(process_name)
                keymap.popBalloon("keybind", "[Enable Emacs keybind]", 1000)
            else:
                fakeymacs.not_emacs_keybind.append(process_name)
                keymap.popBalloon("keybind", "[Disable Emacs keybind]", 1000)

            keymap.updateKeymap()

    ##################################################
    ## IME の操作
    ##################################################

    def enable_input_method():
        set_input_method(1)

    def disable_input_method():
        set_input_method(0)

    def toggle_input_method():
        set_input_method(getImeStatus() ^ 1)

    def set_input_method(ime_status):
        correctImeStatus()

        if getImeStatus() != ime_status:
            # IME を切り替える
            # （setImeStatus(ime_status) を使わないのは、キーボードマクロの再生時に影響がでるため）
            # self_insert_command("A-(25)")() # 日本語キーボードで PowerShell を使った際に @ が
            #                                 # 表示されるため、次行に変更
            self_insert_command("(244)")()

            if fakeymacs.is_playing_kmacro:
                delay(0.2)

        showImeStatus(ime_status)

    def getImeStatus():
        return keymap.getWindow().getImeStatus()

    def setImeStatus(ime_status):
        keymap.getWindow().setImeStatus(ime_status)
        setCursorColor(ime_status)

    def showImeStatus(ime_status, force=False, window=None):
        setCursorColor(ime_status)
        popImeBalloon(ime_status, force, window)

    def correctImeStatus():
        # Chromium 系ブラウザで発生する問題の対策を行う
        if fakeymacs.correct_ime_status:
            if getImeStatus():
                setImeStatus(0) # この行は必要
                setImeStatus(1)

    def setCursorColor(ime_status):
        if fc.use_ime_status_cursor_color:
            if ime_status:
                cursor_color = fc.ime_on_cursor_color
            else:
                cursor_color = fc.ime_off_cursor_color

            # https://docs.python.org/ja/3/library/winreg.html
            # https://itasuke.hatenablog.com/entry/2018/01/08/133510
            with winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER,
                                  r"Software\Microsoft\Accessibility\CursorIndicator",
                                  access=winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, "IndicatorColor", 0, winreg.REG_DWORD, cursor_color)

    def popImeBalloon(ime_status, force=False, window=None):
        if not fakeymacs.is_playing_kmacro:
            if force or fc.use_ime_status_balloon:
                # LINE アプリなど、Qt5152QWindowIcon にマッチするクラスをもつアプリは入力文字に
                # バルーンヘルプが被るので、バルーンヘルプの表示対象から外す
                # （ただし、force が True の場合は除く）
                if force or not checkWindow(None, "Qt5152QWindowIcon", window=window):
                    if ime_status:
                        message = fc.ime_status_balloon_message[1]
                    else:
                        message = fc.ime_status_balloon_message[0]

                    try:
                        # IME の状態をバルーンヘルプで表示する
                        keymap.popBalloon("ime_status", message, 500)
                    except:
                        pass

    def reconversion():
        if fakeymacs.ime_cancel:
            self_insert_command(fc.ime_cancel_key)()
            if fc.use_emacs_ime_mode:
                enable_emacs_ime_mode(100)
        else:
            if fc.ime_reconv_region:
                if fakeymacs.forward_direction is not None:
                    self_insert_command(fc.ime_reconv_key)()
                    if fc.use_emacs_ime_mode:
                        enable_emacs_ime_mode()
            else:
                self_insert_command(fc.ime_reconv_key)()
                if fc.use_emacs_ime_mode:
                    enable_emacs_ime_mode()

    ##################################################
    ## ファイル操作
    ##################################################

    def find_file():
        self_insert_command("C-o")()

    def save_buffer():
        self_insert_command("C-s")()

    def write_file():
        # https://www.sriproot.net/blog/ctrl-shift-s-saveas-922
        # self_insert_command("C-S-s")()

        self_insert_command("A-f")()
        delay()
        self_insert_command("a")()

    def dired():
        keymap.ShellExecuteCommand(None, r"explorer.exe", "", "")()

    ##################################################
    ## カーソル移動
    ##################################################

    def backward_char():
        self_insert_command("Left")()

    def forward_char():
        self_insert_command("Right")()

    def backward_word():
        self_insert_command("C-Left")()

    def forward_word():
        self_insert_command("C-Right")()

    def previous_line():
        self_insert_command("Up")()

    def next_line():
        self_insert_command("Down")()

    def move_beginning_of_line():
        self_insert_command("Home")()

    def move_end_of_line():
        self_insert_command("End")()
        if (checkWindow("WINWORD.EXE", "_WwG") or      # Microsoft Word
            checkWindow("POWERPNT.EXE", "mdiClass") or # Microsoft PowerPoint
            (checkWindow("EXCEL.EXE", "EXCEL*") and    # Microsoft Excel
             fc.is_newline_selectable_in_Excel)):
            if fakeymacs.is_marked:
                self_insert_command("Left")()

    def beginning_of_buffer():
        self_insert_command("C-Home")()

    def end_of_buffer():
        self_insert_command("C-End")()

    def goto_line():
        if (checkWindow("sakura.exe", "EditorClient") or # Sakura Editor
            checkWindow("sakura.exe", "SakuraView*")):   # Sakura Editor
            self_insert_command3("C-j")()
        else:
            self_insert_command3("C-g")()

    def scroll_up():
        self_insert_command("PageUp")()

    def scroll_down():
        self_insert_command("PageDown")()

    def recenter():
        if (checkWindow("sakura.exe", "EditorClient") or # Sakura Editor
            checkWindow("sakura.exe", "SakuraView*")):   # Sakura Editor
            self_insert_command("C-h")()

    ##################################################
    ## カット / コピー / 削除 / アンドゥ
    ##################################################

    def delete_backward_char():
        self_insert_command("Back")()

    def delete_char():
        self_insert_command("Delete")()

    def backward_kill_word(repeat=1):
        resetRegion()
        fakeymacs.is_marked = True

        def move_beginning_of_region():
            for _ in range(repeat):
                backward_word()

        mark(move_beginning_of_region, False)()
        delay()
        kill_region()

    def kill_word(repeat=1):
        resetRegion()
        fakeymacs.is_marked = True

        def move_end_of_region():
            for _ in range(repeat):
                forward_word()

        mark(move_end_of_region, True)()
        delay()
        kill_region()

    def kill_line(repeat=1):
        resetRegion()
        fakeymacs.is_marked = True

        if repeat == 1:
            mark(move_end_of_line, True)()
            delay()

            if (checkWindow("cmd.exe", "ConsoleWindowClass") or       # Cmd
                checkWindow("powershell.exe", "ConsoleWindowClass")): # PowerShell
                kill_region()

            elif checkWindow(None, "HM32CLIENT"): # Hidemaru Software
                kill_region()
                delay()
                if getClipboardText() == "":
                    self_insert_command("Delete")()
            else:
                # 改行を消せるようにするため Cut にはしていない
                copyRegion()
                self_insert_command("Delete")()
        else:
            def move_end_of_region():
                if checkWindow("WINWORD.EXE", "_WwG"): # Microsoft Word
                    for _ in range(repeat):
                        next_line()
                    move_beginning_of_line()
                else:
                    for _ in range(repeat - 1):
                        next_line()
                    move_end_of_line()
                    forward_char()

            mark(move_end_of_region, True)()
            delay()
            kill_region()

    def kill_region():
        # コマンドプロンプトには Cut に対応するショートカットがない。その対策。
        if checkWindow("cmd.exe", "ConsoleWindowClass"): # Cmd
            copyRegion()

            if fakeymacs.forward_direction is not None:
                if fakeymacs.forward_direction:
                    key = "Delete"
                else:
                    key = "Back"

                delay()
                for _ in range(len(getClipboardText())):
                    self_insert_command(key)()
        else:
            cutRegion()

    def kill_ring_save():
        copyRegion()
        resetRegion()

    def yank():
        self_insert_command("C-v")()

    def undo():
        # redo（C-y）の機能を持っていないアプリケーションソフトは常に undo とする
        if checkWindow("notepad.exe", "Edit"): # Windows 10版 Notepad
            self_insert_command("C-z")()
        else:
            if fakeymacs.is_undo_mode:
                self_insert_command("C-z")()
            else:
                self_insert_command("C-y")()

    def set_mark_command():
        if fakeymacs.is_marked or fakeymacs.forward_direction is not None:
            resetRegion()
            fakeymacs.is_marked = False
            fakeymacs.forward_direction = None
        else:
            fakeymacs.is_marked = True

    def mark_whole_buffer():
        if checkWindow("cmd.exe", "ConsoleWindowClass"): # Cmd
            # "Home", "C-a" では上手く動かない場合がある
            self_insert_command("Home", "S-End")()
            fakeymacs.forward_direction = True # 逆の設定にする

        elif checkWindow("powershell.exe", "ConsoleWindowClass"): # PowerShell
            self_insert_command("End", "S-Home")()
            fakeymacs.forward_direction = False

        elif (checkWindow("EXCEL.EXE", "EXCEL*") or # Microsoft Excel
              checkWindow(None, "Edit")):           # Edit クラス
            self_insert_command("C-End", "C-S-Home")()
            fakeymacs.forward_direction = False
        else:
            self_insert_command("C-Home", "C-a")()
            fakeymacs.forward_direction = False

        fakeymacs.is_marked = True

    def mark_page():
        mark_whole_buffer()

    ##################################################
    ## テキストの入れ替え
    ##################################################

    def transpose_chars():
        # Microsoft Excel の場合、セルの編集中（ウインドウのタイトル文字列が空）でなければ終了する
        if checkWindow("EXCEL.EXE", "EXCEL*", "?*"):
            return

        if fakeymacs.clipboard_hook:
            # クリップボードの監視用のフックを無効にする
            keymap.clipboard_history.enableHook(False)

        resetRegion()

        mark2(forward_char, True)()
        setClipboardText("")
        self_insert_command("C-c")()
        delay(0.05)

        clipboard_text = getClipboardText()

        if len(clipboard_text) != 1:
            if clipboard_text == "\r\n":
                backward_char()

            mark2(backward_char, False)()
            setClipboardText("")
            self_insert_command("C-c")()

        self_insert_command("Delete")()
        backward_char()
        yank()
        forward_char()

        if fakeymacs.clipboard_hook:
            # クリップボードの監視用のフックを有効にする
            keymap.clipboard_history.enableHook(True)

    ##################################################
    ## バッファ / ウィンドウ操作
    ##################################################

    def kill_buffer():
        self_insert_command("C-F4")()

    def switch_to_buffer():
        self_insert_command("C-Tab")()

    def other_window():
        window_list = getWindowList(False)

        if len(window_list) >= 2:
            popWindow(window_list[1])()

    ##################################################
    ## 文字列検索 / 置換
    ##################################################

    def isearch(direction):
        if checkWindow("powershell.exe", "ConsoleWindowClass"): # PowerShell
            self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
        else:
            if fakeymacs.is_searching:
                if checkWindow("EXCEL.EXE"): # Microsoft Excel
                    if checkWindow(None, "EDTBX"): # 検索ウィンドウ
                        self_insert_command({"backward":"A-S-f", "forward":"A-f"}[direction])()
                    else:
                        self_insert_command("C-f")()
                else:
                    self_insert_command({"backward":"S-F3", "forward":"F3"}[direction])()
            else:
                self_insert_command("C-f")()
                fakeymacs.is_searching = True

    def isearch_backward():
        isearch("backward")

    def isearch_forward():
        isearch("forward")

    def query_replace():
        if (checkWindow("sakura.exe", "EditorClient") or  # Sakura Editor
            checkWindow("sakura.exe", "SakuraView*")  or  # Sakura Editor
            checkWindow(None, "HM32CLIENT")):             # Hidemaru Software
            self_insert_command("C-r")()
        else:
            self_insert_command("C-h")()

    ##################################################
    ## キーボードマクロ
    ##################################################

    def kmacro_start_macro():
        setImeStatus(0)
        keymap.command_RecordStart()

    def kmacro_end_macro():
        keymap.command_RecordStop()
        # キーボードマクロの終了キー「Ctl-xプレフィックスキー + ")"」の Ctl-xプレフィックスキーがマクロに
        # 記録されてしまうのを対策する（キーボードマクロの終了キーの前提を「Ctl-xプレフィックスキー + ")"」
        # としていることについては、とりあえず了承ください。）
        if fc.ctl_x_prefix_key and len(keymap.record_seq) >= 4:
            if (((keymap.record_seq[len(keymap.record_seq) - 1] == (ctl_x_prefix_vkey[0], True) and
                  keymap.record_seq[len(keymap.record_seq) - 2] == (ctl_x_prefix_vkey[1], True)) or
                 (keymap.record_seq[len(keymap.record_seq) - 1] == (ctl_x_prefix_vkey[1], True) and
                  keymap.record_seq[len(keymap.record_seq) - 2] == (ctl_x_prefix_vkey[0], True))) and
                keymap.record_seq[len(keymap.record_seq) - 3] == (ctl_x_prefix_vkey[1], False)):
                   keymap.record_seq.pop()
                   keymap.record_seq.pop()
                   keymap.record_seq.pop()
                   if keymap.record_seq[len(keymap.record_seq) - 1] == (ctl_x_prefix_vkey[0], False):
                       for i in range(len(keymap.record_seq) - 1, -1, -1):
                           if keymap.record_seq[i] == (ctl_x_prefix_vkey[0], False):
                               keymap.record_seq.pop()
                           else:
                               break
                   else:
                       # コントロール系の入力が連続して行われる場合があるための対処
                       keymap.record_seq.append((ctl_x_prefix_vkey[0], True))

    def kmacro_end_and_call_macro():
        def callKmacro():
            # キーボードマクロの最初が IME ON の場合、この delay が必要
            delay(0.2)
            fakeymacs.is_playing_kmacro = True
            setImeStatus(0)
            keymap.command_RecordPlay()
            fakeymacs.is_playing_kmacro = False

        keymap.delayedCall(callKmacro, 0)

    ##################################################
    ## その他
    ##################################################

    def escape():
        self_insert_command("Esc")()

    def space():
        if (fc.ime_reconv_key is None or
            fakeymacs.forward_direction is None):
            self_insert_command("Space")()
        else:
            reconversion()

    def newline():
        self_insert_command("Enter")()
        if not fc.use_emacs_ime_mode:
            if getImeStatus():
                fakeymacs.ime_cancel = True

    def newline_and_indent():
        self_insert_command("Enter", "Tab")()

    def open_line():
        self_insert_command("Enter", "Up", "End")()

    def indent_for_tab_command():
        self_insert_command("Tab")()

    def keyboard_quit(esc=True):
        resetRegion()

        if esc:
            # Esc を発行して問題ないアプリケーションソフトには Esc を発行する
            if not (checkWindow("cmd.exe", "ConsoleWindowClass") or        # Cmd
                    checkWindow("powershell.exe", "ConsoleWindowClass") or # PowerShell
                    checkWindow("EXCEL.EXE", "EXCEL*", "") or              # Microsoft Excel のセル編集
                    checkWindow("Evernote.exe", "WebViewHost") or          # Evernote
                    checkWindow("Notepad.exe", "RichEditD2DPT")):          # Windows 11版 Notepad
                escape()

        keymap.command_RecordStop()

        if fakeymacs.forward_direction is None:
            if fakeymacs.is_undo_mode:
                fakeymacs.is_undo_mode = False
            else:
                fakeymacs.is_undo_mode = True

    def kill_emacs():
        # Excel のファイルを開いた直後一回目、kill_emacs が正常に動作しない。その対策。
        self_insert_command("D-Alt", "F4")()
        delay(0.1)
        self_insert_command("U-Alt")()

    def universal_argument():
        if fakeymacs.is_universal_argument:
            if fakeymacs.is_digit_argument:
                fakeymacs.is_universal_argument = False
            else:
                fakeymacs.repeat_counter *= 4
        else:
            fakeymacs.is_universal_argument = True
            fakeymacs.repeat_counter *= 4

    def digit_argument(number):
        if fakeymacs.is_digit_argument:
            fakeymacs.repeat_counter = fakeymacs.repeat_counter * 10 + number
        else:
            fakeymacs.repeat_counter = number
            fakeymacs.is_digit_argument = True

    def shell_command():
        command_name = os.path.basename(fc.command_name)
        for window in getWindowList():
            if window.getProcessName() == command_name:
                popWindow(window)()
                return

        keymap.ShellExecuteCommand(None, fc.command_name, "", "")()

    ##################################################
    ## 共通関数
    ##################################################

    def delay(sec=0.02):
        time.sleep(sec)

    def copyRegion():
        self_insert_command("C-c")()
        # C-k (kill_line) したときに k 文字が混在することがあるための対策
        keymap.delayedCall(pushToClipboardList, 100)

    def cutRegion():
        self_insert_command("C-x")()
        # C-k (kill_line) したときに k 文字が混在することがあるための対策
        keymap.delayedCall(pushToClipboardList, 100)

    def pushToClipboardList():
        # clipboard 監視の対象外とするアプリケーションソフトで copy / cut した場合でも
        # クリップボードの内容をクリップボードリストに登録する
        if not fakeymacs.clipboard_hook:
            clipboard_text = getClipboardText()
            if clipboard_text:
                keymap.clipboard_history._push(clipboard_text)

    def resetRegion():
        if fakeymacs.forward_direction is not None:

            if checkWindow(None, "Edit"): # Edit クラス
                # 選択されているリージョンのハイライトを解除するためにカーソルキーを発行する
                if fakeymacs.forward_direction:
                    self_insert_command("Right")()
                else:
                    self_insert_command("Left")()

            elif (checkWindow("cmd.exe", "ConsoleWindowClass") or # Cmd
                  checkWindow("EXCEL.EXE", "EXCEL*", "?*")):      # Microsoft Excel のセル編集でない場合
                # 選択されているリージョンのハイライトを解除するためにカーソルを移動する
                if fakeymacs.forward_direction:
                    self_insert_command("Right", "Left")()
                else:
                    self_insert_command("Left", "Right")()

            elif checkWindow("powershell.exe", "ConsoleWindowClass"): # PowerShell
                # 選択されているリージョンのハイライトを解除するためにカーソルを移動する
                if fakeymacs.forward_direction:
                    self_insert_command("Left", "Right")()
                else:
                    self_insert_command("Right", "Left")()

            # Microsoft Excel 2019 より前のバージョンでは必要な設定の可能性あり
            # elif checkWindow("EXCEL.EXE"): # Microsoft Excel
            #     # 選択されているリージョンのハイライトを解除するためにカーソルを移動する
            #     if fakeymacs.forward_direction:
            #         self_insert_command("Left", "Right")()
            #     else:
            #         self_insert_command("Right", "Left")()

            else:
                # 選択されているリージョンのハイライトを解除するためにカーソルキーを発行する
                if fakeymacs.forward_direction:
                    self_insert_command("Right")()
                else:
                    self_insert_command("Left")()

    def checkWindow(process_name=None, class_name=None, text=None, window=None):
        if window is None:
            window = keymap.getWindow()
        return ((process_name is None or fnmatch.fnmatch(window.getProcessName(), process_name)) and
                (class_name is None or fnmatch.fnmatchcase(window.getClassName(), class_name)) and
                (text is None or fnmatch.fnmatchcase(window.getText(), text)))

    def vkeys():
        vkeys = list(usjisFilter(lambda: keyhac_keymap.KeyCondition.vk_str_table))
        for vkey in [VK_MENU, VK_LMENU, VK_RMENU, VK_CONTROL, VK_LCONTROL, VK_RCONTROL, VK_SHIFT, VK_LSHIFT, VK_RSHIFT, VK_LWIN, VK_RWIN]:
            vkeys.remove(vkey)
        return vkeys

    def vkToStr(vkey):
        return usjisFilter(keyhac_keymap.KeyCondition.vkToStr, vkey)

    def strToVk(name):
        return usjisFilter(keyhac_keymap.KeyCondition.strToVk, name)

    special_char_key_table = {"!"  : ["S-1",            "S-1"],
                              "@"  : ["S-2",            "Atmark"],
                              "#"  : ["S-3",            "S-3"],
                              "$"  : ["S-4",            "S-4"],
                              "%"  : ["S-5",            "S-5"],
                              "^"  : ["S-6",            "Caret"],
                              "&"  : ["S-7",            "S-6"],
                              "*"  : ["S-8",            "S-Colon"],
                              "("  : ["S-9",            "S-8"],
                              ")"  : ["S-0",            "S-9"],
                              "-"  : ["Minus",          "Minus"],
                              "_"  : ["S-Minus",        "S-BackSlash"],
                              "="  : ["Plus",           "S-Minus"],
                              "+"  : ["S-Plus",         "S-Semicolon"],
                              "["  : ["OpenBracket",    "OpenBracket"],
                              "{"  : ["S-OpenBracket",  "S-OpenBracket"],
                              "]"  : ["CloseBracket",   "CloseBracket"],
                              "}"  : ["S-CloseBracket", "S-CloseBracket"],
                              "\\" : ["BackSlash",      "Yen"],
                              "|"  : ["S-BackSlash",    "S-Yen"],
                              ";"  : ["Semicolon",      "Semicolon"],
                              ":"  : ["S-Semicolon",    "Colon"],
                              "'"  : ["Quote",          "S-7"],
                              '"'  : ["S-Quote",        "S-2"],
                              ","  : ["Comma",          "Comma"],
                              "<"  : ["S-Comma",        "S-Comma"],
                              "."  : ["Period",         "Period"],
                              ">"  : ["S-Period",       "S-Period"],
                              "/"  : ["Slash",          "Slash"],
                              "?"  : ["S-Slash",        "S-Slash"],
                              "`"  : ["BackQuote",      "S-Atmark"],
                              "~"  : ["S-BackQuote",    "S-Caret"],
                              }

    def specialCharToKeyStr(key):
        for special_char in special_char_key_table:
            if re.search(r"(^|-){}$".format(re.escape(special_char)), key):
                if is_japanese_keyboard:
                    str = special_char_key_table[special_char][1]
                else:
                    str = special_char_key_table[special_char][0]
                # key = re.sub(r"{}$".format(re.escape(special_char)), str, key)
                key = key[:-1] + str # 一文字の変換であれば、こちらの方が速い
                break
        return key

    def addSideOfModifierKey(key):
        key = re.sub(r"(^|-)(C-)", r"\1" + fc.side_of_ctrl_key + r"\2", key)
        key = re.sub(r"(^|-)(A-)", r"\1" + fc.side_of_alt_key  + r"\2", key)
        key = re.sub(r"(^|-)(W-)", r"\1" + fc.side_of_win_key  + r"\2", key)
        return key

    def kbd(keys):
        key_lists = []

        if keys:
            key_list0 = []
            key_list1 = []
            key_list2 = []

            for key in map(specialCharToKeyStr, keys.split()):
                if key == "Ctl-x":
                    key = fc.ctl_x_prefix_key

                if key == "M-":
                    key_list0 = []
                    if fc.use_esc_as_meta:
                        key_list2 = copy.copy(key_list1)
                        key_list2.append("Esc")
                    key_list1.append("C-OpenBracket")
                    break

                if "M-" in key:
                    key_list0.append(key.replace("M-", "A-"))
                    key_list1.append("C-OpenBracket")
                    key_list1.append(key.replace("M-", ""))
                else:
                    key_list0.append(key)
                    key_list1.append(key)

            if key_list0:
                key_lists.append(key_list0)

            if key_list0 != key_list1:
                key_lists.append(key_list1)

            if key_list2:
                key_lists.append(key_list2)

            for key_list in key_lists:
                key_list[0] = addSideOfModifierKey(key_list[0])

        return key_lists

    def keyPos(key_list):
        return list(itertools.product(*map(usjisPos, key_list)))

    def keyInput(key_list):
        return list(map(usjisInput, key_list))

    def define_key(window_keymap, keys, command, skip_check=True):
        nonlocal keymap_global
        nonlocal keymap_emacs
        nonlocal keymap_ime
        nonlocal keymap_ei
        nonlocal keymap_tsw
        nonlocal keymap_lw

        if keys is None:
            return

        if skip_check:
            # 設定をスキップするキーの処理を行う
            for keymap_name in fc.skip_settings_key:
                if (keymap_name in locals() and
                    window_keymap is locals()[keymap_name]):
                    for skey in fc.skip_settings_key[keymap_name]:
                        if fnmatch.fnmatch(keys, skey):
                            print("skip settings key : [" + keymap_name + "] " + keys)
                            return
                    break

        def keyCommand(key):
            nonlocal keymap_emacs

            if callable(command):
                if (key is not None and
                    "keymap_emacs" in locals() and
                    window_keymap is locals()["keymap_emacs"]):

                    ckey = keyStrNormalization(key)
                    def _command1():
                        fakeymacs.update_last_keys = True
                        if ckey in fakeymacs.exclution_key:
                            InputKeyCommand(key)()
                        else:
                            command()
                        if fakeymacs.update_last_keys:
                            fakeymacs.last_keys = [window_keymap, keys]
                else:
                    def _command1():
                        fakeymacs.update_last_keys = True
                        command()
                        if fakeymacs.update_last_keys:
                            fakeymacs.last_keys = [window_keymap, keys]

                def _command3():
                    if fakeymacs.repeat_counter == 1 or fakeymacs.is_playing_kmacro:
                        _command1()
                    else:
                        def _command2():
                            # モディファイアを離す（keymap.command_RecordPlay 関数を参考）
                            modifier = keymap.modifier
                            input_seq = []
                            for vk_mod in keymap.vk_mod_map.items():
                                if keymap.modifier & vk_mod[1]:
                                    input_seq.append(pyauto.KeyUp(vk_mod[0]))
                            pyauto.Input.send(input_seq)
                            keymap.modifier = 0

                            _command1()

                            # モディファイアを戻す（keymap.command_RecordPlay 関数を参考）
                            keymap.modifier = 0
                            input_seq = []
                            for vk_mod in keymap.vk_mod_map.items():
                                # 「Time stamp Inversion happend.」メッセージがでると、キーの繰り返し入力後に
                                # Shiftキーが押されたままの状態となる。根本的な対策ではないが、Shiftキーの
                                # 押下の状態の復元を除外することで、暫定的な対策とする。
                                # （Shiftキーは押しっぱなしにするキーではないので、押した状態を復元しなくとも
                                #   ほとんどの場合、問題は起きない）
                                if vk_mod[0] not in [VK_LSHIFT, VK_RSHIFT]:
                                    if modifier & vk_mod[1]:
                                        input_seq.append(pyauto.KeyDown(vk_mod[0]))
                                        keymap.modifier |= vk_mod[1]
                            pyauto.Input.send(input_seq)

                        keymap.delayedCall(_command2, 0)
                return _command3
            else:
                return command

        for key_list in kbd(keys):
            for pos_list in keyPos(key_list):
                if len(pos_list) == 1:
                    window_keymap[pos_list[0]] = keyCommand(key_list[0])

                    # Alt キーを単押しした際に、カーソルがメニューへ移動しないようにするための対策
                    # （https://www.haijin-boys.com/discussions/4583）
                    if re.match(r"O-LAlt$", pos_list[0], re.IGNORECASE):
                        window_keymap["D-LAlt"] = "D-LAlt", "(255)"

                    elif re.match(r"O-RAlt$", pos_list[0], re.IGNORECASE):
                        window_keymap["D-RAlt"] = "D-RAlt", "(255)"
                else:
                    w_keymap = window_keymap
                    for key in pos_list[:-1]:
                        w_keymap = w_keymap[key]
                    w_keymap[pos_list[-1]] = keyCommand(None)

    def define_key2(window_keymap, keys, command):
        define_key(window_keymap, keys, command, skip_check=False)

    def define_key3(window_keymap, keys, command, check_func):
        define_key(window_keymap, keys, makeKeyCommand(window_keymap, keys, command, check_func))

    def mergeMultiStrokeKeymap(window_keymap1, window_keymap2, keys):
        try:
            key_list = kbd(keys)[0]
            pos_list = keyPos(key_list)[0]
            for key in pos_list:
                window_keymap1 = window_keymap1[key]
                window_keymap2 = window_keymap2[key]
            window_keymap1.keymap = {**window_keymap2.keymap, **window_keymap1.keymap}
        except:
            pass

    def getKeyCommand(window_keymap, keys):
        try:
            key_list = kbd(keys)[-1]
            pos_list = keyPos(key_list)[0]
            for key in pos_list:
                window_keymap = window_keymap[key]
            func = window_keymap
        except:
            func = None

        return func

    def makeKeyCommand(window_keymap, keys, command, check_func):
        func = getKeyCommand(window_keymap, keys)
        if func is None:
            key_list = kbd(keys)[0]
            if len(key_list) == 1:
                func = InputKeyCommand(key_list[0])
            else:
                func = lambda: None

        def _func():
            if check_func():
                command()
            else:
                func()
        return _func

    def InputKeyCommand(*key_list, usjis_conv=True):
        if usjis_conv:
            func = keymap.InputKeyCommand(*keyInput(key_list))
        else:
            func = keymap.InputKeyCommand(*key_list)

        def _func():
            func()
            # Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
            # 開く機能がある。その挙動を抑制するための対策。
            if fakeymacs.ctrl_button_app:
                if keyhac_keymap.checkModifier(keymap.modifier, MODKEY_CTRL):
                    if "C-" not in key_list[-1]:
                        delay(0.01) # issue #19 の対策
                        pyauto.Input.send([pyauto.Key(strToVk("(255)"))])
        return _func

    self_insert_command_cache = {}

    def self_insert_command(*key_list, usjis_conv=True):
        try:
            func = self_insert_command_cache[(key_list, usjis_conv)]
        except:
            func = InputKeyCommand(*map(addSideOfModifierKey, map(specialCharToKeyStr, key_list)),
                                   usjis_conv=usjis_conv)
            self_insert_command_cache[(key_list, usjis_conv)] = func

        def _func():
            func()
            fakeymacs.ime_cancel = False
        return _func

    def self_insert_command2(*key_list, usjis_conv=True):
        func = self_insert_command(*key_list, usjis_conv=usjis_conv)
        def _func():
            correctImeStatus()
            func()
            if fc.use_emacs_ime_mode:
                if getImeStatus():
                    # 次の判定は、数引数を指定して日本語入力をした際に必要
                    if fakeymacs.ei_last_window is None:
                        enable_emacs_ime_mode()
        return _func

    def self_insert_command3(*key_list, usjis_conv=True):
        func = self_insert_command(*key_list, usjis_conv=usjis_conv)
        def _func():
            func()
            setImeStatus(0)
        return _func

    def digit(number):
        def _func():
            if fakeymacs.is_universal_argument:
                digit_argument(number)
            else:
                reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(str(number))))))()
        return _func

    def digit2(number):
        def _func():
            fakeymacs.is_universal_argument = True
            digit_argument(number)
        return _func

    def mark(func, forward_direction):
        # M-< や M-> 押下時に D-Shift が解除されないようにする対策
        func_d_shift = self_insert_command("D-LShift", "D-RShift")
        func_u_shift = self_insert_command("U-LShift", "U-RShift")
        def _func():
            if fakeymacs.is_marked:
                func_d_shift()
                # Windows 11 で遅延が顕著に発生するようになったので一旦コメント化（必要かもしれないが..）
                # delay()
                func()
                func_u_shift()

                # fakeymacs.forward_direction が未設定の場合、設定する
                if fakeymacs.forward_direction is None:
                    fakeymacs.forward_direction = forward_direction
            else:
                fakeymacs.forward_direction = None
                func()
        return _func

    def mark2(func, forward_direction):
        func_mark = mark(func, forward_direction)
        def _func():
            fakeymacs.is_marked = True
            func_mark()
            fakeymacs.is_marked = False
        return _func

    def reset_mark(func):
        def _func():
            func()
            fakeymacs.is_marked = False
            fakeymacs.forward_direction = None
        return _func

    def reset_counter(func):
        def _func():
            func()
            fakeymacs.is_universal_argument = False
            fakeymacs.is_digit_argument = False
            fakeymacs.repeat_counter = 1
        return _func

    def reset_undo(func):
        def _func():
            func()
            fakeymacs.is_undo_mode = True
        return _func

    def reset_search(func):
        def _func():
            func()
            fakeymacs.is_searching = False
        return _func

    def repeat(func):
        def _func():
            if fakeymacs.repeat_counter > fc.repeat_max:
                print("コマンドのリピート回数の最大値を超えています")
                repeat_counter = fc.repeat_max
            else:
                repeat_counter = fakeymacs.repeat_counter

            # キーボードマクロの繰り返し実行を可能とするために初期化する
            fakeymacs.repeat_counter = 1

            for _ in range(repeat_counter):
                func()
        return _func

    def repeat2(func):
        def _func():
            if fakeymacs.is_marked:
                fakeymacs.repeat_counter = 1
            repeat(func)()
        return _func

    def repeat3(func):
        def _func():
            if fakeymacs.repeat_counter > fc.repeat_max:
                print("コマンドのリピート回数の最大値を超えています")
                repeat_counter = fc.repeat_max
            else:
                repeat_counter = fakeymacs.repeat_counter

            func(repeat_counter)
        return _func

    def princ(str):
        imeStatus = getImeStatus()
        if imeStatus:
            setImeStatus(0)
        keymap.InputTextCommand(str)()
        if imeStatus:
            setImeStatus(1)

    def reloadConfig(mode):
        if mode == 1:
            keymap.fakeymacs_keyboard = "US"
        elif mode == 2:
            keymap.fakeymacs_keyboard = "JP"

        keymap.command_ReloadConfig()
        keymap.popBalloon("reloaded", "[Reloaded]", 1000)


    ##################################################
    ## キーバインド
    ##################################################

    # キーバインドの定義に利用している表記の意味は次のとおりです。
    # ・S-    : Shiftキー
    # ・C-    : Ctrlキー
    # ・A-    : Altキー
    # ・M-    : Altキー と Esc、C-[ のプレフィックスキーを利用する３パターンを定義（Emacs の Meta と同様）
    # ・W-    : Winキー
    # ・Ctl-x : ctl_x_prefix_key 変数で定義されているプレフィックスキーに置換え
    # ・(999) : 仮想キーコード指定

    # https://github.com/crftwr/keyhac/blob/master/keyhac_keymap.py
    # https://github.com/crftwr/pyauto/blob/master/pyauto_const.py
    # https://bsakatu.net/doc/virtual-key-of-windows/
    # http://www3.airnet.ne.jp/saka/hardware/keyboard/109scode.html

    ## 全てのキーパターンの設定（キーの入力記録を残すための設定）
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1 in ["", "W-"]:
            for mod2 in ["", "A-"]:
                for mod3 in ["", "C-"]:
                    for mod4 in ["", "S-"]:
                        mkey = mod1 + mod2 + mod3 + mod4 + key
                        define_key2(keymap_base, mkey, self_insert_command(mkey))

    ## マルチストロークキーの設定
    define_key(keymap_emacs, "Ctl-x",  keymap.defineMultiStrokeKeymap(fc.ctl_x_prefix_key))
    define_key(keymap_emacs, "C-q",    keymap.defineMultiStrokeKeymap("C-q"))
    define_key(keymap_emacs, "M-",     keymap.defineMultiStrokeKeymap("Esc"))
    define_key(keymap_emacs, "M-g",    keymap.defineMultiStrokeKeymap("M-g"))
    define_key(keymap_emacs, "M-g M-", keymap.defineMultiStrokeKeymap("M-g Esc"))

    ## 数字キーの設定
    for n in range(10):
        key = str(n)
        define_key(keymap_emacs, key, digit(n))
        if fc.use_ctrl_digit_key_for_digit_argument:
            define_key(keymap_emacs, "C-" + key, digit2(n))
        define_key(keymap_emacs, "M-" + key, digit2(n))
        define_key(keymap_emacs, "S-" + key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2("S-" + key))))))
        define_key(keymap_ime,          key, self_insert_command2(       key))
        define_key(keymap_ime,   "S-" + key, self_insert_command2("S-" + key))

    ## アルファベットキーの設定
    for vkey in range(VK_A, VK_Z + 1):
        key = vkToStr(vkey)
        define_key(keymap_emacs,        key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(       key))))))
        define_key(keymap_emacs, "S-" + key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2("S-" + key))))))
        define_key(keymap_ime,          key, self_insert_command2(       key))
        define_key(keymap_ime,   "S-" + key, self_insert_command2("S-" + key))

    ## 特殊文字キーの設定
    define_key(keymap_emacs, "Space"  , reset_undo(reset_counter(reset_mark(repeat(space)))))
    define_key(keymap_emacs, "S-Space", reset_undo(reset_counter(reset_mark(repeat(self_insert_command("S-Space"))))))

    for vkey in [VK_OEM_MINUS, VK_OEM_PLUS, VK_OEM_COMMA, VK_OEM_PERIOD, VK_OEM_1, VK_OEM_2, VK_OEM_3, VK_OEM_4, VK_OEM_5, VK_OEM_6, VK_OEM_7, VK_OEM_102]:
        key = vkToStr(vkey)
        define_key(keymap_emacs,        key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(       key))))))
        define_key(keymap_emacs, "S-" + key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2("S-" + key))))))
        define_key(keymap_ime,          key, self_insert_command2(       key))
        define_key(keymap_ime,   "S-" + key, self_insert_command2("S-" + key))

    ## 10key の特殊文字キーの設定
    for vkey in [VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE]:
        key = vkToStr(vkey)
        define_key(keymap_emacs, key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(key))))))
        define_key(keymap_ime,   key, self_insert_command2(key))

    ## quoted-insertキーの設定
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1 in ["", "W-"]:
            for mod2 in ["", "A-"]:
                for mod3 in ["", "C-"]:
                    for mod4 in ["", "S-"]:
                        mkey = mod1 + mod2 + mod3 + mod4 + key
                        define_key(keymap_emacs, "C-q " + mkey, self_insert_command(mkey))

    ## Escキーの設定
    define_key(keymap_emacs, "C-[ C-[", reset_undo(reset_counter(escape)))
    if fc.use_esc_as_meta:
        define_key(keymap_emacs, "Esc Esc", reset_undo(reset_counter(escape)))
    else:
        define_key(keymap_emacs, "Esc", reset_undo(reset_counter(escape)))

    ## universal-argumentキーの設定
    define_key(keymap_emacs, "C-u", universal_argument)

    ## 「IME の切り替え」のキー設定
    define_key(keymap_base, "A-(25)", toggle_input_method)

    if is_japanese_keyboard:
        define_key(keymap_base, "(243)", toggle_input_method) # <半角／全角> キー
        define_key(keymap_base, "(244)", toggle_input_method) # <半角／全角> キー

    define_key(keymap_base, "(240)",   toggle_input_method) # CapsLock キー
    define_key(keymap_base, "S-(240)", toggle_input_method) # CapsLock キー

    ## 「ファイル操作」のキー設定
    define_key(keymap_emacs, "Ctl-x C-f", reset_search(reset_undo(reset_counter(reset_mark(find_file)))))
    define_key(keymap_emacs, "Ctl-x C-s", reset_search(reset_undo(reset_counter(reset_mark(save_buffer)))))
    define_key(keymap_emacs, "Ctl-x C-w", reset_search(reset_undo(reset_counter(reset_mark(write_file)))))
    define_key(keymap_emacs, "Ctl-x d",   reset_search(reset_undo(reset_counter(reset_mark(dired)))))

    ## 「カーソル移動」のキー設定
    define_key(keymap_emacs, "C-b",     reset_search(reset_undo(reset_counter(mark(repeat(backward_char), False)))))
    define_key(keymap_emacs, "C-f",     reset_search(reset_undo(reset_counter(mark(repeat(forward_char), True)))))
    define_key(keymap_emacs, "M-b",     reset_search(reset_undo(reset_counter(mark(repeat(backward_word), False)))))
    define_key(keymap_emacs, "M-f",     reset_search(reset_undo(reset_counter(mark(repeat(forward_word), True)))))
    define_key(keymap_emacs, "C-p",     reset_search(reset_undo(reset_counter(mark(repeat(previous_line), False)))))
    define_key(keymap_emacs, "C-n",     reset_search(reset_undo(reset_counter(mark(repeat(next_line), True)))))
    define_key(keymap_emacs, "C-a",     reset_search(reset_undo(reset_counter(mark(move_beginning_of_line, False)))))
    define_key(keymap_emacs, "C-e",     reset_search(reset_undo(reset_counter(mark(move_end_of_line, True)))))
    define_key(keymap_emacs, "M-<",     reset_search(reset_undo(reset_counter(mark(beginning_of_buffer, False)))))
    define_key(keymap_emacs, "M->",     reset_search(reset_undo(reset_counter(mark(end_of_buffer, True)))))
    define_key(keymap_emacs, "M-g g",   reset_search(reset_undo(reset_counter(reset_mark(goto_line)))))
    define_key(keymap_emacs, "M-g M-g", reset_search(reset_undo(reset_counter(reset_mark(goto_line)))))
    define_key(keymap_emacs, "C-l",     reset_search(reset_undo(reset_counter(recenter))))

    define_key(keymap_emacs, "C-S-b", reset_search(reset_undo(reset_counter(mark2(repeat(backward_char), False)))))
    define_key(keymap_emacs, "C-S-f", reset_search(reset_undo(reset_counter(mark2(repeat(forward_char), True)))))
    define_key(keymap_emacs, "M-S-b", reset_search(reset_undo(reset_counter(mark2(repeat(backward_word), False)))))
    define_key(keymap_emacs, "M-S-f", reset_search(reset_undo(reset_counter(mark2(repeat(forward_word), True)))))
    define_key(keymap_emacs, "C-S-p", reset_search(reset_undo(reset_counter(mark2(repeat(previous_line), False)))))
    define_key(keymap_emacs, "C-S-n", reset_search(reset_undo(reset_counter(mark2(repeat(next_line), True)))))
    define_key(keymap_emacs, "C-S-a", reset_search(reset_undo(reset_counter(mark2(move_beginning_of_line, False)))))
    define_key(keymap_emacs, "C-S-e", reset_search(reset_undo(reset_counter(mark2(move_end_of_line, True)))))

    define_key(keymap_emacs, "Left",     reset_search(reset_undo(reset_counter(mark(repeat(backward_char), False)))))
    define_key(keymap_emacs, "Right",    reset_search(reset_undo(reset_counter(mark(repeat(forward_char), True)))))
    define_key(keymap_emacs, "C-Left",   reset_search(reset_undo(reset_counter(mark(repeat(backward_word), False)))))
    define_key(keymap_emacs, "C-Right",  reset_search(reset_undo(reset_counter(mark(repeat(forward_word), True)))))
    define_key(keymap_emacs, "Up",       reset_search(reset_undo(reset_counter(mark(repeat(previous_line), False)))))
    define_key(keymap_emacs, "Down",     reset_search(reset_undo(reset_counter(mark(repeat(next_line), True)))))
    define_key(keymap_emacs, "Home",     reset_search(reset_undo(reset_counter(mark(move_beginning_of_line, False)))))
    define_key(keymap_emacs, "End",      reset_search(reset_undo(reset_counter(mark(move_end_of_line, True)))))
    define_key(keymap_emacs, "C-Home",   reset_search(reset_undo(reset_counter(mark(beginning_of_buffer, False)))))
    define_key(keymap_emacs, "C-End",    reset_search(reset_undo(reset_counter(mark(end_of_buffer, True)))))
    define_key(keymap_emacs, "PageUP",   reset_search(reset_undo(reset_counter(mark(scroll_up, False)))))
    define_key(keymap_emacs, "PageDown", reset_search(reset_undo(reset_counter(mark(scroll_down, True)))))

    define_key(keymap_emacs, "S-Left",     reset_search(reset_undo(reset_counter(mark2(repeat(backward_char), False)))))
    define_key(keymap_emacs, "S-Right",    reset_search(reset_undo(reset_counter(mark2(repeat(forward_char), True)))))
    define_key(keymap_emacs, "C-S-Left",   reset_search(reset_undo(reset_counter(mark2(repeat(backward_word), False)))))
    define_key(keymap_emacs, "C-S-Right",  reset_search(reset_undo(reset_counter(mark2(repeat(forward_word), True)))))
    define_key(keymap_emacs, "S-Up",       reset_search(reset_undo(reset_counter(mark2(repeat(previous_line), False)))))
    define_key(keymap_emacs, "S-Down",     reset_search(reset_undo(reset_counter(mark2(repeat(next_line), True)))))
    define_key(keymap_emacs, "S-Home",     reset_search(reset_undo(reset_counter(mark2(move_beginning_of_line, False)))))
    define_key(keymap_emacs, "S-End",      reset_search(reset_undo(reset_counter(mark2(move_end_of_line, True)))))
    define_key(keymap_emacs, "C-S-Home",   reset_search(reset_undo(reset_counter(mark2(beginning_of_buffer, False)))))
    define_key(keymap_emacs, "C-S-End",    reset_search(reset_undo(reset_counter(mark2(end_of_buffer, True)))))
    define_key(keymap_emacs, "S-PageUP",   reset_search(reset_undo(reset_counter(mark2(scroll_up, False)))))
    define_key(keymap_emacs, "S-PageDown", reset_search(reset_undo(reset_counter(mark2(scroll_down, True)))))

    ## 「カット / コピー / 削除 / アンドゥ」のキー設定
    define_key(keymap_emacs, "C-h",      reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_backward_char))))))
    define_key(keymap_emacs, "C-d",      reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_char))))))
    define_key(keymap_emacs, "M-Delete", reset_search(reset_undo(reset_counter(reset_mark(repeat3(backward_kill_word))))))
    define_key(keymap_emacs, "M-d",      reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_word))))))
    define_key(keymap_emacs, "C-k",      reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_line))))))
    define_key(keymap_emacs, "C-w",      reset_search(reset_undo(reset_counter(reset_mark(kill_region)))))
    define_key(keymap_emacs, "M-w",      reset_search(reset_undo(reset_counter(reset_mark(kill_ring_save)))))
    define_key(keymap_emacs, "C-y",      reset_search(reset_undo(reset_counter(reset_mark(repeat(yank))))))
    define_key(keymap_emacs, "C-/",      reset_search(reset_counter(reset_mark(undo))))
    define_key(keymap_emacs, "Ctl-x u",  reset_search(reset_counter(reset_mark(undo))))

    define_key(keymap_emacs, "Back",      reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_backward_char))))))
    define_key(keymap_emacs, "Delete",    reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_char))))))
    define_key(keymap_emacs, "C-Back",    reset_search(reset_undo(reset_counter(reset_mark(repeat3(backward_kill_word))))))
    define_key(keymap_emacs, "C-Delete",  reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_word))))))
    define_key(keymap_emacs, "C-c",       reset_search(reset_undo(reset_counter(reset_mark(kill_ring_save)))))
    define_key(keymap_emacs, "C-v",       reset_search(reset_undo(reset_counter(reset_mark(repeat(yank)))))) # scroll_key の設定で上書きされない場合
    define_key(keymap_emacs, "C-z",       reset_search(reset_counter(reset_mark(undo))))
    define_key(keymap_emacs, "C-_",       reset_search(reset_undo(reset_counter(reset_mark(undo)))))
    define_key(keymap_emacs, "C-@",       reset_search(reset_undo(reset_counter(set_mark_command))))
    define_key(keymap_emacs, "C-Space",   reset_search(reset_undo(reset_counter(set_mark_command))))
    define_key(keymap_emacs, "Ctl-x h",   reset_search(reset_undo(reset_counter(mark_whole_buffer))))
    define_key(keymap_emacs, "Ctl-x C-p", reset_search(reset_undo(reset_counter(mark_page))))

    ## 「テキストの入れ替え」のキー設定
    define_key(keymap_emacs, "C-t", reset_search(reset_undo(reset_counter(reset_mark(transpose_chars)))))

    ## 「バッファ / ウィンドウ操作」のキー設定
    define_key(keymap_emacs, "M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
    define_key(keymap_emacs, "Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
    define_key(keymap_emacs, "Ctl-x b", reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
    define_key(keymap_emacs, "Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

    ## 「文字列検索 / 置換」のキー設定
    define_key(keymap_emacs, "C-r", reset_undo(reset_counter(reset_mark(isearch_backward))))
    define_key(keymap_emacs, "C-s", reset_undo(reset_counter(reset_mark(isearch_forward))))
    define_key(keymap_emacs, "M-%", reset_search(reset_undo(reset_counter(reset_mark(query_replace)))))

    ## 「キーボードマクロ」のキー設定
    define_key(keymap_emacs, "Ctl-x (", kmacro_start_macro)
    define_key(keymap_emacs, "Ctl-x )", kmacro_end_macro)
    define_key(keymap_emacs, "Ctl-x e", reset_search(reset_undo(reset_counter(repeat(kmacro_end_and_call_macro)))))

    ## 「その他」のキー設定
    define_key(keymap_emacs, "Enter",     reset_undo(reset_counter(reset_mark(repeat(newline)))))
    define_key(keymap_emacs, "C-m",       reset_undo(reset_counter(reset_mark(repeat(newline)))))
    define_key(keymap_emacs, "C-j",       reset_undo(reset_counter(reset_mark(newline_and_indent))))
    define_key(keymap_emacs, "C-o",       reset_undo(reset_counter(reset_mark(repeat(open_line)))))
    define_key(keymap_emacs, "Tab",       reset_undo(reset_counter(reset_mark(repeat(indent_for_tab_command)))))
    define_key(keymap_emacs, "C-g",       reset_search(reset_counter(reset_mark(keyboard_quit))))
    define_key(keymap_emacs, "Ctl-x C-c", reset_search(reset_undo(reset_counter(reset_mark(kill_emacs)))))
    define_key(keymap_emacs, "M-!",       reset_search(reset_undo(reset_counter(reset_mark(shell_command)))))

    ## 「タブ」のキー設定
    if fc.use_ctrl_i_as_tab:
        define_key(keymap_emacs, "C-i", reset_undo(reset_counter(reset_mark(repeat(indent_for_tab_command)))))

    ## 「スクロール」のキー設定
    if fc.scroll_key:
        define_key(keymap_emacs, fc.scroll_key[0], reset_search(reset_undo(reset_counter(mark(scroll_up, False)))))
        define_key(keymap_emacs, fc.scroll_key[1], reset_search(reset_undo(reset_counter(mark(scroll_down, True)))))

    ## 「カット」のキー設定
    if fc.ctl_x_prefix_key != "C-x":
        define_key(keymap_emacs, "C-x", reset_search(reset_undo(reset_counter(reset_mark(kill_region)))))

    ## 「IME の切り替え」のキー設定
    for key in fc.toggle_input_method_key:
        define_key(keymap_emacs, key, toggle_input_method)
        define_key(keymap_ime,   key, toggle_input_method)

    for disable_key, enable_key in fc.set_input_method_key:
        define_key(keymap_emacs, disable_key, disable_input_method)
        define_key(keymap_ime,   disable_key, disable_input_method)
        define_key(keymap_emacs, enable_key,  enable_input_method)
        define_key(keymap_ime,   enable_key,  enable_input_method)

    ## 「再変換」、「確定取り消し」のキー設定
    if fc.reconversion_key:
        if fc.ime == "Google_IME":
            # Google日本語入力を利用している時、ime_cancel_key に設定しているキーがキーバインドに
            # 定義されていると、「確定取り消し」が正常に動作しない場合がある。このため、そのキー
            # バインドの定義を削除する。
            del keymap_base[keyPos(kbd(fc.ime_cancel_key)[0])[0][0]]
            try:
                del keymap_emacs[keyPos(kbd(fc.ime_cancel_key)[0])[0][0]]
            except:
                pass

        for key in fc.reconversion_key:
            define_key(keymap_emacs, key, reset_undo(reset_counter(reset_mark(reconversion))))


    ###########################################################################
    ## Emacs日本語入力モードの設定
    ###########################################################################
    if fc.use_emacs_ime_mode:

        def is_emacs_ime_mode(window):
            if fakeymacs.ei_last_window is window:
                return True
            else:
                fakeymacs.ei_last_window = None
                return False

        def is_emacs_ime_mode2(window):
            if is_emacs_ime_mode(window):
                ei_popBalloon(1)
                return True
            else:
                ei_popBalloon(0)
                return False

        keymap_ei = keymap.defineWindowKeymap(check_func=is_emacs_ime_mode2)

        # Emacs日本語入力モードが開始されたときのウィンドウオブジェクトを格納する変数を初期化する
        fakeymacs.ei_last_window = None

        ##################################################
        ## Emacs日本語入力モード の切り替え
        ##################################################

        def enable_emacs_ime_mode(delay=0):
            fakeymacs.ei_last_window = keymap.getWindow()
            ei_updateKeymap(delay)

        def disable_emacs_ime_mode():
            fakeymacs.ei_last_window = None
            ei_updateKeymap(0)

        ##################################################
        ## IME の切り替え（Emacs日本語入力モード用）
        ##################################################

        def ei_enable_input_method():
            # IME の状態のバルーンヘルプを表示するために敢えてコールする
            enable_input_method()

        def ei_disable_input_method():
            disable_emacs_ime_mode()
            disable_input_method()

        def ei_enable_input_method2(window_keymap, key):
            func = getKeyCommand(window_keymap, key)
            if func is None:
                if key.startswith("O-"):
                    func = self_insert_command("(28)") # <変換> キーを発行
                else:
                    func = self_insert_command(key)

            def _func():
                if (fakeymacs.last_keys[0] is keymap_ei and
                    fakeymacs.last_keys[1] in ["Back", "C-h"]):
                    ei_enable_input_method()
                    fakeymacs.update_last_keys = False
                else:
                    func()
            return _func

        def ei_disable_input_method2(window_keymap, key):
            func = getKeyCommand(window_keymap, key)
            if func is None:
                if key.startswith("O-"):
                    func = self_insert_command("(29)") # <無変換> キーを発行
                else:
                    func = self_insert_command(key)

            def _func():
                if (fakeymacs.last_keys[0] is keymap_ei and
                    fakeymacs.last_keys[1] in ["Back", "C-h"]):
                    ei_disable_input_method()
                    fakeymacs.update_last_keys = False
                else:
                    func()
            return _func

        ##################################################
        ## その他（Emacs日本語入力モード用）
        ##################################################

        def ei_esc():
            escape()

        def ei_newline():
            self_insert_command("Enter")()
            fakeymacs.ime_cancel = True
            disable_emacs_ime_mode()

        def ei_keyboard_quit():
            escape()
            disable_emacs_ime_mode()

        ##################################################
        ## 共通関数（Emacs日本語入力モード用）
        ##################################################

        def ei_popBalloon(ime_mode_status):
            if not fakeymacs.is_playing_kmacro:
                if fc.emacs_ime_mode_balloon_message:
                    # Qt5*QWindowIcon にマッチするクラスをもつアプリは入力文字にバルーンヘルプが
                    # 被るので、バルーンヘルプの表示対象から外す
                    if not checkWindow(None, "Qt5*QWindowIcon"):
                        if ime_mode_status:
                            try:
                                keymap.popBalloon("emacs_ime_mode", fc.emacs_ime_mode_balloon_message)
                            except:
                                pass
                        else:
                            keymap.closeBalloon("emacs_ime_mode")

        def ei_updateKeymap(delay):
            if fakeymacs.is_playing_kmacro:
                keymap.updateKeymap()
            else:
                keymap.delayedCall(keymap.updateKeymap, delay)

        ##################################################
        ## キーバインド（Emacs日本語入力モード用）
        ##################################################

        ## 「IME の切り替え」のキー設定
        define_key(keymap_ei, "(243)",   ei_disable_input_method)
        define_key(keymap_ei, "(244)",   ei_disable_input_method)
        define_key(keymap_ei, "A-(25)",  ei_disable_input_method)
        define_key(keymap_ei, "(240)",   ei_disable_input_method)
        define_key(keymap_ei, "S-(240)", ei_disable_input_method)

        ## Escキーの設定
        define_key(keymap_ei, "Esc", ei_esc)
        define_key(keymap_ei, "C-[", ei_esc)

        ## 「カーソル移動」のキー設定
        define_key(keymap_ei, "C-b", backward_char)
        define_key(keymap_ei, "C-f", forward_char)
        define_key(keymap_ei, "C-p", previous_line)
        define_key(keymap_ei, "C-n", next_line)
        define_key(keymap_ei, "C-a", move_beginning_of_line)
        define_key(keymap_ei, "C-e", move_end_of_line)

        ## 「カット / コピー / 削除 / アンドゥ」のキー設定
        define_key(keymap_ei, "C-h",  delete_backward_char)
        define_key(keymap_ei, "Back", delete_backward_char) # キーの記録を残すために敢えて設定
        define_key(keymap_ei, "C-d",  delete_char)

        ## 「その他」のキー設定
        define_key(keymap_ei, "Enter", ei_newline)
        define_key(keymap_ei, "C-m",   ei_newline)
        define_key(keymap_ei, "C-g",   ei_keyboard_quit)

        ## 「スクロール」のキー設定
        if fc.scroll_key:
            if fc.scroll_key[0]:
                define_key(keymap_ei, fc.scroll_key[0].replace("M-", "A-"), scroll_up)
            if fc.scroll_key[1]:
                define_key(keymap_ei, fc.scroll_key[1].replace("M-", "A-"), scroll_down)

        # 「IME のショートカットの置き換え」のキー設定
        for replace_key, original_key in fc.emacs_ime_mode_key:
            define_key(keymap_ei, replace_key, self_insert_command(original_key))

        # この時点の keymap_ei を複製する
        keymap_ei_dup = copy.deepcopy(keymap_ei)

        ## 「IME の切り替え」のキー設定
        for key in fc.toggle_input_method_key:
            define_key(keymap_ei, key, ei_disable_input_method2(keymap_ei_dup, key))

        ## 「IME の切り替え」のキー設定
        for disable_key, enable_key in fc.set_input_method_key:
            if disable_key:
                define_key(keymap_ei, disable_key, ei_disable_input_method2(keymap_ei_dup, disable_key))
            if enable_key:
                define_key(keymap_ei, enable_key,  ei_enable_input_method2(keymap_ei_dup, enable_key))


    ###########################################################################
    ## 「Emacs キーバインドの切り替え」のキー設定
    ###########################################################################

    def is_global_target(window):
        if window.getProcessName() in fc.transparent_target:
            return False
        else:
            return True

    keymap_global = keymap.defineWindowKeymap(check_func=is_global_target)

    define_key(keymap_global, fc.toggle_emacs_keybind_key, toggle_emacs_keybind)


    ###########################################################################
    ## アプリケーションキーの設定
    ###########################################################################

    define_key(keymap_global, fc.application_key, self_insert_command("Apps"))


    ###########################################################################
    ## ファンクションキーの設定
    ###########################################################################

    ## Alt+数字キー列の設定
    if fc.use_alt_digit_key_for_f1_to_f12:
        for i in range(10):
            define_key(keymap_global, "A-{}".format((i + 1) % 10), self_insert_command(vkToStr(VK_F1 + i)))

        define_key(keymap_global, "A--", self_insert_command(vkToStr(VK_F11)))

        if is_japanese_keyboard:
            define_key(keymap_global, "A-^", self_insert_command(vkToStr(VK_F12)))
        else:
            define_key(keymap_global, "A-=", self_insert_command(vkToStr(VK_F12)))

    ## Alt+Shift+数字キー列の設定
    if fc.use_alt_shift_digit_key_for_f13_to_f24:
        for i in range(10):
            define_key(keymap_global, "A-S-{}".format((i + 1) % 10), self_insert_command(vkToStr(VK_F13 + i)))

        define_key(keymap_global, "A-S--", self_insert_command(vkToStr(VK_F23)))

        if is_japanese_keyboard:
            define_key(keymap_global, "A-S-^", self_insert_command(vkToStr(VK_F24)))
        else:
            define_key(keymap_global, "A-S-=", self_insert_command(vkToStr(VK_F24)))


    ###########################################################################
    ## デスクトップの設定
    ###########################################################################

    ##################################################
    ## ウィンドウ操作（デスクトップ用）
    ##################################################

    def popWindow(window):
        def _func():
            try:
                if window.isMinimized():
                    window.restore()

                window.getLastActivePopup().setForeground()
            except:
                print("選択したウィンドウは存在しませんでした")

            fakeymacs.window_list = []
        return _func

    def getWindowList(minimized_window=None):
        def makeWindowList(window, arg):
            nonlocal window_title

            if window.isVisible() and not window.getOwner():
                class_name = window.getClassName()
                title = re.sub(r".* ‎- ", r"", window.getText())

                if class_name == "Emacs" or title != "":
                    if not re.match(fc.window_operation_exclusion_class, class_name):
                        process_name = window.getProcessName()

                        if not re.match(fc.window_operation_exclusion_process, process_name):

                            # バックグラウンドで起動している UWPアプリが window_list に登録されるのを抑制する
                            # （http://mrxray.on.coocan.jp/Delphi/plSamples/320_AppList.htm）
                            # （http://mrxray.on.coocan.jp/Delphi/plSamples/324_CheckRun_UWPApp.htm）

                            if class_name == "Windows.UI.Core.CoreWindow":
                                window_title = title

                            elif class_name == "ApplicationFrameWindow":
                                if title != "Cortana":
                                    if (title != window_title or window.isMinimized() or
                                        window in fakeymacs.window_list): # UWPアプリの仮想デスクトップ対策
                                        window_list.append(window)
                                window_title = None
                            else:
                                window_list.append(window)
            return True

        window_title = None
        window_list = []
        Window.enum(makeWindowList, None)

        if minimized_window is None:
            window_list2 = window_list
        else:
            window_list2 = []
            for window in window_list:
                if ((minimized_window and window.isMinimized()) or
                    (not minimized_window and not window.isMinimized())):
                    window_list2.append(window)

        return window_list2

    def saveWindowList():
        window_list = getWindowList(False)

        # ２つのリストに差異があるか？
        if set(window_list) ^ set(fakeymacs.window_list):
            fakeymacs.window_list = window_list

    def previous_window():
        saveWindowList()

        if fakeymacs.window_list:
            window_list = fakeymacs.window_list[-1:] + fakeymacs.window_list[:-1]
            popWindow(window_list[0])()
            fakeymacs.window_list = window_list

    def next_window():
        saveWindowList()

        if fakeymacs.window_list:
            window_list = fakeymacs.window_list[1:] + fakeymacs.window_list[:1]
            popWindow(window_list[0])()
            fakeymacs.window_list = window_list

    def move_window_to_previous_display():
        self_insert_command("W-S-Left")()

    def move_window_to_next_display():
        self_insert_command("W-S-Right")()

    def minimize_window():
        window = keymap.getTopLevelWindow()
        if window and not window.isMinimized():
            window.minimize()
            delay()
            window_list = getWindowList()
            if window in window_list:
                if window is window_list[-1]:
                    fakeymacs.reverse_window_to_restore = False
                else:
                    fakeymacs.reverse_window_to_restore = True

    def restore_window():
        window_list = getWindowList(True)
        if window_list:
            if not fakeymacs.reverse_window_to_restore:
                window_list.reverse()
            window_list[0].restore()

    def previous_desktop():
        self_insert_command("W-C-Left")()

    def next_desktop():
        self_insert_command("W-C-Right")()

    def move_window_to_previous_desktop():
        self_insert_command("LW-LC-LA-Left")()

    def move_window_to_next_desktop():
        self_insert_command("LW-LC-LA-Right")()

    ##################################################
    ## キーバインド（デスクトップ用）
    ##################################################

    # 表示しているウィンドウの中で、一番最近までフォーカスがあったウィンドウに移動
    define_key(keymap_global, fc.other_window_key, other_window)

    # アクティブウィンドウの切り替え
    for previous_key, next_key in fc.window_switching_key:
        define_key(keymap_global, previous_key, previous_window)
        define_key(keymap_global, next_key,     next_window)

    # アクティブウィンドウのディスプレイ間移動
    for previous_key, next_key in fc.window_movement_key_for_displays:
        define_key(keymap_global, previous_key, move_window_to_previous_display)
        define_key(keymap_global, next_key,     move_window_to_next_display)

    # ウィンドウの最小化、リストア
    for restore_key, minimize_key in fc.window_minimize_key:
        define_key(keymap_global, restore_key,  restore_window)
        define_key(keymap_global, minimize_key, minimize_window)

    # 仮想デスクトップの切り替え
    for previous_key, next_key in fc.desktop_switching_key:
        define_key(keymap_global, previous_key, previous_desktop)
        define_key(keymap_global, next_key,     next_desktop)

    # アクティブウィンドウ仮想デスクトップの切り替え
    for previous_key, next_key in fc.window_movement_key_for_desktops:
        define_key(keymap_global, previous_key, move_window_to_previous_desktop)
        define_key(keymap_global, next_key,     move_window_to_next_desktop)

    # IME の「単語登録」プログラムの起動
    define_key(keymap_global, fc.word_register_key,
               keymap.ShellExecuteCommand(None, fc.word_register_name, fc.word_register_param, ""))


    ###########################################################################
    ## タスク切り替え画面／タスクビューの設定
    ###########################################################################

    def is_task_switching_window(window):
        if (window.getProcessName() == "explorer.exe" and
            window.getClassName() in ["MultitaskingViewFrame",
                                      "TaskSwitcherWnd",
                                      "Windows.UI.Core.CoreWindow",
                                      "Windows.UI.Input.InputSite.WindowClass"]):
            return True
        else:
            return False

    keymap_tsw = keymap.defineWindowKeymap(check_func=is_task_switching_window)

    ##################################################
    ## キーバインド（タスク切り替え画面／タスクビュー用）
    ##################################################

    define_key(keymap_tsw, "A-b", self_insert_command("A-Left"))
    define_key(keymap_tsw, "A-f", self_insert_command("A-Right"))
    define_key(keymap_tsw, "A-p", self_insert_command("A-Up"))
    define_key(keymap_tsw, "A-n", self_insert_command("A-Down"))
    define_key(keymap_tsw, "A-d", self_insert_command("A-Delete"))
    define_key(keymap_tsw, "A-g", self_insert_command("A-Esc"))

    define_key(keymap_tsw, "C-b", backward_char)
    define_key(keymap_tsw, "C-f", forward_char)
    define_key(keymap_tsw, "C-p", previous_line)
    define_key(keymap_tsw, "C-n", next_line)
    define_key(keymap_tsw, "C-d", delete_char)
    define_key(keymap_tsw, "C-g", escape)


    ###########################################################################
    ## リストウィンドウの設定
    ###########################################################################

    # リストウィンドウはクリップボードリストで利用していますが、クリップボードリストの機能を
    # Emacsキーバインドを適用していないアプリケーションソフトでも利用できるようにするため、
    # クリップボードリストで Enter を押下した際の挙動を、次のとおりに切り分けています。
    #
    # １）Emacsキーバインドを適用しているアプリケーションソフトからクリップボードリストを起動
    #     →   Enter（テキストの貼り付け）
    # ２）Emacsキーバインドを適用していないアプリケーションソフトからクリップボードリストを起動
    #     → S-Enter（テキストをクリップボードに格納）
    #
    # ※ Emacsキーバインドを適用しないアプリケーションソフトには、文字の入出力の方式が特殊な
    #    ものもあるため、テキストの貼り付けはそのアプリケーションソフトのペースト操作で行う
    #    ことを前提としています。
    # ※ C-Enter（引用記号付で貼り付け）の置き換えは、対応が複雑となるため行っておりません。

    def is_list_window(window):
        if window.getClassName() == "KeyhacWindowClass" and window.getText() != "Keyhac":
            fakeymacs.lw_is_searching = False
            return True
        else:
            return False

    keymap_lw = keymap.defineWindowKeymap(check_func=is_list_window)

    # リストウィンドウで検索が開始されると True になる
    fakeymacs.lw_is_searching = False

    ##################################################
    ## 文字列検索 / 置換（リストウィンドウ用）
    ##################################################

    def lw_isearch(direction):
        if fakeymacs.lw_is_searching:
            self_insert_command({"backward":"Up", "forward":"Down"}[direction])()
        else:
            self_insert_command("f")()
            fakeymacs.lw_is_searching = True

    def lw_isearch_backward():
        lw_isearch("backward")

    def lw_isearch_forward():
        lw_isearch("forward")

    ##################################################
    ## その他（リストウィンドウ用）
    ##################################################

    def lw_keyboard_quit():
        escape()

    ##################################################
    ## 共通関数（リストウィンドウ用）
    ##################################################

    def lw_newline():
        if fakeymacs.keybind == "emacs":
            self_insert_command("Enter")()
        else:
            self_insert_command("S-Enter")()

    def lw_exit_search(func):
        def _func():
            if fakeymacs.lw_is_searching:
                self_insert_command("Enter")()
            func()
        return _func

    def lw_reset_search(func):
        def _func():
            func()
            fakeymacs.lw_is_searching = False
        return _func

    ##################################################
    ## キーバインド（リストウィンドウ用）
    ##################################################

    ## Escキーの設定
    define_key(keymap_lw, "Esc", lw_reset_search(escape))
    define_key(keymap_lw, "C-[", lw_reset_search(escape))

    ## 「カーソル移動」のキー設定
    define_key(keymap_lw, "C-b", backward_char)
    define_key(keymap_lw, "A-b", backward_char)

    define_key(keymap_lw, "C-f", forward_char)
    define_key(keymap_lw, "A-f", forward_char)

    define_key(keymap_lw, "C-p", previous_line)
    define_key(keymap_lw, "A-p", previous_line)

    define_key(keymap_lw, "C-n", next_line)
    define_key(keymap_lw, "A-n", next_line)

    if fc.scroll_key:
        if fc.scroll_key[0]:
            define_key(keymap_lw, fc.scroll_key[0].replace("M-", "A-"), scroll_up)
        if fc.scroll_key[1]:
            define_key(keymap_lw, fc.scroll_key[1].replace("M-", "A-"), scroll_down)

    ## 「カット / コピー / 削除 / アンドゥ」のキー設定
    define_key(keymap_lw, "C-h", delete_backward_char)
    define_key(keymap_lw, "A-h", delete_backward_char)

    define_key(keymap_lw, "C-d", delete_char)
    define_key(keymap_lw, "A-d", delete_char)

    ## 「文字列検索 / 置換」のキー設定
    define_key(keymap_lw, "C-r", lw_isearch_backward)
    define_key(keymap_lw, "A-r", lw_isearch_backward)

    define_key(keymap_lw, "C-s", lw_isearch_forward)
    define_key(keymap_lw, "A-s", lw_isearch_forward)

    ## 「その他」のキー設定
    define_key(keymap_lw, "Enter", lw_exit_search(lw_newline))
    define_key(keymap_lw, "C-m",   lw_exit_search(lw_newline))
    define_key(keymap_lw, "A-m",   lw_exit_search(lw_newline))

    define_key(keymap_lw, "C-g", lw_reset_search(lw_keyboard_quit))
    define_key(keymap_lw, "A-g", lw_reset_search(lw_keyboard_quit))

    define_key(keymap_lw, "S-Enter", lw_exit_search(self_insert_command("S-Enter")))
    define_key(keymap_lw, "C-Enter", lw_exit_search(self_insert_command("C-Enter")))
    define_key(keymap_lw, "A-Enter", lw_exit_search(self_insert_command("C-Enter")))

    # 個人設定ファイルのセクション [section-base-2] を読み込んで実行する
    exec(readConfigPersonal("[section-base-2]"), dict(globals(), **locals()))


    ####################################################################################################
    ## クリップボードリストの設定
    ####################################################################################################

    # クリップボードリストを利用するための設定です。クリップボードリストは clipboardList_key 変数で
    # 設定したキーの押下により起動します。クリップボードリストを開いた後、C-f（→）や C-b（←）
    # キーを入力することで画面を切り替えることができます。
    # （参考：https://github.com/crftwr/keyhac/blob/master/_config.py）

    # リストウィンドウのフォーマッタを定義する
    list_formatter = "{:30}"

    # 定型文
    fc.fixed_items = [
        ["---------+ x 8", "---------+" * 8],
        ["メールアドレス", "user_name@domain_name"],
        ["住所",           "〒999-9999 ＮＮＮＮＮＮＮＮＮＮ"],
        ["電話番号",       "99-999-9999"],
    ]
    fc.fixed_items[0][0] = list_formatter.format(fc.fixed_items[0][0])

    # 日時をペーストする機能
    def dateAndTime(fmt):
        def _func():
            return datetime.datetime.now().strftime(fmt)
        return _func

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

    # 個人設定ファイルのセクション [section-clipboardList-1] を読み込んで実行する
    exec(readConfigPersonal("[section-clipboardList-1]"), dict(globals(), **locals()))

    keymap.cblisters = [keymap.cblisters[0]] + fc.clipboardList_listers

    def lw_clipboardList():
        keymap.command_ClipboardList()

    # クリップボードリストを起動する
    define_key(keymap_global, fc.clipboardList_key, lw_clipboardList)

    # 個人設定ファイルのセクション [section-clipboardList-2] を読み込んで実行する
    exec(readConfigPersonal("[section-clipboardList-2]"), dict(globals(), **locals()))


    ####################################################################################################
    ## ランチャーリストの設定
    ####################################################################################################

    # ランチャー用のリストを利用するための設定です。ランチャーリストは lancherList_key 変数で
    # 設定したキーの押下により起動します。ランチャーリストを開いた後、C-f（→）や C-b（←）
    # キーを入力することで画面を切り替えることができます。
    # （参考：https://github.com/crftwr/keyhac/blob/master/_config.py）

    # リストウィンドウのフォーマッタを定義する
    list_formatter = "{:30}"

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

    # その他
    fc.other_items = [
        ["Edit   config.py", keymap.command_EditConfig],
        ["Reload config.py", lambda: reloadConfig(0)],
    ]
    if os_keyboard_type == "JP":
        fc.other_items += [
            ["Reload config.py (to  US layout)", lambda: reloadConfig(1)],
            ["Reload config.py (to JIS layout)", lambda: reloadConfig(2)],
        ]
    fc.other_items[0][0] = list_formatter.format(fc.other_items[0][0])

    fc.lancherList_listers = [
        ["App",     cblister_FixedPhrase(fc.application_items)],
        ["Website", cblister_FixedPhrase(fc.website_items)],
        ["Other",   cblister_FixedPhrase(fc.other_items)],
    ]

    # 個人設定ファイルのセクション [section-lancherList-1] を読み込んで実行する
    exec(readConfigPersonal("[section-lancherList-1]"), dict(globals(), **locals()))

    def lw_lancherList():
        def popLancherList():

            # 既にリストが開いていたら閉じるだけ
            if keymap.isListWindowOpened():
                keymap.cancelListWindow()
                return

            # ウィンドウ
            window_list = getWindowList()
            window_items = []
            if window_list:
                process_name_length = max(map(len, map(Window.getProcessName, window_list)))

                formatter = "{0:" + str(process_name_length) + "} |{1:1}| {2}"
                for window in window_list:
                    if window.isMinimized():
                        icon = "m"
                    else:
                        icon = ""

                    window_items.append([formatter.format(window.getProcessName(),
                                                          icon, window.getText()), popWindow(window)])

            window_items.append([list_formatter.format("<Desktop>"),
                                 keymap.ShellExecuteCommand(None, r"shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}", "", "")])

            listers = [["Window", cblister_FixedPhrase(window_items)]] + fc.lancherList_listers

            try:
                select_item = keymap.popListWindow(listers)

                if not select_item:
                    Window.find("Progman", None).setForeground()
                    select_item = keymap.popListWindow(listers)

                if select_item and select_item[0] and select_item[0][1]:
                    select_item[0][1]()
            except:
                print("エラーが発生しました")

        # キーフックの中で時間のかかる処理を実行できないので、delayedCall() を使って遅延実行する
        keymap.delayedCall(popLancherList, 0)

    # ランチャーリストを起動する
    define_key(keymap_global, fc.lancherList_key, lw_lancherList)

    # 個人設定ファイルのセクション [section-lancherList-2] を読み込んで実行する
    exec(readConfigPersonal("[section-lancherList-2]"), dict(globals(), **locals()))


    ####################################################################################################
    ## 拡張機能の設定
    ####################################################################################################

    # 個人設定ファイルのセクション [section-extensions] を読み込んで実行する
    exec(readConfigPersonal("[section-extensions]"), dict(globals(), **locals()))


    ####################################################################################################
    ## 後処理（キーマップの優先順位を調整する）
    ####################################################################################################

    keymap.window_keymap_list.remove(keymap_global)
    keymap.window_keymap_list.remove(keymap_tsw)
    keymap.window_keymap_list.remove(keymap_lw)

    keymap.window_keymap_list.append(keymap_global)
    keymap.window_keymap_list.append(keymap_tsw)
    keymap.window_keymap_list.append(keymap_lw)
