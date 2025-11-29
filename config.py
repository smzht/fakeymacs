# -*- mode: python; coding: utf-8-with-signature-dos -*-

#########################################################################
##                              Fakeymacs
#########################################################################
##  Windows の操作を Emacs のキーバインドで行うための設定（Keyhac版）
#########################################################################

fakeymacs_version = "20251129_01"

import time
import os
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
    # （https://www.tokovalue.jp/function/GetKeyboardLayout.htm）
    # （https://www.tokovalue.jp/function/GetKeyboardType.htm）
    if ctypes.windll.user32.GetKeyboardType(0) == 7:
        str_vk_table = copy.copy(keyhac_keymap.KeyCondition.str_vk_table_common)
        for name in keyhac_keymap.KeyCondition.str_vk_table_jpn:
            del str_vk_table[name]
        str_vk_table.update(keyhac_keymap.KeyCondition.str_vk_table_std)

        vk_str_table = copy.copy(keyhac_keymap.KeyCondition.vk_str_table_common)
        for vk in keyhac_keymap.KeyCondition.vk_str_table_jpn:
            del vk_str_table[vk]
        vk_str_table.update(keyhac_keymap.KeyCondition.vk_str_table_std)

        # 「英語用キーボードドライバ置換」を利用する場合、キーテーブルを US 用のものに置き換える
        # （https://github.com/kskmori/US-AltIME.ahk?tab=readme-ov-file#us101mode）
        if (ctypes.windll.user32.GetKeyboardLayout(0) >> 16) == 0x409:
            keyhac_keymap.KeyCondition.str_vk_table = str_vk_table
            keyhac_keymap.KeyCondition.vk_str_table = vk_str_table
            os_keyboard_type = "US"
        else:
            os_keyboard_type = "JP"
    else:
        os_keyboard_type = "US"

    # 個人設定ファイルを読み込む
    try:
        with open(rf"{dataPath()}\config_personal.py", "r", encoding="utf-8-sig") as f:
            config_personal = f.read()
    except:
        print("個人設定ファイル config_personal.py は存在しないため、読み込みしていません")
        config_personal = ""

    def readConfigPersonal(section):
        if config_personal:
            # https://www.zu-min.com/archives/614
            m = re.search(rf"(#\s{re.escape(section)}.*?)(#\s\[section-|\Z)", config_personal,
                          flags=re.DOTALL)
            try:
                config_section = m.group(1)
                config_section = re.sub(r"^##.*", r"", config_section, flags=re.MULTILINE)
            except:
                print(f"個人設定ファイルのセクション {section} の読み込みに失敗しました")
                config_section = ""
        else:
            config_section = ""

        return config_section

    def readConfigExtension(config_file, msg=True):
        try:
            with open(rf"{dataPath()}\fakeymacs_extensions\{config_file}", "r", encoding="utf-8-sig") as f:
                config_extension = f.read()
        except:
            if msg:
                print(f"拡張機能ファイル {config_file} の読み込みに失敗しました")
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
    #   さらに Google 日本語入力を利用している場合、keymap.getWindow().getImeStatus() が True を返すため、
    #   Emacs 日本語入力モードの挙動がおかしくなります。この対策を行うかどうかを指定します。）
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

    # すべてのキーマップを透過するアプリケーションソフトのプロセス名称（ワイルドカード指定可）を指定する
    # （全ての設定に優先します）
    # （keymap_base、keymap_global を含むすべてのキーマップをスルーします）
    fc.transparent_target       = []

    # すべてのキーマップを透過するウィンドウのクラス名称（ワイルドカード指定可）を指定する
    # （全ての設定に優先します）
    # （keymap_base、keymap_global を含むすべてのキーマップをスルーします）
    fc.transparent_target_class = ["IHWindowClass"]      # Remote Desktop

    # Emacs のキーバインドにするウィンドウのクラス名称（ワイルドカード指定可）を指定する
    # （fc.emacs_target、fc.not_emacs_target の設定より優先します）
    fc.emacs_target_class   = ["Edit",                   # テキスト入力フィールドなどが該当
                               "Button",                 # ボタン
                               "ComboBox",               # コンボボックス
                               "ListBox",                # リストボックス
                               ]

    # Emacs のキーバインドに“する”アプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    # （fc.not_emacs_target の設定より優先します）
    # （Keyhac のメニューから「内部ログ」を ON にすると、processname や classname を確認することが
    #   できます）
    fc.emacs_target = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                        ["*PowerShell*", "*コマンド プロンプト*", "*Command Prompt*",
                         "* - edit*", "* - micro*", "設定", "Settings"]],
                       ["powershell.exe", "ConsoleWindowClass", "*PowerShell*"],
                       ["cmd.exe", "ConsoleWindowClass", ["*コマンド プロンプト*", "*Command Prompt*"]],
                       [None, "ConsoleWindowClass", ["* - edit*", "* - micro*"]],
                       ]

    # Emacs のキーバインドに“しない”アプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    # （Keyhac のメニューから「内部ログ」を ON にすると、processname や classname を確認することが
    #   できます）
    fc.not_emacs_target     = ["wsl.exe",                # WSL
                               "bash.exe",               # WSL
                               "ubuntu*.exe",            # WSL
                               "debian.exe",             # WSL
                               "kali.exe",               # WSL
                               "SLES-*.exe",             # WSL
                               "openSUSE-*.exe",         # WSL
                               "WindowsTerminal.exe",    # Windows Terminal
                               "powershell.exe",         # Windows PowerShell
                               "cmd.exe",                # コマンドプロンプト
                               "mintty.exe",             # mintty
                               "Cmder.exe",              # Cmder
                               "ConEmu*.exe",            # ConEmu
                               "emacs*.exe",             # Emacs
                               "gvim.exe",               # GVim
                               "xyzzy.exe",              # xyzzy
                               "msrdc.exe",              # WSLg
                               "XWin*.exe",              # XWin
                               "Xming.exe",              # Xming
                               "vcxsrv.exe",             # VcXsrv
                               "GWSL_vcxsrv*.exe",       # GWSL
                               "X410.exe",               # X410
                               "Xpra-Launcher.exe",      # Xpra
                               "putty.exe",              # PuTTY
                               "ttermpro.exe",           # TeraTerm
                               "MobaXterm.exe",          # MobaXterm
                               "TurboVNC.exe",           # TurboVNC
                               "vncviewer*.exe",         # UltraVNC
                               "mc.exe",                 # Midnight Commander
                               [None, None, "さくらのクラウドシェル*"],
                               ]

    # IME の切り替え“のみをしたい”アプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    # （指定できるアプリケーションソフトは、not_emacs_target で（除外）指定したものからのみとなります）
    fc.ime_target           = ["wsl.exe",                # WSL
                               "bash.exe",               # WSL
                               "ubuntu*.exe",            # WSL
                               "debian.exe",             # WSL
                               "kali.exe",               # WSL
                               "SLES-*.exe",             # WSL
                               "openSUSE-*.exe",         # WSL
                               "WindowsTerminal.exe",    # Windows Terminal
                               "powershell.exe",         # Windows PowerShell
                               "cmd.exe",                # コマンドプロンプト
                               "mintty.exe",             # mintty
                               "Cmder.exe",              # Cmder
                               "ConEmu*.exe",            # ConEmu
                               "gvim.exe",               # GVim
                               "xyzzy.exe",              # xyzzy
                               "putty.exe",              # PuTTY
                               "ttermpro.exe",           # TeraTerm
                               "MobaXterm.exe",          # MobaXterm
                               "mc.exe",                 # Midnight Commander
                               [None, None, "さくらのクラウドシェル*"],
                               ]

    # キーマップ毎にキー設定をスキップするキーを指定する
    # （リストに指定するキーは、define_key の第二引数に指定する記法のキーとしてください。"A-v" や "C-v"
    #   のような指定の他に、"M-f" や "Ctl-x d" などの指定も可能です。"M-g*" のようにワイルドカードも
    #   利用することができます。ワイルドカード文字をエスケープしたい場合は、[] で括ってください。）
    # （ここで指定したキーに新たに別のキー設定をしたいときには、define_key2 関数を利用してください）
    fc.skip_settings_key    = {"keymap_base"      : ["W-g", "A-Tab", "Space"], # ベース Keymap
                               "keymap_global"    : [], # グローバル Keymap
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

    # clipboard 監視の対象外とするアプリケーションソフトのプロセス名称（ワイルドカード指定可）を指定する
    fc.not_clipboard_target = []
    fc.not_clipboard_target += ["EXCEL.EXE"] # Microsoft Excel

    # clipboard 監視の対象外とするウィンドウのクラス名称（ワイルドカード指定可）を指定する
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

    # ウィンドウが切り替わった際、IME の状態をリセット（英数入力）するかを指定する（True: する、False: しない）
    fc.use_ime_status_reset = False

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

    # キーマップを再設定するキーを指定する
    fc.update_keymap_key = "A-S-Enter"

    # Emacs キーバインドを切り替えるキーを指定する
    # （Emacs キーバインドを利用するアプリケーションソフトでかつフォーカスが当たっているソフトに対して
    #   切り替えが機能します。また、Emacs キーバインドを OFF にしても、IME の切り替えは ime_target に
    #   登録したアプリケーションソフトと同様に機能するようにしています。）
    # （fc.emacs_target_class 変数に指定したクラスに該当するアプリケーションソフト（Windows10版 Notepad など）
    #   は、Emacs キーバインドを切り替えの対象となりません（常に Emacs キーバインドとなります）。）
    # fc.toggle_emacs_keybind_key = "C-S-Space"
    fc.toggle_emacs_keybind_key = "A-S-Space"

    # アプリケーションキーとして利用するキーを指定する
    # （修飾キーに Alt は使えないようです）
    fc.application_key = None
    # fc.application_key = "O-RCtrl"

    # 数引数の指定に Ctrl+数字キーを使うかを指定する（True: 使う、False: 使わない）
    # （False に指定しても、C-u 数字キーで数引数を指定することができます）
    fc.use_ctrl_digit_key_for_digit_argument = False

    # 数字キー列が Alt キーと一緒に押されたとき、F1 から F12 のファンクションキーとして使うかを指定する
    # （True: 使う、False: 使わない）
    fc.use_alt_digit_key_for_f1_to_f12 = False

    # 表示しているウィンドウの中で、一番最近までフォーカスがあったウィンドウに移動するキーを指定する
    fc.other_window_key = "A-o"

    # ウィンドウ操作（other_window など）の対象としたくないアプリケーションソフトのクラス名称を指定する
    # （正規表現で指定してください（複数指定する場合は「|」で連結してください））
    fc.window_operation_exclusion_class = r"Progman"

    # ウィンドウ操作（other_window など）の対象としたくないアプリケーションソフトのプロセス名称を指定する
    # （正規表現で指定してください（複数指定する場合は「|」で連結してください））
    fc.window_operation_exclusion_process = r"RocketDock\.exe"  # サンプルとして RocketDock.exe を登録

    # クリップボードリストを起動するキーを指定する
    fc.clipboardList_key = "A-y"

    # ランチャーリストを起動するキーを指定する
    fc.lancherList_key = "A-l"

    # shell_command 関数で起動するアプリケーションソフトを指定する
    # （PATH が通っていない場所にあるコマンドは、絶対パスで指定してください）
    fc.command_name = r"cmd.exe"

    # コマンドのリピート回数の最大値を指定する
    # （数値を大きくしていくと「Time stamp inversion happened.」が発生するので注意してください）
    fc.repeat_max = 128

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

    # ゲームなど、キーバインドの設定を極力行いたくないアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトルのリスト（ワイルドカード指定可、リストの後ろの項目から省略可）
    #   を指定してください）
    # （keymap_global 以外のすべてのキーマップをスルーします。ゲームなど、Keyhac によるキー設定と
    #   相性が悪いアプリケーションソフトを指定してください。keymap_base の設定もスルーするため、
    #   英語 -> 日本語キーボード変換の機能が働かなくなることにご留意ください。）
    # （msrdc.exe の行の有効化の必要性については、次のコミットの説明を参照してください。
    #   https://github.com/smzht/fakeymacs/commit/5ceb921bd754ce348f9cd79b6606086916520945）
    fc.game_app_list        = ["ffxiv_dx11.exe",              # FINAL FANTASY XIV
                               # ["msrdc.exe", "RAIL_WINDOW"],  # WSLg
                               ]

    # ウィンドウのタイトルが変わった時にキーバインドの再設定を行うアプリケーションソフトの
    # プロセス名称（ワイルドカード指定可）を指定する
    fc.name_change_app_list = ["chrome.exe",
                               "msedge.exe",
                               "firefox.exe",
                               "WindowsTerminal.exe",
                               "powershell.exe",
                               "cmd.exe",
                               "ubuntu*.exe",
                               "mc.exe",
                               ]

    # keyboard_quit 関数で、Esc を発行しないアプリケーションソフトを指定する
    # （アプリケーションソフトは、プロセス名称のみ（ワイルドカード指定可）、もしくは、プロセス名称、
    #   クラス名称、ウィンドウタイトル（リストによる複数指定可）のリスト（ワイルドカード指定可、
    #   リストの後ろの項目から省略可）を指定してください）
    fc.keyboard_quit_no_esc_app_list = [["WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                                         ["*PowerShell*", "*コマンド プロンプト*", "*Command Prompt*"]],
                                        ["powershell.exe", "ConsoleWindowClass", "*PowerShell*"],
                                        ["cmd.exe", "ConsoleWindowClass",
                                         ["*コマンド プロンプト*", "*Command Prompt*"]],
                                        ["EXCEL.EXE", "EXCEL*", ""], # Microsoft Excel のセル編集
                                        ["Evernote.exe", "WebViewHost"],
                                        ["LINE.exe", "Qt*QWindowIcon"],
                                        [None, "Chrome_WidgetWin_1", ["LINE",  "X *", "* / X*"]],
                                        ["firefox.exe", "MozillaWindowClass", ["X *", "* / X*"]],
                                        ["mstsc.exe", "RAIL_WINDOW", ["LINE*", "X *", "* / X*"]],
                                        ]

    # 個人設定ファイルのセクション [section-base-1] を読み込んで実行する
    exec(readConfigPersonal("[section-base-1]"), dict(globals(), **locals()))


    ###########################################################################
    ## ウィンドウフォーカスが変わった時、すぐに Keyhac に検知させるための設定
    ###########################################################################

    # IME の状態をテキスト カーソル インジケーターの色で表現するときに必要となる設定
    # （https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook）
    # （https://stackoverflow.com/questions/15849564/how-to-use-winapi-setwineventhook-in-python）
    # （https://tutorialmore.com/questions-652366.htm）
    # （https://www.nicovideo.jp/watch/sm20797948）

    def setWinEventHook():
        EVENT_SYSTEM_FOREGROUND = 0x0003
        EVENT_OBJECT_NAMECHANGE = 0x800C
        WINEVENT_OUTOFCONTEXT   = 0x0000

        user32 = ctypes.windll.user32
        ole32 = ctypes.windll.ole32

        try:
            # 変数が設定されていて０でない場合、イベントフックを解除する
            if keymap.fakeymacs_hook2 != 0:
                user32.UnhookWinEvent(keymap.fakeymacs_hook1)
        except:
            pass

        try:
            # 変数が設定されていて０でない場合、イベントフックを解除する
            if keymap.fakeymacs_hook2 != 0:
                user32.UnhookWinEvent(keymap.fakeymacs_hook2)
        except:
            pass

        ole32.CoUninitialize()
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

        regex = "|".join([fnmatch.translate(p) for p in fc.name_change_app_list])
        if regex == "": regex = "$." # 絶対にマッチしない正規表現
        name_change_app = re.compile(regex)

        def _callback(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
            if keymap.hook_enabled:
                if event == EVENT_SYSTEM_FOREGROUND:
                    delay(0.2)
                    if hwnd == user32.GetForegroundWindow():
                        keymap.delayedCall(keymap._updateFocusWindow, 0)

                elif event == EVENT_OBJECT_NAMECHANGE:
                    if hwnd == user32.GetForegroundWindow():
                        if idChild == 0:
                            try:
                                process_name = getProcessName()
                                if process_name and name_change_app.match(process_name):
                                    updateKeymap(True)
                            except:
                                pass
            else:
                setCursorColor(False)

        # この設定は必要（この設定がないと、Keyhac が落ちる場合がある）
        global WinEventProc

        WinEventProc = WinEventProcType(_callback)

        user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE

        keymap.fakeymacs_hook1 = user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            None,
            WinEventProc,
            0,
            0,
            WINEVENT_OUTOFCONTEXT
        )

        keymap.fakeymacs_hook2 = user32.SetWinEventHook(
            EVENT_OBJECT_NAMECHANGE,
            EVENT_OBJECT_NAMECHANGE,
            None,
            WinEventProc,
            0,
            0,
            WINEVENT_OUTOFCONTEXT
        )

    # ウィンドウが切り替わるときのイベントフックを設定する
    setWinEventHook()


    ###########################################################################
    ## 日本語キーボード設定をした OS 上で英語キーボードを利用するための設定
    ###########################################################################

    if use_usjis_keyboard_conversion:
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

    usjis_key_table = {"S-2"            : [["S-2"],                "Atmark"        ], # @
                       "S-6"            : [["S-6"],                "Caret"         ], # ^
                       "S-7"            : [["S-7"],                "S-6"           ], # &
                       "S-8"            : [["S-8"],                "S-Colon"       ], # *
                       "S-9"            : [["S-9"],                "S-8"           ], # (
                       "S-0"            : [["S-0"],                "S-9"           ], # )
                       "S-Minus"        : [["S-Minus"],            "S-BackSlash"   ], # _
                       "Plus"           : [["Caret"],              "S-Minus"       ], # =
                       "S-Plus"         : [["S-Caret"],            "S-Semicolon"   ], # +
                       "OpenBracket"    : [["Atmark"],             "OpenBracket"   ], # [
                       "S-OpenBracket"  : [["S-Atmark"],           "S-OpenBracket" ], # {
                       "CloseBracket"   : [["OpenBracket"],        "CloseBracket"  ], # ]
                       "S-CloseBracket" : [["S-OpenBracket"],      "S-CloseBracket"], # }
                       "BackSlash"      : [["CloseBracket"],       "Yen"           ], # \
                       "S-BackSlash"    : [["S-CloseBracket"],     "S-Yen"         ], # |
                       "S-Semicolon"    : [["S-Semicolon"],        "Colon"         ], # :
                       "Quote"          : [["Colon"],              "S-7"           ], # '
                       "S-Quote"        : [["S-Colon"],            "S-2"           ], # "
                       "BackQuote"      : [["(243)", "(244)"],     "S-Atmark"      ], # `
                       "S-BackQuote"    : [["S-(243)", "S-(244)"], "S-Caret"       ], # ~
                       "(243)"          : [[],                     "(243)"         ], # <半角／全角>
                       "S-(243)"        : [[],                     "S-(243)"       ], # S-<半角／全角>
                       "(244)"          : [[],                     "(244)"         ], # <半角／全角>
                       "S-(244)"        : [[],                     "S-(244)"       ], # S-<半角／全角>
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
            for us_key, jis_list in usjis_key_table.items():
                if re.search(rf"(^|[^S]-){re.escape(us_key)}$", key):
                    for jis_pos_key in jis_list[0]:
                        key_list.append(key.replace(us_key, jis_pos_key))
                    match_flg = True
                    break
        if not match_flg:
            key_list.append(key)
        return key_list

    def usjisInput(key):
        key = keyStrNormalization(key)
        if use_usjis_keyboard_conversion:
            for us_key, jis_list in usjis_key_table.items():
                if re.search(rf"(^|[^S]-){re.escape(us_key)}$", key):
                    jis_input_key = jis_list[1]
                    key = key.replace(us_key, jis_input_key)
                    break
        return key


    ###########################################################################
    ## 基本機能の設定
    ###########################################################################

    fakeymacs.window = None
    fakeymacs.process_name = None
    fakeymacs.not_emacs_keybind = []
    fakeymacs.not_ime_keybind = []
    fakeymacs.ime_cancel = False
    fakeymacs.last_window = None
    fakeymacs.force_update = False
    fakeymacs.clipboard_hook = True
    fakeymacs.last_keys = [None, None]
    fakeymacs.correct_ime_status = False
    fakeymacs.window_list = []
    fakeymacs.delayed_command = None
    fakeymacs.shift_down = False
    fakeymacs.shift_down2 = False

    regex = "|".join([fnmatch.translate(p) for p in fc.transparent_target])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    transparent_target = re.compile(regex)

    regex = "|".join([fnmatch.translate(c) for c in fc.transparent_target_class])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    transparent_target_class = re.compile(regex)

    regex = "|".join([fnmatch.translate(p) for p in fc.not_clipboard_target])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    not_clipboard_target = re.compile(regex)

    regex = "|".join([fnmatch.translate(c) for c in fc.not_clipboard_target_class])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    not_clipboard_target_class = re.compile(regex)

    regex = "|".join([fnmatch.translate(c) for c in fc.emacs_target_class])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    emacs_target_class = re.compile(regex)

    regex = "|".join([fnmatch.translate(app) for app in fc.emacs_target if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    emacs_target1 = re.compile(regex)
    emacs_target2 = [app for app in fc.emacs_target if type(app) is list]

    regex = "|".join([fnmatch.translate(app) for app in fc.not_emacs_target if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    not_emacs_target1 = re.compile(regex)
    not_emacs_target2 = [app for app in fc.not_emacs_target if type(app) is list]

    regex = "|".join([fnmatch.translate(app) for app in fc.ime_target if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    ime_target1 = re.compile(regex)
    ime_target2 = [app for app in fc.ime_target if type(app) is list]

    regex = "|".join([fnmatch.translate(app) for app in fc.game_app_list if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    game_app_list1 = re.compile(regex)
    game_app_list2 = [app for app in fc.game_app_list if type(app) is list]

    def is_base_target(window):
        if window is not fakeymacs.last_window:
            process_name = getProcessName(window)
            class_name   = getClassName(window)

            if (not_clipboard_target.match(process_name) or
                not_clipboard_target_class.match(class_name)):
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
            if any(checkWindow(*app, window=window) for app in fc.ctrl_button_app_list):
                fakeymacs.ctrl_button_app = True

            # Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
            # 開く機能がある。その挙動を抑制するための対策。
            d_ctrl = f"D-{fc.side_of_ctrl_key}Ctrl"
            if fakeymacs.ctrl_button_app:
                keymap_base[d_ctrl] = d_ctrl, "(255)"
            else:
                keymap_base[d_ctrl] = d_ctrl

            if is_task_switching_window(window) or is_list_window(window):
                fakeymacs.is_base_target = True
                fakeymacs.keymap_selected1 = True

            elif (transparent_target.match(process_name) or
                  transparent_target_class.match(class_name) or
                  game_app_list1.match(process_name) or
                  any(checkWindow(*app, window=window) for app in game_app_list2)):
                fakeymacs.is_base_target = False
                fakeymacs.keymap_selected1 = True
            else:
                if not fakeymacs.force_update:
                    if fc.use_ime_status_reset:
                        setImeStatus(0)
                    showImeStatus(window.getImeStatus(), window=window)

                fakeymacs.is_base_target = True
                fakeymacs.keymap_selected1 = False

        return fakeymacs.is_base_target

    fakeymacs.is_emacs_target = False

    def is_emacs_target(window):
        if window is not fakeymacs.last_window or fakeymacs.force_update:
            fakeymacs.is_emacs_target_in_previous_window = fakeymacs.is_emacs_target

            process_name = getProcessName(window)
            class_name   = getClassName(window)

            fakeymacs.keymap_selected2 = fakeymacs.keymap_selected1

            if fakeymacs.keymap_selected2 == False:
                if emacs_target_class.match(class_name):
                    fakeymacs.is_emacs_target = True

                elif process_name in fakeymacs.not_emacs_keybind:
                    fakeymacs.is_emacs_target = False

                elif (emacs_target1.match(process_name) or
                      any(checkWindow(*app, window=window) for app in emacs_target2)):
                    fakeymacs.is_emacs_target = True

                elif (not_emacs_target1.match(process_name) or
                      any(checkWindow(*app, window=window) for app in not_emacs_target2)):
                    fakeymacs.is_emacs_target = False
                else:
                    fakeymacs.is_emacs_target = True
            else:
                fakeymacs.is_emacs_target = False

            if fakeymacs.is_emacs_target == True:
                reset_undo(reset_counter(reset_mark(lambda: None)))()
                fakeymacs.ime_cancel = False

                if process_name in fc.emacs_exclusion_key:
                    fakeymacs.emacs_exclusion_key = [
                        keyStrNormalization(addSideOfModifierKey(specialCharToKeyStr(key)))
                        for key in fc.emacs_exclusion_key[process_name]]
                else:
                    fakeymacs.emacs_exclusion_key = []

                fakeymacs.keymap_selected2 = True

        return fakeymacs.is_emacs_target

    def is_ime_target(window):
        if window is not fakeymacs.last_window or fakeymacs.force_update:
            process_name = getProcessName(window)

            if fakeymacs.keymap_selected2 == False:
                if process_name in fakeymacs.not_ime_keybind:
                    setImeStatus(0)
                    fakeymacs.is_ime_target = False

                elif (ime_target1.match(process_name) or
                    any(checkWindow(*app, window=window) for app in ime_target2)):
                    fakeymacs.is_ime_target = True

                elif process_name in fakeymacs.not_emacs_keybind:
                    if (emacs_target1.match(process_name) or
                        any(checkWindow(*app, window=window) for app in emacs_target2)):
                        fakeymacs.is_ime_target = True

                    elif (not_emacs_target1.match(process_name) or
                        any(checkWindow(*app, window=window) for app in not_emacs_target2)):
                        fakeymacs.is_ime_target = False
                    else:
                        fakeymacs.is_ime_target = True
                else:
                    fakeymacs.is_ime_target = False
            else:
                fakeymacs.is_ime_target = False

        return fakeymacs.is_ime_target

    keymap_base = keymap.defineWindowKeymap(check_func=is_base_target)

    if fc.use_emacs_ime_mode:
        keymap_emacs = keymap.defineWindowKeymap(check_func=lambda wnd: (is_emacs_target(wnd) and
                                                                         not is_emacs_ime_mode(wnd)))
        keymap_ime   = keymap.defineWindowKeymap(check_func=lambda wnd: (is_ime_target(wnd) and
                                                                         not is_emacs_ime_mode(wnd)))
    else:
        keymap_emacs = keymap.defineWindowKeymap(check_func=is_emacs_target)
        keymap_ime   = keymap.defineWindowKeymap(check_func=is_ime_target)

    # mark がセットされると True になる
    fakeymacs.is_marked = False

    # リージョンを拡張する際に、順方向に拡張すると True、逆方向に拡張すると False になる
    fakeymacs.forward_direction = None

    # 検索画面が表示されるとされると False になり、検索が開始されると True になる
    fakeymacs.is_searching = None

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

    # Ctl-x プレフィックスキーを構成するキーの仮想キーコードを設定する
    if fc.ctl_x_prefix_key:
        keyCondition = usjisFilter(keyhac_keymap.KeyCondition.fromString, fc.ctl_x_prefix_key)

        if keyCondition.mod == keyhac_keymap.MODKEY_CTRL:
            if fc.side_of_ctrl_key == "L":
                ctl_x_prefix_vkey = [VK_LCONTROL, keyCondition.vk]
            else:
                ctl_x_prefix_vkey = [VK_RCONTROL, keyCondition.vk]

        elif keyCondition.mod == keyhac_keymap.MODKEY_ALT:
            if fc.side_of_alt_key == "L":
                ctl_x_prefix_vkey = [VK_LMENU, keyCondition.vk]
            else:
                ctl_x_prefix_vkey = [VK_RMENU, keyCondition.vk]
        else:
            print("Ctl-x プレフィックスキーのモディファイアキーは、Ctrl または Alt のいずれかから指定してください")

    # 「英語用キーボードドライバ置換」を利用する際の設定を行う
    # （https://github.com/smzht/fakeymacs/issues/55）
    # （https://github.com/kskmori/US-AltIME.ahk?tab=readme-ov-file#us101mode）
    if (ctypes.windll.user32.GetKeyboardLayout(0) >> 16) == 0x409:
        if fc.side_of_ctrl_key == "L":
            keymap.replaceKey("CapsLock", "LCtrl") # CapsLock キーを Ctrl キーに変換する設定
            keymap_base["RC-LCtrl"] = "CapsLock"   # C-CapsLock で CapsLock とする
        else:
            keymap.replaceKey("CapsLock", "RCtrl") # CapsLock キーを Ctrl キーに変換する設定
            keymap_base["LC-RCtrl"] = "CapsLock"   # C-CapsLock で CapsLock とする

    ##################################################
    ## キーマップを再読み込み
    ##################################################

    def update_keymap():
        keymap.popBalloon("keymap", "[Update keymap]", 1000)
        updateKeymap(True)

    ##################################################
    ## Emacs キーバインドの切り替え
    ##################################################

    def toggle_emacs_keybind():
        process_name = getProcessName()
        class_name   = getClassName()

        if not ((game_app_list1.match(process_name) or
                 any(checkWindow(*app) for app in game_app_list2)) or
                emacs_target_class.match(class_name)):

            if ((emacs_target1.match(process_name) or
                 any(checkWindow(*app) for app in emacs_target2)) or
                not (not_emacs_target1.match(process_name) or
                     any(checkWindow(*app) for app in not_emacs_target2))):

                if process_name in fakeymacs.not_emacs_keybind:
                    fakeymacs.not_emacs_keybind.remove(process_name)
                    keymap.popBalloon("keybind", "[Enable Emacs keybind]", 1000)
                else:
                    fakeymacs.not_emacs_keybind.append(process_name)
                    keymap.popBalloon("keybind", "[Disable Emacs keybind]", 1000)

            elif (ime_target1.match(process_name) or
                  any(checkWindow(*app) for app in ime_target2)):

                if process_name in fakeymacs.not_ime_keybind:
                    fakeymacs.not_ime_keybind.remove(process_name)
                    keymap.popBalloon("keybind", "[Enable IME keybind]", 1000)
                else:
                    fakeymacs.not_ime_keybind.append(process_name)
                    keymap.popBalloon("keybind", "[Disable IME keybind]", 1000)

            updateKeymap(True)

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
            # （RemoteApp を利用する際、IME の切り替えが正常に動作しない場合があるため、その対策を追加）
            if os_keyboard_type == "JP":
                self_insert_command("A-(243)")()
            else:
                self_insert_command("A-`")()

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
                # LINE アプリなど、Qt*QWindowIcon にマッチするクラスをもつアプリは入力文字に
                # バルーンヘルプが被るので、バルーンヘルプの表示対象から外す
                # （ただし、force が True の場合は除く）
                if force or not checkWindow(class_name="Qt*QWindowIcon", window=window):
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
        self_insert_command("C-S-s")()

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
        if (checkWindow("WINWORD.EXE", "_WwG") or
            checkWindow("POWERPNT.EXE", "mdiClass") or
            (checkWindow("EXCEL.EXE", "EXCEL*") and
             fc.is_newline_selectable_in_Excel)):
            if fakeymacs.is_marked:
                self_insert_command("Left")()

    def beginning_of_buffer():
        self_insert_command("C-Home")()

    def end_of_buffer():
        self_insert_command("C-End")()

    def goto_line():
        if (checkWindow("sakura.exe", "EditorClient") or
            checkWindow("sakura.exe", "SakuraView*")):
            self_insert_command3("C-j")()

        elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - micro*") or
              checkWindow(None, "ConsoleWindowClass", "* - micro*") or
              checkWindow("TeXworks.exe", "Qt661QWindowIcon")):
            self_insert_command3("C-l")()
        else:
            self_insert_command3("C-g")()

    def scroll_up():
        self_insert_command("PageUp")()

    def scroll_down():
        self_insert_command("PageDown")()

    def recenter():
        if (checkWindow("sakura.exe", "EditorClient") or
            checkWindow("sakura.exe", "SakuraView*")):
            self_insert_command("C-h")()
        else:
            # else の場合は、recenter のデフォルトキーバインドの C-l を発行する
            # （発行するキーを C-l と決め打ちにしているのは、ご了承ください）
            self_insert_command("C-l")()

    ##################################################
    ## カット / コピー / 削除 / アンドゥ
    ##################################################

    def delete_backward_char():
        self_insert_command("Back")()

    def delete_char():
        self_insert_command("Delete")()

    def backward_kill_word(repeat=1):
        resetRegion()
        setMark()

        def _move_beginning_of_region():
            for _ in range(repeat):
                backward_word()

        mark(_move_beginning_of_region, False)()
        delay()
        kill_region()

    def kill_word(repeat=1):
        resetRegion()
        setMark()

        def _move_end_of_region():
            for _ in range(repeat):
                forward_word()

        mark(_move_end_of_region, True)()
        delay()
        kill_region()

    def kill_line(repeat=1, kill_whole_line=False):
        resetRegion()
        setMark()

        if repeat == 1 and not kill_whole_line:
            mark(move_end_of_line, True)()
            delay()

            if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                            ["*PowerShell*", "*コマンド プロンプト*", "*Command Prompt*"]) or
                checkWindow("powershell.exe", "ConsoleWindowClass", "*PowerShell*") or
                checkWindow("cmd.exe", "ConsoleWindowClass",
                            ["*コマンド プロンプト*", "*Command Prompt*"])):
                kill_region()

            elif checkWindow(class_name="HM32CLIENT"): # Hidemaru Software
                kill_region()
                delay()
                if getClipboardText() == "":
                    self_insert_command("Delete")()
            else:
                # 改行を消せるようにするため Cut にはしていない
                copyRegion()
                self_insert_command("Delete")()
        else:
            def _move_end_of_region():
                if checkWindow("WINWORD.EXE", "_WwG"):
                    for _ in range(repeat):
                        next_line()
                    move_beginning_of_line()
                else:
                    for _ in range(repeat - 1):
                        next_line()
                    move_end_of_line()
                    forward_char()

            mark(_move_end_of_region, True)()
            delay()
            kill_region()

    def kill_region():
        # コマンドプロンプトには Cut に対応するショートカットがない。その対策。
        if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                        ["*コマンド プロンプト*", "*Command Prompt*"]) or
            checkWindow("cmd.exe", "ConsoleWindowClass",
                        ["*コマンド プロンプト*", "*Command Prompt*"])):
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
        if not checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                           ["*コマンド プロンプト*", "*Command Prompt*"]):
            resetRegion()

    def yank():
        if checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS"):
            self_insert_command("C-S-v")()
        else:
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
            resetMark()
        else:
            setMark()

    def mark_whole_buffer():
        if checkWindow("cmd.exe", "ConsoleWindowClass",
                       ["*コマンド プロンプト*", "*Command Prompt*"]):
            # "Home", "C-a" では上手く動かない場合がある
            self_insert_command("Home", "S-End")()
            fakeymacs.forward_direction = True # 逆の設定にする

        elif checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                         ["*コマンド プロンプト*", "*Command Prompt*"]):
            if fakeymacs.is_marked or fakeymacs.forward_direction is not None:
                self_insert_command("Esc")()

            # "Home", "C-a" では上手く動かない場合がある
            self_insert_command("Home", "C-S-m", "S-End")()
            fakeymacs.forward_direction = True # 逆の設定にする

        elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "*PowerShell*") or
              checkWindow("powershell.exe", "ConsoleWindowClass", "*PowerShell*")):
            self_insert_command("End", "S-Home")()
            fakeymacs.forward_direction = False

        elif (checkWindow("EXCEL.EXE", "EXCEL*") or
              checkWindow(class_name="Edit")):
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

        self_insert_command("Back")() # Delete は誤動作のもととなるので使わない

        backward_char()
        yank()
        forward_char()
        delay() # この delay を入れると、動作が安定する

        if fakeymacs.clipboard_hook:
            # クリップボードの監視用のフックを有効にする
            keymap.clipboard_history.enableHook(True)

    ##################################################
    ## バッファ / ウィンドウ操作
    ##################################################

    def kill_buffer():
        if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                        ["*PowerShell*", "*コマンド プロンプト*", "*Command Prompt*"])):
            self_insert_command("C-S-w")()

        elif (checkWindow("TeXworks.exe", "Qt661QWindowIcon") or
              checkWindow("Obsidian.exe", "Chrome_WidgetWin_1")):
            self_insert_command("C-w")()
        else:
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
        if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "*PowerShell*") or
            checkWindow("powershell.exe", "ConsoleWindowClass", "*PowerShell*")):
            self_insert_command({"backward":"C-r", "forward":"C-s"}[direction])()
        else:
            if fakeymacs.is_searching is None:
                self_insert_command("C-f")()

                if checkWindow("TeXworks.exe", "Qt661QWindowIcon"):
                    self_insert_command("Tab", "Tab")()

                fakeymacs.is_searching = False
            else:
                if checkWindow("EXCEL.EXE"):
                    if checkWindow(class_name="EDTBX"): # 検索ウィンドウ
                        self_insert_command({"backward":"A-S-f", "forward":"A-f"}[direction])()
                    else:
                        self_insert_command("C-f")()

                elif checkWindow("TeXworks.exe", "Qt661QWindowIcon"):
                    self_insert_command("C-g")()

                elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - edit*") or
                      checkWindow(None, "ConsoleWindowClass", "* - edit*")):
                    self_insert_command({"backward":"S-Enter", "forward":"Enter"}[direction])()

                elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - micro*") or
                      checkWindow(None, "ConsoleWindowClass", "* - micro*")):
                    self_insert_command({"backward":"C-p", "forward":"C-n"}[direction])()
                else:
                    self_insert_command({"backward":"S-F3", "forward":"F3"}[direction])()

    def isearch_backward():
        isearch("backward")

    def isearch_forward():
        isearch("forward")

    def query_replace():
        if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - edit*") or
            checkWindow(None, "ConsoleWindowClass", "* - edit*") or
            checkWindow("sakura.exe", "EditorClient") or
            checkWindow("sakura.exe", "SakuraView*")  or
            checkWindow(class_name="HM32CLIENT")):
            self_insert_command("C-r")()

        elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "* - micro*") or
              checkWindow(None, "ConsoleWindowClass", "* - micro*")):
            self_insert_command("C-e")()
            setImeStatus(0)
            keymap.InputTextCommand("replace ")()

        elif checkWindow("TeXworks.exe", "Qt661QWindowIcon"):
            self_insert_command("C-r")()
            self_insert_command("Tab", "Tab", "Tab")()
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

        # キーボードマクロの終了キー「Ctl-x プレフィックスキー + ")"」の Ctl-x プレフィックスキーがマクロに
        # 記録されてしまうのを対策する（キーボードマクロの終了キーの前提を「Ctl-xプレフィックスキー + ")"」
        # としていることについては、とりあえず了承ください。）
        if fc.ctl_x_prefix_key:
            if len(keymap.record_seq) >= 4:
                if (((keymap.record_seq[-1] == (ctl_x_prefix_vkey[0], True) and
                      keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], True)) or
                     (keymap.record_seq[-1] == (ctl_x_prefix_vkey[1], True) and
                      keymap.record_seq[-2] == (ctl_x_prefix_vkey[0], True))) and
                    keymap.record_seq[-3] == (ctl_x_prefix_vkey[1], False)):
                    for _ in range(3):
                        keymap.record_seq.pop()
                    if keymap.record_seq[-1] == (ctl_x_prefix_vkey[0], False):
                        for i in range(len(keymap.record_seq) - 1, -1, -1):
                            if keymap.record_seq[i] == (ctl_x_prefix_vkey[0], False):
                                keymap.record_seq.pop()
                            else:
                                break
                    else:
                        # コントロール系の入力が連続して行われる場合があるための対処
                        keymap.record_seq.append((ctl_x_prefix_vkey[0], True))

                elif ((ctypes.windll.user32.GetKeyboardLayout(0) >> 16) == 0x409 and
                      ((keymap.record_seq[-1] == (VK_CAPITAL, True) and
                        keymap.record_seq[-2] == (ctl_x_prefix_vkey[1], True)) or
                       (keymap.record_seq[-1] == (ctl_x_prefix_vkey[1], True) and
                        keymap.record_seq[-2] == (VK_CAPITAL, True))) and
                      keymap.record_seq[-3] == (ctl_x_prefix_vkey[1], False)):
                    for _ in range(3):
                        keymap.record_seq.pop()
                    if keymap.record_seq[-1] == (VK_CAPITAL, False):
                        for i in range(len(keymap.record_seq) - 1, -1, -1):
                            if keymap.record_seq[i] == (VK_CAPITAL, False):
                                keymap.record_seq.pop()
                            else:
                                break
                    else:
                        # コントロール系の入力が連続して行われる場合があるための対処
                        keymap.record_seq.append((VK_CAPITAL, True))

    def kmacro_end_and_call_macro():
        def _kmacro_end_and_call_macro():
            # キーボードマクロの最初が IME ON の場合、この delay が必要
            delay(0.2)
            fakeymacs.is_playing_kmacro = True
            setImeStatus(0)
            keymap.command_RecordPlay()
            fakeymacs.is_playing_kmacro = False

        keymap.delayedCall(_kmacro_end_and_call_macro, 0)

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

        if fakeymacs.is_searching == False:
            fakeymacs.is_searching = True

    def newline_and_indent():
        self_insert_command("Enter", "Tab")()

    def open_line():
        self_insert_command("Enter", "Up", "End")()

    def indent_for_tab_command():
        self_insert_command("Tab")()

    regex = "|".join([fnmatch.translate(app)
                      for app in fc.keyboard_quit_no_esc_app_list if type(app) is str])
    if regex == "": regex = "$." # 絶対にマッチしない正規表現
    keyboard_quit_no_esc_app_list1 = re.compile(regex)
    keyboard_quit_no_esc_app_list2 = [app for app in fc.keyboard_quit_no_esc_app_list
                                      if type(app) is list]

    def keyboard_quit(esc=True):
        resetRegion()

        if esc:
            # Esc を発行して問題ないアプリケーションソフトには Esc を発行する
            if not (keyboard_quit_no_esc_app_list1.match(getProcessName()) or
                    any(checkWindow(*app) for app in keyboard_quit_no_esc_app_list2)):
                escape()

        keymap.command_RecordStop()

        if fakeymacs.forward_direction is None:
            if fakeymacs.is_undo_mode:
                fakeymacs.is_undo_mode = False
            else:
                fakeymacs.is_undo_mode = True

        if fakeymacs.is_searching == False:
            fakeymacs.is_searching = None

    def kill_emacs():
        if (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", ["* - edit*", "* - micro*"]) or
            checkWindow(None, "ConsoleWindowClass", ["* - edit*", "* - micro*"])):
            setImeStatus(0)
            self_insert_command("C-q")()

        # Windows 11版 Notepad の場合、A-F4 が失敗することがあるので、C-S-w を発行する
        elif checkWindow("Notepad.exe", "RichEditD2DPT"):
            self_insert_command("C-S-w")()
        else:
            self_insert_command("A-F4")()

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

    def updateKeymap(force_update=False):
        fakeymacs.force_update = force_update
        keymap.updateKeymap()

    def delay(sec=0.02):
        time.sleep(sec)

    def setMark():
        if checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                       ["*コマンド プロンプト*", "*Command Prompt*"]):
            self_insert_command("C-S-m")()
        fakeymacs.is_marked = True

    def resetMark():
        fakeymacs.is_marked = False
        fakeymacs.forward_direction = None

    def copyRegion():
        self_insert_command("C-c")()
        # C-k (kill_line) したときに k 文字が混在することがあるため delayedCall とする
        keymap.delayedCall(pushToClipboardList, 100)

    def cutRegion():
        self_insert_command("C-x")()
        # C-k (kill_line) したときに k 文字が混在することがあるため delayedCall とする
        keymap.delayedCall(pushToClipboardList, 100)

    def pushToClipboardList():
        # clipboard 監視の対象外とするアプリケーションソフトで copy / cut した場合でも
        # クリップボードの内容をクリップボードリストに登録するための対策。
        # また、clipboard 監視の対象のアプリケーションソフトでも、マウスでリージョンを
        # 選択した際に copy / cut を行うと、リージョンの内容がクリップボードリストに
        # 反映されない場合がある。その対策でもある。
        clipboard_text = getClipboardText()
        if clipboard_text:
            if len(keymap.clipboard_history.items) > 0:
                if keymap.clipboard_history.items[0] != clipboard_text:
                    keymap.clipboard_history._push(clipboard_text)
            else:
                keymap.clipboard_history._push(clipboard_text)

    def resetRegion():
        if checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS",
                       ["*コマンド プロンプト*", "*Command Prompt*"]):
            if fakeymacs.is_marked or fakeymacs.forward_direction is not None:
                self_insert_command("Esc")()

        elif fakeymacs.forward_direction is not None:
            if checkWindow(class_name="Edit"):
                # 選択されているリージョンのハイライトを解除するためにカーソルキーを発行する
                if fakeymacs.forward_direction:
                    self_insert_command("Right")()
                else:
                    self_insert_command("Left")()

            elif (checkWindow("EXCEL.EXE", "EXCEL*", "?*") or # Microsoft Excel のセル編集でない場合
                  checkWindow("cmd.exe", "ConsoleWindowClass",
                              ["*コマンド プロンプト*", "*Command Prompt*"])):
                # 選択されているリージョンのハイライトを解除するためにカーソルを移動する
                if fakeymacs.forward_direction:
                    self_insert_command("Right", "Left")()
                else:
                    self_insert_command("Left", "Right")()

            elif (checkWindow("WindowsTerminal.exe", "CASCADIA_HOSTING_WINDOW_CLASS", "*PowerShell*") or
                  checkWindow("powershell.exe", "ConsoleWindowClass", "*PowerShell*")):
                # 選択されているリージョンのハイライトを解除するためにカーソルを移動する
                if fakeymacs.forward_direction:
                    self_insert_command("Left", "Right")()
                else:
                    self_insert_command("Right", "Left")()
            else:
                # 選択されているリージョンのハイライトを解除するためにカーソルキーを発行する
                if fakeymacs.forward_direction:
                    self_insert_command("Right")()
                else:
                    self_insert_command("Left")()

    def getProcessName(window=None):
        if window is None:
            window = keymap.getWindow()

        if window is not fakeymacs.window:
            fakeymacs.window = window
            fakeymacs.process_name = window.getProcessName()

        return fakeymacs.process_name

    def getClassName(window=None):
        if window is None:
            window = keymap.getWindow()

        return window.getClassName()

    def getText(window=None):
        if window is None:
            window = keymap.getWindow()

        return window.getText()

    def checkWindow(process_name=None, class_name=None, text=None, window=None):
        if window is None:
            window = keymap.getWindow()

        window_process_name = getProcessName(window)
        window_class_name   = getClassName(window)

        if (window_process_name == "WindowsTerminal.exe" and
            window_class_name   == "Windows.UI.Input.InputSite.WindowClass"):
            window = window.getParent().getParent()
            window_class_name = getClassName(window)

        if ((process_name is None or fnmatch.fnmatch(window_process_name, process_name)) and
            (class_name is None or fnmatch.fnmatchcase(window_class_name, class_name))):
            if text is None:
                return True
            else:
                title = getText(window)
                if type(text) is list:
                    return any(fnmatch.fnmatchcase(title, t) for t in text)
                else:
                    return fnmatch.fnmatchcase(title, text)
        else:
            return False

    def vkeys():
        vkeys = list(usjisFilter(lambda: keyhac_keymap.KeyCondition.vk_str_table))
        for vkey in [VK_MENU, VK_LMENU, VK_RMENU, VK_CONTROL, VK_LCONTROL, VK_RCONTROL,
                     VK_SHIFT, VK_LSHIFT, VK_RSHIFT, VK_LWIN, VK_RWIN]:
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
        n = 1 if is_japanese_keyboard else 0
        for special_char, key_str in special_char_key_table.items():
            if re.search(rf"(^|-){re.escape(special_char)}$", key):
                key = key[:-1] + key_str[n]
                break
        return key

    def addSideOfModifierKey(key):
        key = re.sub(r"(^|-)(C-)", rf"\1{fc.side_of_ctrl_key}\2", key)
        key = re.sub(r"(^|-)(A-)", rf"\1{fc.side_of_alt_key}\2", key)
        key = re.sub(r"(^|-)(W-)", rf"\1{fc.side_of_win_key}\2", key)
        key = re.sub(r"(^|-)(U.-)", rf"\1L\2", key)
        return key

    def kbd(keys):
        key_lists = []

        if keys:
            key_list0 = []
            key_list1 = []
            key_list2 = []
            key_lists0 = []

            for key in map(specialCharToKeyStr, keys.split()):
                if key == "Ctl-x":
                    key = fc.ctl_x_prefix_key

                if key == "M-":
                    if fc.use_esc_as_meta:
                        key_list1 = key_list0 + ["Esc"]

                    if fc.use_ctrl_openbracket_as_meta:
                        key_list2 = key_list0 + ["C-OpenBracket"]

                    key_list0 = []
                    break

                if "M-" in key:
                    key_list0.append(key.replace("M-", "A-"))

                    if fc.use_esc_as_meta:
                        key_list1.append("Esc")
                        key_list1.append(key.replace("M-", ""))

                    elif fc.use_ctrl_openbracket_as_meta:
                        key_list2.append("C-OpenBracket")
                        key_list2.append(key.replace("M-", ""))
                else:
                    key_list0.append(key)

                    if fc.use_esc_as_meta:
                        key_list1.append(key)

                    elif fc.use_ctrl_openbracket_as_meta:
                        key_list2.append(key)

            if key_list0:
                key_lists0.append(key_list0)

            if key_list1:
                if key_list0 != key_list1:
                    key_lists0.append(key_list1)

            if key_list2:
                if key_list0 != key_list2:
                    key_lists0.append(key_list2)

            for key_list in key_lists0:
                key_list[0] = addSideOfModifierKey(key_list[0])
                key_lists.append(list(map(keyStrNormalization, key_list)))

        return key_lists

    def keyPos(key_list):
        return list(itertools.product(*map(usjisPos, key_list)))

    def keyInput(key_list):
        return list(map(usjisInput, key_list))

    command_dict = {}

    def define_key(window_keymap, keys, command, skip_check=True):
        nonlocal keymap_base
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
                            print(f"skip settings key : [{keymap_name}] {keys}")
                            return
                    break

        def _keyCommand1(key_list):
            nonlocal keymap_emacs

            if callable(command):
                if (len(key_list) == 1 and
                    "keymap_emacs" in locals() and
                    window_keymap is locals()["keymap_emacs"]):

                    def _command1():
                        if key_list[0] in fakeymacs.emacs_exclusion_key:
                            try:
                                func = command_dict[(keymap_base, tuple(key_list))]
                            except:
                                func = InputKeyCommand(key_list[0])
                            func()
                        else:
                            command()
                else:
                    _command1 = command

                return _command1
            else:
                return command

        def _keyCommand2(key_list):
            _command1 = command_dict[(window_keymap, tuple(key_list))] = _keyCommand1(key_list)
            up_key = key_list[0].startswith("U-")

            if callable(_command1):
                def _command2():
                    if not up_key:
                        if fakeymacs.delayed_command:
                            _command = fakeymacs.delayed_command
                            fakeymacs.delayed_command = None
                            _command()

                    fakeymacs.update_last_keys = True
                    _command1()
                    if fakeymacs.update_last_keys:
                        fakeymacs.last_keys = [window_keymap, keys]

                    if up_key:
                        if fakeymacs.delayed_command:
                            _command = fakeymacs.delayed_command
                            fakeymacs.delayed_command = None
                            _command()

                return _command2
            else:
                return _command1

        for key_list in kbd(keys):
            for pos_list in keyPos(key_list):
                w_keymap = window_keymap
                for key in pos_list[:-1]:
                    w_keymap = w_keymap[key]
                w_keymap[pos_list[-1]] = _keyCommand2(key_list)

                if len(pos_list) == 1:
                    # Alt キーを単押しした際に、カーソルがメニューへ移動しないようにするための対策
                    # （https://www.haijin-boys.com/discussions/4583）
                    if re.fullmatch(r"O-LAlt", pos_list[0], re.IGNORECASE):
                        window_keymap["D-LAlt"] = "D-LAlt", "(255)"

                    elif re.fullmatch(r"O-RAlt", pos_list[0], re.IGNORECASE):
                        window_keymap["D-RAlt"] = "D-RAlt", "(255)"

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

    def getKeyAction(key):
        key_list = kbd(key)[0]
        pos_list = keyPos(key_list)[0]
        if len(pos_list) == 1:
            key_cond = keyhac_keymap.KeyCondition.fromString(pos_list[0])
            def _func():
                try:
                    keymap.current_map[key_cond]()
                except:
                    self_insert_command(key)()
        else:
            _func = lambda: None

        return _func

    def getKeyCommand(window_keymap, keys):
        key_list = kbd(keys)[0]
        try:
            func = command_dict[(window_keymap, tuple(key_list))]
        except:
            func = None

        return func

    def makeKeyCommand(window_keymap, keys, command, check_func):
        key_list = kbd(keys)[0]
        try:
            func = command_dict[(window_keymap, tuple(key_list))]
        except:
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
            key_list = keyInput(key_list)

        if "S-" in key_list[-1]:
            shift_check = True
        else:
            shift_check = False

        def _func():
            key_list2 = list(key_list)

            if shift_check:
                # 「define_key(keymap_base, "W-S-m", self_insert_command("W-S-m"))」のような設定を
                # した場合、 Shift に RShift を使うと正常に動作しない。その対策。
                if (keymap.modifier & keyhac_keymap.MODKEY_SHIFT_R and
                    (keymap.modifier & (keyhac_keymap.MODKEY_WIN_L | keyhac_keymap.MODKEY_WIN_R) or
                     keymap.modifier & (keyhac_keymap.MODKEY_ALT_L | keyhac_keymap.MODKEY_ALT_R))):
                    key_list2[-1] = re.sub(r"(^|-)(S-)", r"\1R\2", key_list2[-1])

            if fakeymacs.shift_down:
                key_list2 = ["D-Shift"] + key_list2 + ["U-Shift"]

            if fakeymacs.shift_down2:
                key_list2 = ["U-Shift"] + key_list2 + ["D-Shift"]

            keymap.InputKeyCommand(*key_list2)()

            # Microsoft Word 等では画面に Ctrl ボタンが表示され、Ctrl キーの単押しによりサブウインドウが
            # 開く機能がある。その挙動を抑制するための対策。
            if fakeymacs.ctrl_button_app:
                if keyhac_keymap.checkModifier(keymap.modifier, keyhac_keymap.MODKEY_CTRL):
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

    def self_insert_command4(*key_list, usjis_conv=True):
        func = self_insert_command(*key_list, usjis_conv=usjis_conv)
        def _func():
            ime_status = getImeStatus()
            if ime_status:
                setImeStatus(0)
            func()
            if ime_status:
                delay()
                setImeStatus(1)
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
        def _func():
            if fakeymacs.is_marked:
                fakeymacs.shift_down = True
                func()
                fakeymacs.shift_down = False

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
            resetMark()
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
            if fakeymacs.is_searching:
                fakeymacs.is_searching = None
        return _func

    def repeat(func):
        def _func():
            if fakeymacs.repeat_counter > fc.repeat_max:
                print(f"コマンドのリピート回数の最大値 {fc.repeat_max} を超えています")
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
            delay()
            setImeStatus(1)

    def reloadConfig(mode):
        if mode == 1:
            keymap.fakeymacs_keyboard = "US"
        elif mode == 2:
            keymap.fakeymacs_keyboard = "JP"

        keymap.command_ReloadConfig()
        keymap.popBalloon("reloaded", "[Reloaded]", 1000)

    def editConfigPersonal():
        config_filename = rf"{dataPath()}\config_personal.py"

        def jobEditConfig(job_item):
            keymap.editTextFile(config_filename)

        def jobEditConfigFinished(job_item):
            print(ckit.strings["log_config_editor_launched"])
            print("")

        job_item = ckit.JobItem(jobEditConfig, jobEditConfigFinished)
        ckit.JobQueue.defaultQueue().enqueue(job_item)

    ##################################################
    ## キーバインド
    ##################################################

    # キーバインドの定義に利用している表記の意味は次のとおりです。
    # ・S-    : Shift キー（左右どちらでも）
    # ・C-    : Ctrl キー（fc.side_of_ctrl_key 変数で指定した側のキー）
    # ・LC-   : 左 Ctrl キー
    # ・RC-   : 右 Ctrl キー
    # ・A-    : Alt キー（fc.side_of_alt_key 変数で指定した側のキー）
    # ・LA-   : 左 Alt キー
    # ・RA-   : 右 Alt キー
    # ・W-    : Win キー（fc.side_of_win_key 変数で指定した側のキー）
    # ・LW-   : 左 Win キー
    # ・RW-   : 右 Win キー
    # ・M-    : Alt キー と Esc、C-[ のプレフィックスキーを利用する３パターンを定義（Emacs の Meta と同様）
    # ・Ctl-x : fc.ctl_x_prefix_key 変数で定義されているプレフィックスキーに置換え
    # ・(999) : 仮想キーコード指定

    # https://github.com/crftwr/keyhac/blob/master/keyhac_keymap.py
    # https://github.com/crftwr/pyauto/blob/master/pyauto_const.py
    # https://bsakatu.net/doc/virtual-key-of-windows/
    # http://www3.airnet.ne.jp/saka/hardware/keyboard/109scode.html

    ## 全てのキーパターンの設定（キーの入力記録を残すための設定）
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
            mkey = mod1 + mod2 + mod3 + mod4 + key
            define_key(keymap_base, mkey, self_insert_command(mkey))

    # US と JIS のキーボード変換の機能を有効にしている場合は、変換が必要となるキーを、左右両方の
    # モディファイアキーの全てのパターンで keymap_base に登録する
    if use_usjis_keyboard_conversion:
        for us_key, jis_list in usjis_key_table.items():
            if jis_list[0]:
                for mod1, mod2, mod3 in itertools.product(["", "LW-", "RW-"],
                                                          ["", "LA-", "RA-"],
                                                          ["", "LC-", "RC-"]):
                    mkey = mod1 + mod2 + mod3 + us_key
                    if not getKeyCommand(keymap_base, mkey):
                        define_key(keymap_base, mkey, self_insert_command(mkey))

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
            define_key(keymap_emacs, f"C-{key}", digit2(n))
        define_key(keymap_emacs, f"M-{key}", digit2(n))
        define_key(keymap_emacs, f"S-{key}", reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(f"S-{key}"))))))
        for mod in ["", "S-"]:
            mkey = mod + key
            define_key(keymap_ime, mkey, self_insert_command2(mkey))

    ## アルファベットキーの設定
    for vkey in range(VK_A, VK_Z + 1):
        key = vkToStr(vkey)
        for mod in ["", "S-"]:
            mkey = mod + key
            define_key(keymap_emacs, mkey, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(mkey))))))
            define_key(keymap_ime,   mkey, self_insert_command2(mkey))

    ## 特殊文字キーの設定
    define_key(keymap_emacs, "Space"  , reset_undo(reset_counter(reset_mark(repeat(space)))))
    define_key(keymap_emacs, "S-Space", reset_undo(reset_counter(reset_mark(repeat(self_insert_command("S-Space"))))))

    for vkey in [VK_OEM_MINUS, VK_OEM_PLUS, VK_OEM_COMMA, VK_OEM_PERIOD,
                 VK_OEM_1, VK_OEM_2, VK_OEM_3, VK_OEM_4, VK_OEM_5, VK_OEM_6, VK_OEM_7, VK_OEM_102]:
        key = vkToStr(vkey)
        for mod in ["", "S-"]:
            mkey = mod + key
            define_key(keymap_emacs, mkey, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(mkey))))))
            define_key(keymap_ime,   mkey, self_insert_command2(mkey))

    ## 10key の特殊文字キーの設定
    for vkey in [VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE]:
        key = vkToStr(vkey)
        define_key(keymap_emacs, key, reset_undo(reset_counter(reset_mark(repeat(self_insert_command2(key))))))
        define_key(keymap_ime,   key, self_insert_command2(key))

    ## quoted-insert キーの設定
    for vkey in vkeys():
        key = vkToStr(vkey)
        for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
            mkey = mod1 + mod2 + mod3 + mod4 + key
            define_key(keymap_emacs, f"C-q {mkey}", self_insert_command(mkey))

    ## Esc キーの設定
    if fc.use_esc_as_meta:
        define_key(keymap_emacs, "Esc Esc", reset_undo(reset_counter(escape)))
    else:
        define_key(keymap_emacs, "Esc", reset_undo(reset_counter(escape)))

    if fc.use_ctrl_openbracket_as_meta:
        define_key(keymap_emacs, "C-[ C-[", reset_undo(reset_counter(escape)))
    else:
        define_key(keymap_emacs, "C-[", reset_undo(reset_counter(escape)))

    ## universal-argument キーの設定
    define_key(keymap_emacs, "C-u", universal_argument)

    ## 「IME の切り替え」のキー設定
    define_key(keymap_base, "C-`",     toggle_input_method) # C-` キー
    define_key(keymap_base, "A-(25)",  toggle_input_method) # A-` キー
    define_key(keymap_base, "(243)",   toggle_input_method) # <半角／全角> キー
    define_key(keymap_base, "(244)",   toggle_input_method) # <半角／全角> キー
    define_key(keymap_base, "C-(243)", toggle_input_method) # C-<半角／全角> キー
    define_key(keymap_base, "C-(244)", toggle_input_method) # C-<半角／全角> キー
    define_key(keymap_base, "(240)",   toggle_input_method) # CapsLock キー
    define_key(keymap_base, "S-(240)", toggle_input_method) # S-CapsLock キー

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
    define_key(keymap_emacs, "PageUp",   reset_search(reset_undo(reset_counter(mark(scroll_up, False)))))
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
    define_key(keymap_emacs, "S-PageUp",   reset_search(reset_undo(reset_counter(mark2(scroll_up, False)))))
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
            # Google 日本語入力を利用している時、ime_cancel_key に設定しているキーがキーバインドに
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
    ## Emacs 日本語入力モードの設定
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

        # Emacs 日本語入力モードが開始されたときのウィンドウオブジェクトを格納する変数を初期化する
        fakeymacs.ei_last_window = None

        ##################################################
        ## Emacs 日本語入力モード の切り替え
        ##################################################

        def enable_emacs_ime_mode(delay=0):
            fakeymacs.ei_last_window = keymap.getWindow()
            ei_updateKeymap(delay)

        def disable_emacs_ime_mode():
            fakeymacs.ei_last_window = None
            ei_updateKeymap(0)

        ##################################################
        ## IME の切り替え（Emacs 日本語入力モード用）
        ##################################################

        def ei_enable_input_method():
            # IME の状態のバルーンヘルプを表示するために敢えてコールする
            enable_input_method()

        def ei_disable_input_method():
            disable_emacs_ime_mode()
            disable_input_method()

        def ei_enable_input_method2(key, command):
            func = command
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

        def ei_disable_input_method2(key, command):
            func = command
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
        ## その他（Emacs 日本語入力モード用）
        ##################################################

        def ei_newline():
            self_insert_command("Enter")()
            fakeymacs.ime_cancel = True
            disable_emacs_ime_mode()

        def ei_keyboard_quit():
            escape()
            disable_emacs_ime_mode()

        ##################################################
        ## 共通関数（Emacs 日本語入力モード用）
        ##################################################

        def ei_popBalloon(ime_mode_status):
            if not fakeymacs.is_playing_kmacro:
                if fc.emacs_ime_mode_balloon_message:
                    # LINE アプリなど、Qt*QWindowIcon にマッチするクラスをもつアプリは入力文字に
                    # バルーンヘルプが被るので、バルーンヘルプの表示対象から外す
                    if not checkWindow(class_name="Qt*QWindowIcon"):
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
        ## キーバインド（Emacs 日本語入力モード用）
        ##################################################

        ## 「IME の切り替え」のキー設定
        define_key(keymap_ei, "C-`",     ei_disable_input_method) # C-` キー
        define_key(keymap_ei, "A-(25)",  ei_disable_input_method) # A-` キー
        define_key(keymap_ei, "(243)",   ei_disable_input_method) # <半角／全角> キー
        define_key(keymap_ei, "(244)",   ei_disable_input_method) # <半角／全角> キー
        define_key(keymap_ei, "C-(243)", ei_disable_input_method) # C-<半角／全角> キー
        define_key(keymap_ei, "C-(244)", ei_disable_input_method) # C-<半角／全角> キー
        define_key(keymap_ei, "(240)",   ei_disable_input_method) # CapsLock キー
        define_key(keymap_ei, "S-(240)", ei_disable_input_method) # S-CapsLock キー

        ## Esc キーの設定
        define_key(keymap_ei, "Esc", escape)
        define_key(keymap_ei, "C-[", escape)

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

        # この時点の command を保存する
        command_keep = {}
        for key in fc.toggle_input_method_key:
            command_keep[key] = getKeyCommand(keymap_ei, key)
        for disable_key, enable_key in fc.set_input_method_key:
            if disable_key:
                command_keep[disable_key] = getKeyCommand(keymap_ei, disable_key)
            if enable_key:
                command_keep[enable_key] = getKeyCommand(keymap_ei, enable_key)

        ## 「IME の切り替え」のキー設定
        for key in fc.toggle_input_method_key:
            define_key(keymap_ei, key, ei_disable_input_method2(key, command_keep[key]))

        ## 「IME の切り替え」のキー設定
        for disable_key, enable_key in fc.set_input_method_key:
            if disable_key:
                define_key(keymap_ei, disable_key,
                           ei_disable_input_method2(disable_key, command_keep[disable_key]))
            if enable_key:
                define_key(keymap_ei, enable_key,
                           ei_enable_input_method2(enable_key, command_keep[enable_key]))


    ###########################################################################
    ## 「キーマップの再設定」のキー設定
    ###########################################################################

    def is_global_target(window):
        global global_target_status

        if window is not fakeymacs.last_window:
            if (transparent_target.match(getProcessName(window)) or
                transparent_target_class.match(getClassName(window))):
                global_target_status = False
            else:
                global_target_status = True

        fakeymacs.last_window = window
        fakeymacs.force_update = False

        return global_target_status

    keymap_global = keymap.defineWindowKeymap(check_func=is_global_target)

    define_key(keymap_global, fc.update_keymap_key, update_keymap)


    ###########################################################################
    ## 「Emacs キーバインドの切り替え」のキー設定
    ###########################################################################

    define_key(keymap_global, fc.toggle_emacs_keybind_key, toggle_emacs_keybind)


    ###########################################################################
    ## Ctrl-Tab キーの設定
    ###########################################################################

    define_key(keymap_global, "C-Tab", switch_to_buffer)


    ###########################################################################
    ## アプリケーションキーの設定
    ###########################################################################

    define_key(keymap_global, fc.application_key, self_insert_command("Apps"))


    ###########################################################################
    ## ファンクションキーの設定
    ###########################################################################

    if fc.use_alt_digit_key_for_f1_to_f12:
        for mod1, mod2, mod3 in itertools.product(["", "W-"], ["", "C-"], ["", "S-"]):
            mod = "A-" + mod1 + mod2 + mod3

            for i in range(10):
                define_key(keymap_global,
                           mod + f"{(i + 1) % 10}", self_insert_command(mod + vkToStr(VK_F1 + i)))

            define_key(keymap_global, mod + "-", self_insert_command(mod + vkToStr(VK_F11)))

            if is_japanese_keyboard:
                define_key(keymap_global, mod + "^", self_insert_command(mod + vkToStr(VK_F12)))
            else:
                define_key(keymap_global, mod + "=", self_insert_command(mod + vkToStr(VK_F12)))


    ###########################################################################
    ## デスクトップの設定
    ###########################################################################

    ##################################################
    ## ウィンドウ操作（デスクトップ用）
    ##################################################

    def getTopLevelWindow():
        window = keymap.getTopLevelWindow()
        if (window and
            window.getProcessName() == "explorer.exe" and
            window.getClassName() in ["WorkerW", "Shell_TrayWnd"]):
            return None
        else:
            return window

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

    def getWindowList(minimized_window=None, process_name=None):
        def _makeWindowList(window, arg):
            nonlocal window_title

            if window.isVisible() and not window.getOwner():
                process_name2 = window.getProcessName()

                if process_name is None or process_name == process_name2:
                    class_name = window.getClassName()

                    # ハイフンの前に見えない文字がある場合の対策
                    title = re.sub(r".* ‎- ", r"", window.getText())

                    # RemoteApp を利用する際のおまじない
                    if (process_name2 == "mstsc.exe" and
                        class_name == "RAIL_WINDOW" and
                        title == " (リモート)"):
                        pass

                    elif class_name == "Emacs" or title != "":
                        if (not re.fullmatch(fc.window_operation_exclusion_class, class_name) and
                            not re.fullmatch(fc.window_operation_exclusion_process, process_name2)):

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
        Window.enum(_makeWindowList, None)

        if minimized_window is None:
            window_list2 = window_list
        else:
            window_list2 = []
            for window in window_list:
                if ((minimized_window and window.isMinimized()) or
                    (not minimized_window and not window.isMinimized())):
                    window_list2.append(window)

        return window_list2

    ##################################################
    ## キーバインド（デスクトップ用）
    ##################################################

    # 表示しているウィンドウの中で、一番最近までフォーカスがあったウィンドウに移動
    define_key(keymap_global, fc.other_window_key, other_window)

    # IME の「単語登録」プログラムの起動
    define_key(keymap_global, fc.word_register_key,
               keymap.ShellExecuteCommand(None, fc.word_register_name, fc.word_register_param, ""))


    ###########################################################################
    ## タスク切り替え画面／タスクビューの設定
    ###########################################################################

    def is_task_switching_window(window):
        if (getProcessName(window) == "explorer.exe" and
            getClassName(window) in ["MultitaskingViewFrame",
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
    # Emacs キーバインドを適用していないアプリケーションソフトでも利用できるようにするため、
    # クリップボードリストで Enter を押下した際の挙動を、次のとおりに切り分けています。
    #
    # １）Emacs キーバインドを適用しているアプリケーションソフトからクリップボードリストを起動
    #     →   Enter（テキストの貼り付け）
    # ２）Emacs キーバインドを適用していないアプリケーションソフトからクリップボードリストを起動
    #     → S-Enter（テキストをクリップボードに格納）
    #
    # ※ Emacs キーバインドを適用しないアプリケーションソフトには、文字の入出力の方式が特殊な
    #    ものもあるため、テキストの貼り付けはそのアプリケーションソフトのペースト操作で行う
    #    ことを前提としています。
    # ※ C-Enter（引用記号付で貼り付け）の置き換えは、対応が複雑となるため行っておりません。

    def is_list_window(window):
        if getClassName(window) == "KeyhacWindowClass" and getText(window) != "Keyhac":
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
        self_insert_command("S-Enter")()
        if fakeymacs.is_emacs_target_in_previous_window:
            keymap.delayedCall(yank, 200)

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

    ## Esc キーの設定
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

    # クリップボードリストを利用するための設定です。クリップボードリストは fc.clipboardList_key 変数で
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
        ["Edit   config.py",          keymap.command_EditConfig],
        ["Edit   config_personal.py", editConfigPersonal],
        ["Reload config file",        lambda: reloadConfig(0)],
    ]
    if os_keyboard_type == "JP":
        fc.other_items += [
            ["Reload config file (to  US layout)", lambda: reloadConfig(1)],
            ["Reload config file (to JIS layout)", lambda: reloadConfig(2)],
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
        def _lw_lancherList():

            # 既にリストが開いていたら閉じるだけ
            if keymap.isListWindowOpened():
                keymap.cancelListWindow()
                return

            # ウィンドウ
            window_list = getWindowList()
            window_items = []
            if window_list:
                process_name_length = max(map(len, map(Window.getProcessName, window_list)))

                formatter = f"{{0:{process_name_length}}} |{{1:1}}| {{2}}"
                for window in window_list:
                    icon  = "m" if window.isMinimized() else ""
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
        keymap.delayedCall(_lw_lancherList, 0)

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
    ## 後処理
    ####################################################################################################

    # キーマップの優先順位を調整する
    keymap.window_keymap_list.remove(keymap_global)
    keymap.window_keymap_list.remove(keymap_tsw)
    keymap.window_keymap_list.remove(keymap_lw)
    keymap.window_keymap_list.append(keymap_global)
    keymap.window_keymap_list.append(keymap_tsw)
    keymap.window_keymap_list.append(keymap_lw)

    # 個人設定ファイルのセクション [section-extension-space_fn] を読み込んで実行する
    exec(readConfigPersonal("[section-extension-space_fn]"), dict(globals(), **locals()))

    # 個人設定ファイルのセクション [section-extension-capslock_key] を読み込んで実行する
    exec(readConfigPersonal("[section-extension-capslock_key]"), dict(globals(), **locals()))
