# -*- mode: python; coding: utf-8-with-signature-dos -*-

##                               nickname: Fakeymacs
##
## Windows の操作を Emacs のキーバインドで行うための設定（Keyhac版）
##

fakeymacs_version = "20211108_01"

# このスクリプトは、Keyhac for Windows ver 1.82 以降で動作します。
#   https://sites.google.com/site/craftware/keyhac-ja
# スクリプトですので、使いやすいようにカスタマイズしてご利用ください。
#
# この内容は、utf-8-with-signature-dos の coding-system で config.py の名前でセーブして
# 利用してください。
#
# 本設定を利用するための仕様は、以下を参照してください。
#
# ＜共通の仕様＞
# ・emacs_target_class 変数、not_emacs_target 変数、ime_target 変数で、Emacsキーバインドや
#   IME の切り替えキーバインドの対象とするアプリケーションソフトやウィンドウを指定できる。
# ・skip_settings_key 変数で、キーマップ毎にキー設定をスキップするキーを指定できる。
# ・emacs_exclusion_key 変数で、Emacs キーバインドから除外するキーを指定できる。
# ・not_clipboard_target 変数、not_clipboard_target_class 変数で、clipboard 監視の対象外と
#   するアプリケーションソフトやウィンドウを指定できる。
# ・左右どちらの Ctrlキーを使うかを side_of_ctrl_key 変数で指定できる。
# ・左右どちらの Altキーを使うかを side_of_alt_key 変数で指定できる。
# ・左右どちらの Winキーを使うかを side_of_win_key 変数で指定できる。
# ・キーバインドの定義では次の表記が利用できる。
#   ・S-    : Shiftキー
#   ・C-    : Ctrlキー
#   ・A-    : Altキー
#   ・M-    : Altキー と Esc、C-[ のプレフィックスキーを利用する３パターンを定義
#             （Emacsキーバインド設定で利用可。emacs の Meta と同様の意味。）
#   ・Ctl-x : ctl_x_prefix_key 変数で定義されているプレフィックスキーに置換え
#             （Emacsキーバインド設定で利用可。変数の意味は以下を参照のこと。）
#   ・(999) : 仮想キーコード指定
#
# ＜Emacsキーバインド設定と IME の切り替え設定を有効にしたアプリケーションソフトでの動き＞
# ・toggle_input_method_key 変数と set_input_method_key 変数の設定により、IME を切り替える
#   キーを指定できる。
# ・use_emacs_ime_mode 変数の設定により、Emacs日本語入力モードを使うかどうかを指定
#   できる。Emacs日本語入力モードは、IME が ON の時に文字（英数字か、スペースを除く
#   特殊文字）を入力すると起動する。
#   Emacs日本語入力モードでは、次のキーのみが Emacsキーバインドとして利用でき、
#   その他のキーは emacs_ime_mode_key 変数に設定したキーにより置き換えがされた後、
#   Windows にそのまま渡されるようになる。
#   ・Emacs日本語入力モードで使える Emacsキーバインドキー
#     ・C-[
#     ・C-b、C-f
#     ・C-p、C-n
#     ・C-a、C-e
#     ・C-h
#     ・C-d
#     ・C-m
#     ・C-g
#     ・scroll_key 変数で指定したスクロールキー
#   Emacs日本語入力モードは、次の操作で終了する。
#   ・Enter、C-m または C-g が押された場合
#   ・<半角／全角> キー、A-` キーが押された場合
#   ・BS、C-h 押下直後に toggle_input_method_key 変数や set_input_method_key 変数の
#     disable で指定したキーが押された場合
#     （間違って日本語入力をしてしまった時のキー操作を想定しての対策）
# ・Emacs日本語入力モードの使用を有効にした際、emacs_ime_mode_balloon_message 変数の
#   設定でバルーンメッセージとして表示する文字列を指定できる。
# ・use_ime_status_balloon 変数の設定により、IME の状態を表示するバルーンメッセージを
#   表示するかどうかを指定できる。
# ・ime_status_balloon_message 変数の設定により、IME の状態を表示するバルーンメッセージ
#   の組み合わせ（英数入力、日本語入力）を指定できる。
#
# ＜Emacsキーバインド設定を有効にしたアプリケーションソフトでの動き＞
# ・use_ctrl_i_as_tab 変数の設定により、C-iキーを Tabキーとして使うかどうかを指定できる。
# ・use_esc_as_meta 変数の設定より、Escキーを Metaキーとして使うかどうかを指定できる。
#   use_esc_as_meta 変数が True（Metaキーとして使う）に設定されている場合、ESC の
#   二回押下で ESC が入力される。
# ・ctl_x_prefix_key 変数の設定により、Ctl-xプレフィックスキーに使うキーを指定できる。
# ・scroll_key 変数の設定により、スクロールに使うキーを指定できる。scroll_key 変数を
#   None に設定するなどして C-v の指定を外すと、C-v が Windows の 「ペースト」として
#   機能するようになる。
# ・C-c、C-z は、Windows の「コピー」、「取り消し」が機能するようにしている。
#   ctl_x_prefix_key 変数が C-x 以外に設定されている場合には、C-x が Windows の
#   「カット」として機能するようにしている。
# ・C-k を連続して実行しても、クリップボードへの削除文字列の蓄積は行われない。
#   複数行を一括してクリップボードに入れたい場合は、削除の範囲をマークして削除するか
#   前置引数を指定して削除する。
# ・C-y を前置引数を指定して実行すると、ヤンク（ペースト）の繰り返しが行われる。
# ・C-l は、アプリケーションソフト個別対応とする。recenter 関数で個別に指定すること。
#   この設定では、Sakura Editor のみ対応している。
# ・キーボードマクロの再生時に IME の状態に依存した動作とならないようにするため、
#   キーボードマクロの記録と再生の開始時に IME を強制的に OFF にするようにしている。
# ・kill-buffer に Ctl-x k とは別に M-k も割り当てている。プラウザのタブを削除する際
#   などに利用可。
# ・use_ctrl_digit_key_for_digit_argument 変数の設定により、数引数の指定に Ctrl+数字
#   キーを使うかを指定できる。
# ・reconversion_key 変数の設定により、IME の「再変換」を行うキーを指定できる。
#
# ＜全てのアプリケーションソフトで共通の動き＞
# ・toggle_emacs_keybind_key 変数の設定により、emacs キーバインドを利用する設定をした
#   アプリケーションソフトの Emacs キーバインドの利用を切り替えることができる。
# ・application_key 変数の設定により、アプリケーションキーとして利用するキーを指定できる。
# ・use_alt_digit_key_for_f1_to_f12 変数の設定により、F1 から F12 を Alt+数字キー列として
#   使うかを指定できる。
# ・use_alt_shift_digit_key_for_f13_to_f24 変数の設定により、F13 から F24 を Alt+Shift+数字
#   キー列として使うかを指定できる。
# ・other_window_key 変数に設定したキーにより、表示しているウィンドウの中で、一番最近
#   までフォーカスがあったウィンドウに移動する。NTEmacs の機能やランチャーの機能から
#   Windows アプリケーションソフトを起動した際に、起動元のアプリケーションソフトに戻る
#   のに便利。この機能は Ctl-x o にも割り当てているが、こちらは Emacs のキーバインドを
#   適用したアプリケーションソフトのみで有効となる。
# ・window_switching_key 変数に設定したキーにより、アクティブウィンドウの切り替えが行われる。
# ・マルチディスプレイを利用している際に、window_movement_key_for_displays 変数に設定した
#   キーにより、アクティブウィンドウのディスプレイ間の移動が行われる。
# ・window_minimize_key 変数に設定したキーにより、ウィンドウの最小化、リストアが行われる。
# ・desktop_switching_key 変数に設定したキーにより、仮想デスクトップの切り替えが行われる。
#   （仮想デスクトップの利用については、次のページを参照ください。
#     ・http://pc-karuma.net/windows-10-virtual-desktops/
#     ・http://pc-karuma.net/windows-10-virtual-desktop-show-all-window-app/
#     仮想デスクトップ切替時のアニメーションを止める方法は次のページを参照ください。
#     ・http://www.jw7.org/2015/11/03/windows10_virtualdesktop_animation_off/ ）
# ・window_movement_key_for_desktops 変数に設定したキーにより、アクティブウィンドウの
#   仮想デスクトップ間の移動が行われる。
#   （本機能を利用する場合は、Microsoft Store から SylphyHorn をインストールしてください。）
# ・word_register_key 変数に設定したキーにより、IME の「単語登録」プログラムの起動が
#   行われる。
# ・clipboardList_key 変数に設定したキーにより、クリップボードリストが起動する。
#   （C-f、C-b でリストの変更、C-n、C-p でリスト内を移動し、Enter で確定する。
#     C-s、C-r で検索も可能。migemo 辞書を登録してあれば、検索文字を大文字で始める
#     ことで migemo 検索も可能。Emacsキーバインドを適用しないアプリケーションソフト
#     でもクリップボードリストは起動し、選択した項目を Enter で確定することで、
#     クリップボードへの格納（テキストの貼り付けではない）が行われる。）
# ・lancherList_key 変数に設定したキーにより、ランチャーリストが起動する。
#   （全てのアプリケーションソフトで利用可能。操作方法は、クリップボードリストと同じ。）
# ・クリップボードリストやランチャーリストのリストボックス内では、基本、Altキーを
#   Ctrlキーと同じキーとして扱っている。（C-v と A-v の置き換えのみ行っていない。）

import time
import sys
import os.path
import re
import fnmatch
import copy
import types
import datetime
import ctypes

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

    # OS に設定しているキーボードタイプが日本語キーボードかどうかを設定する（自動設定）
    # （True: 日本語キーボード、False: 英語キーボード）
    # （http://tokovalue.jp/function/GetKeyboardType.htm）
    if ctypes.windll.user32.GetKeyboardType(0) == 7:
        is_japanese_keyboard = True
    else:
        is_japanese_keyboard = False

    try:
        with open(dataPath() + r"\config_personal.py", "r", encoding="utf-8-sig") as f:
            config_personal = f.read()
    except:
        print("個人設定ファイル config_personal.py は存在しないため、読み込みしていません")
        config_personal = ""

    def readConfigPersonal(section):
        if config_personal:
            m = re.match(r".*(#\s{}.*?((?=#\s\[section-)|$)).*".format(re.escape(section)), config_personal,
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
    fc.ime = "old_Microsoft_IME"
    # fc.ime = "new_Microsoft_IME"
    # fc.ime = "Google_IME"
    # fc.ime = None

    # Chromium 系ブラウザで発生する問題の対策を行うかどうかを指定する（True: 対策する、False: 対策しない）
    # （Chromium 系ブラウザのバージョン 92 では、アドレスバーにカーソルを移動した際、強制的に ASCII入力
    #   モードに移行する不具合が発生します。（バージョン 93 で対策済みですが、過去にも度々発生しています）
    #   （https://did2memo.net/2021/07/22/chrome-japanese-ime-off-issue-chrome-92/）
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
    ## カスタマイズパラメータの設定
    ###########################################################################

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
                               "mstsc.exe",              # Remote Desktop
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
                               "VirtualBox.exe",         # VirtualBox
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
    fc.reconversion_key = []
    fc.reconversion_key += ["C-t"]
    # fc.reconversion_key += ["(28)"]   # <変換> キーを利用する場合でも、本機能を全て使うためには設定が必要
    # fc.reconversion_key += ["O-RAlt"] # ワンショットモディファイアの指定も可能

    ## IME に設定してある「再変換」、「確定取り消し」を行うキーを指定する

    ## Windows 10 1909 以前の Microsoft IME の場合
    ## （Windows 10 1909 以前の Microsoft IME の場合、C-t を押下して確定の取り消しの状態に入った後、
    ##   Ctrl キーを押したままで C-n による選択メニューの移動を行おうとすると正常に動作しません。
    ##   一度 Ctrl キーを離す、メニューの移動に Space キーを利用する、ime_cancel_key に "W-Slash" を
    ##   設定して「再変換」の機能として利用するなど、いくつかの回避方法があります。お試しください。）
    if fc.ime == "old_Microsoft_IME":
        fc.ime_reconv_key = "W-Slash" # 「再変換」キー
        fc.ime_cancel_key = "C-Back"  # 「確定の取り消し」キー
        fc.ime_reconv_region = False  # 「再変換」の時にリージョンの選択が必要かどうかを指定する
        fc.ime_reconv_space  = False  # リージョンを選択した状態で Space キーを押下した際、「再変換」が働くか
                                      # どうかを指定する

    ## Windows 10 2004 以降の 新しい Microsoft IME の場合
    ## （新しい Microsoft IME には確定取り消し（C-Backspace）の設定が無いようなので、「再変換」のキー
    ##   を設定しています）
    elif fc.ime == "new_Microsoft_IME":
        fc.ime_reconv_key = "W-Slash" # 「再変換」キー
        fc.ime_cancel_key = "W-Slash" # 「確定の取り消し」キー
        fc.ime_reconv_region = False  # 「再変換」の時にリージョンの選択が必要かどうかを指定する
        fc.ime_reconv_space  = True   # リージョンを選択した状態で Space キーを押下した際、「再変換」が働くか
                                      # どうかを指定する

    ## Google日本語入力の場合
    elif fc.ime == "Google_IME":
        fc.ime_reconv_key = "W-Slash" # 「再変換」キー
        fc.ime_cancel_key = "C-Back"  # 「確定の取り消し」キー
        fc.ime_reconv_region = True   # 「再変換」の時にリージョンの選択が必要かどうかを指定する
        fc.ime_reconv_space  = False  # リージョンを選択した状態で Space キーを押下した際、「再変換」が働くか
                                      # どうかを指定する

    ## 上記以外の場合の場合（機能を無効にする）
    else:
        fc.reconversion_key = []
        fc.ime_reconv_key = None
        fc.ime_cancel_key = None
        fc.ime_reconv_region = False
        fc.ime_reconv_space  = False
    #---------------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------------------------
    # Emacs日本語入力モードを利用する際に、IME のショートカットを置き換えるキーの組み合わせ
    # （置き換え先、置き換え元）を指定する
    # （Microsoft IME で「ことえり」のキーバインドを利用するための設定例です。Google日本語入力で
    #   「ことえり」のキー設定になっている場合には不要ですが、設定を行っていても問題はありません。）
    fc.emacs_ime_mode_key = []
    fc.emacs_ime_mode_key += [["C-i", "S-Left"],      # 文節を縮める
                              ["C-o", "S-Right"],     # 文節を伸ばす
                              ["C-j", "F6"],          # ひらがなに変換
                              ["C-k", "F7"],          # 全角カタカナに変換
                              ["C-l", "F9"],          # 全角英数に表示切替
                              ["C-Semicolon", "F8"]]  # 半角に変換

    if is_japanese_keyboard:
        fc.emacs_ime_mode_key += [["C-Colon", "F10"]] # 半角英数に表示切替
    else:
        fc.emacs_ime_mode_key += [["C-Quote", "F10"]] # 半角英数に表示切替
    #---------------------------------------------------------------------------------------------------

    #---------------------------------------------------------------------------------------------------
    # IME の「単語登録」プログラムを利用するための設定を行う

    ## IME の「単語登録」プログラムを起動するキーを指定する
    # fc.word_register_key = None
    fc.word_register_key = "C-CloseBracket"

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
    # （emacs_target_class 変数に指定したクラス（初期値：Edit）に該当するアプリケーションソフト（NotePad
    #   など）は、Emacs キーバインドを切り替えの対象となりません（常に Emacs キーバインドとなります）。）
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
    # （内部で A-Tab による切り替えを行っているため、設定するキーは Altキーとの組み合わせとしてください）
    # （切り替え画面が起動した後は、A-b、A-f、A-p、A-n でウィンドウを切り替えられるように設定している他、
    #   Alt + 矢印キーでもウィンドウを切り替えることができます。また、A-g もしくは A-Esc で切り替え画面の
    #   終了（キャンセル）となり、Altキーを離すか A-Enter で切り替えるウィンドウの確定となります。）
    # （デフォルトキーは、["A-S-Tab", "A-Tab"]）
    fc.window_switching_key = []
    # fc.window_switching_key += [["A-p", "A-n"]]

    # アクティブウィンドウをディスプレイ間で移動するキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （デフォルトキーは、["W-S-Left", "W-S-Right"]）
    fc.window_movement_key_for_displays = []
    fc.window_movement_key_for_displays += [[None, "W-o"]]

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
    # （本機能を利用する場合は、Microsoft Store から SylphyHorn をインストールしてください。
    #   Windows 10 では動作を確認しておりますが、Windows 11 では正常に動作しないようです。）
    # （デフォルトキーは、["W-C-A-Left", "W-C-A-Right"] です。この設定は変更しないでください）
    # （仮想デスクトップ切り替え時の通知を ON にすると処理が重くなります。代わりに、トレイアイコンに
    #   デスクトップ番号を表示する機能を ON にすると良いようです。）
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

    # 個人設定ファイルのセクション [section-base-1] を読み込んで実行する
    exec(readConfigPersonal("[section-base-1]"), dict(globals(), **locals()))


    ###########################################################################
    ## 基本機能の設定
    ###########################################################################

    fakeymacs.not_emacs_keybind = []
    fakeymacs.ime_cancel = False
    fakeymacs.last_window = None
    fakeymacs.clipboard_hook = True
    fakeymacs.last_keys = [None, None]
    fakeymacs.correct_ime_status = False

    def is_emacs_target(window):
        last_window  = fakeymacs.last_window
        process_name = window.getProcessName()
        class_name   = window.getClassName()

        if window != last_window:
            if (process_name in fc.not_clipboard_target or
                any([checkWindow(None, c, None, window) for c in fc.not_clipboard_target_class])):
                # クリップボードの監視用のフックを無効にする
                keymap.clipboard_history.enableHook(False)
                fakeymacs.clipboard_hook = False
            else:
                # クリップボードの監視用のフックを有効にする
                keymap.clipboard_history.enableHook(True)
                fakeymacs.clipboard_hook = True

            if process_name in fc.emacs_exclusion_key:
                fakeymacs.exclution_key = [str(keyhac_keymap.KeyCondition.fromString(addSideOfModifierKey(key)))
                                           for key in fc.emacs_exclusion_key[process_name]]
            else:
                fakeymacs.exclution_key = []

            if fc.correct_ime_status:
                if fc.ime == "Google_IME":
                    if window.getProcessName() in fc.chromium_browser_list:
                        fakeymacs.correct_ime_status = True
                    else:
                        fakeymacs.correct_ime_status = False

            reset_undo(reset_counter(reset_mark(lambda: None)))()
            fakeymacs.ime_cancel = False
            fakeymacs.last_window = window

        if is_task_switching_window(window):
            return False

        if is_list_window(window):
            return False

        if (class_name not in fc.emacs_target_class and
            (process_name in fakeymacs.not_emacs_keybind or
             process_name in fc.not_emacs_target)):
            fakeymacs.keybind = "not_emacs"
            return False
        else:
            if window != last_window:
                popImeBalloon()
            fakeymacs.keybind = "emacs"
            return True

    def is_ime_target(window):
        if (window.getClassName() not in fc.emacs_target_class and
            (window.getProcessName() in fakeymacs.not_emacs_keybind or
             window.getProcessName() in fc.ime_target)):
            return True
        else:
            return False

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

    # Ctl-xプレフィックスキーを構成するキーの仮想キーコードを設定する
    if fc.ctl_x_prefix_key:
        keyCondition = keyhac_keymap.KeyCondition.fromString(fc.ctl_x_prefix_key)

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
        setImeStatus(1)

    def disable_input_method():
        setImeStatus(0)

    def toggle_input_method():
        setImeStatus(keymap.getWindow().getImeStatus() ^ 1)

    def setImeStatus(ime_status):
        correctImeStatus()

        if keymap.getWindow().getImeStatus() != ime_status:
            # IME を切り替える
            # （keymap.getWindow().setImeStatus(ime_status) を使わないのは、キーボードマクロの再生時に
            #   影響がでるため）
            self_insert_command("A-(25)")()

            if fakeymacs.is_playing_kmacro:
                delay(0.2)

        popImeBalloon(ime_status)

    def correctImeStatus():
        # Chromium 系ブラウザで発生する問題の対策を行う
        if fakeymacs.correct_ime_status:
            if keymap.getWindow().getImeStatus():
                keymap.getWindow().setImeStatus(0) # この行は必要
                keymap.getWindow().setImeStatus(1)

    def popImeBalloon(ime_status=None, force=False):
        if not fakeymacs.is_playing_kmacro:
            if force or fc.use_ime_status_balloon:
                # LINE アプリなど、Qt5152QWindowIcon にマッチするクラスをもつアプリは入力文字に
                # バルーンヘルプが被るので、バルーンヘルプの表示対象から外す
                # （ただし、force が True の場合は除く）
                if force or not checkWindow(None, "Qt5152QWindowIcon"):
                    if ime_status is None:
                        ime_status = keymap.getWindow().getImeStatus()

                    if ime_status:
                        message = fc.ime_status_balloon_message[1]
                    else:
                        message = fc.ime_status_balloon_message[0]

                    try:
                        # IME の状態をバルーンヘルプで表示する
                        keymap.popBalloon("ime_status", message, 500)
                    except:
                        pass

    def reconversion(reconv_key, cancel_key):
        def _func():
            if fakeymacs.ime_cancel:
                self_insert_command(cancel_key)()
                if fc.use_emacs_ime_mode:
                    enable_emacs_ime_mode(100)
            else:
                if fc.ime_reconv_region:
                    if fakeymacs.forward_direction is not None:
                        self_insert_command(reconv_key)()
                        if fc.use_emacs_ime_mode:
                            enable_emacs_ime_mode()
                else:
                    self_insert_command(reconv_key)()
                    if fc.use_emacs_ime_mode:
                        enable_emacs_ime_mode()
        return _func

    ##################################################
    ## ファイル操作
    ##################################################

    def find_file():
        self_insert_command("C-o")()

    def save_buffer():
        self_insert_command("C-s")()

    def write_file():
        self_insert_command("A-f", "A-a")()

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
            for i in range(repeat):
                backward_word()

        mark(move_beginning_of_region, False)()
        delay()
        kill_region()

    def kill_word(repeat=1):
        resetRegion()
        fakeymacs.is_marked = True

        def move_end_of_region():
            for i in range(repeat):
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
                    for i in range(repeat):
                        next_line()
                    move_beginning_of_line()
                else:
                    for i in range(repeat - 1):
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
                for i in range(len(getClipboardText())):
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
        if checkWindow("notepad.exe", "Edit"): # NotePad
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
    ## バッファ / ウィンドウ操作
    ##################################################

    def kill_buffer():
        self_insert_command("C-F4")()

    def switch_to_buffer():
        self_insert_command("C-Tab")()

    def other_window():
        window_list = getWindowList()
        try:
            for wnd in window_list[1:]:
                if not wnd.isMinimized():
                    wnd.getLastActivePopup().setForeground()
                    break
        except:
            pass

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
        keymap.getWindow().setImeStatus(0)
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
            keymap.getWindow().setImeStatus(0)
            keymap.command_RecordPlay()
            fakeymacs.is_playing_kmacro = False

        keymap.delayedCall(callKmacro, 0)

    ##################################################
    ## その他
    ##################################################

    def space():
        self_insert_command("Space")()
        if fc.use_emacs_ime_mode:
            if fc.ime_reconv_space:
                if keymap.getWindow().getImeStatus():
                    if fakeymacs.forward_direction is not None:
                        enable_emacs_ime_mode()

    def newline():
        self_insert_command("Enter")()
        if not fc.use_emacs_ime_mode:
            if keymap.getWindow().getImeStatus():
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
                    checkWindow("EXCEL.EXE", "EXCEL*") or                  # Microsoft Excel
                    checkWindow("Evernote.exe", "WebViewHost")):           # Evernote
                self_insert_command("Esc")()

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
        def popCommandWindow(wnd, command):
            if wnd.isVisible() and not wnd.getOwner() and wnd.getProcessName() == command:
                popWindow(wnd)()
                fakeymacs.is_executing_command = True
                return False
            return True

        fakeymacs.is_executing_command = False
        Window.enum(popCommandWindow, os.path.basename(fc.command_name))

        if not fakeymacs.is_executing_command:
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

            elif checkWindow("cmd.exe", "ConsoleWindowClass"): # Cmd
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
                (class_name is None or fnmatch.fnmatch(window.getClassName(), class_name)) and
                (text is None or fnmatch.fnmatch(window.getText(), text)))

    def vkeys():
        vkeys = list(keyCondition.vk_str_table)
        for vkey in [VK_MENU, VK_LMENU, VK_RMENU, VK_CONTROL, VK_LCONTROL, VK_RCONTROL, VK_SHIFT, VK_LSHIFT, VK_RSHIFT, VK_LWIN, VK_RWIN]:
            vkeys.remove(vkey)
        return vkeys

    def vkToStr(vkey):
        return keyhac_keymap.KeyCondition.vkToStr(vkey)

    def strToVk(name):
        return keyhac_keymap.KeyCondition.strToVk(name)

    def addSideOfModifierKey(key):
        key = re.sub(r'(^|-)(C-)', r'\1' + fc.side_of_ctrl_key + r'\2', key)
        key = re.sub(r'(^|-)(A-)', r'\1' + fc.side_of_alt_key  + r'\2', key)
        key = re.sub(r'(^|-)(W-)', r'\1' + fc.side_of_win_key  + r'\2', key)
        return key

    def kbd(keys):
        key_lists = []

        if keys:
            key_list0 = []
            key_list1 = []
            key_list2 = []

            for key in keys.split():
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

    def define_key(window_keymap, keys, command, skip_check=True):
        if keys is None:
            return

        if skip_check:
            # local スコープで参照できるようにする
            try:
                keymap_global
                keymap_emacs
                keymap_ime
                keymap_ei
                keymap_tsw
                keymap_lw
            except:
                pass

            # 設定をスキップするキーの処理を行う
            for keymap_name in fc.skip_settings_key:
                if (keymap_name in locals() and
                    window_keymap == locals()[keymap_name]):
                    for skey in fc.skip_settings_key[keymap_name]:
                        if fnmatch.fnmatch(keys, skey):
                            print("skip settings key : [" + keymap_name + "] " + keys)
                            return

        def keyCommand(key):
            # local スコープで参照できるようにする
            try:
                keymap_emacs
            except:
                pass

            if callable(command):
                if (key is not None and
                    "keymap_emacs" in locals() and
                    window_keymap == locals()["keymap_emacs"]):

                    ckey = str(keyhac_keymap.KeyCondition.fromString(key))
                    def _command():
                        fakeymacs.update_last_keys = True
                        if ckey in fakeymacs.exclution_key:
                            keymap.InputKeyCommand(key)()
                        else:
                            command()
                        if fakeymacs.update_last_keys:
                            fakeymacs.last_keys = [window_keymap, keys]
                    return _command
                else:
                    def _command():
                        fakeymacs.update_last_keys = True
                        command()
                        if fakeymacs.update_last_keys:
                            fakeymacs.last_keys = [window_keymap, keys]
                    return _command
            else:
                return command

        for key_list in kbd(keys):
            if len(key_list) == 1:
                window_keymap[key_list[0]] = keyCommand(key_list[0])

                # Alt キーを単押しした際に、カーソルがメニューへ移動しないようにする
                # （https://www.haijin-boys.com/discussions/4583）
                if key_list[0] == "O-LAlt":
                    window_keymap["D-LAlt"] = "D-LAlt", "(7)"

                elif key_list[0] == "O-RAlt":
                    window_keymap["D-RAlt"] = "D-RAlt", "(7)"
            else:
                w_keymap = window_keymap
                for key in key_list[:-1]:
                    w_keymap = w_keymap[key]
                w_keymap[key_list[-1]] = keyCommand(None)

    def define_key2(window_keymap, keys, command):
        define_key(window_keymap, keys, command, skip_check=False)

    def define_key3(window_keymap, keys, command, check_func):
        define_key(window_keymap, keys, makeKeyCommand(window_keymap, keys, command, check_func))

    def mergeMultiStrokeKeymap(window_keymap1, window_keymap2, keys):
        key_list = kbd(keys)[0]
        for key in key_list:
            window_keymap1 = window_keymap1[key]
            window_keymap2 = window_keymap2[key]
        window_keymap1.keymap = {**window_keymap2.keymap, **window_keymap1.keymap}

    def getKeyCommand(window_keymap, keys):
        try:
            key_list = kbd(keys)[-1]
            for key in key_list:
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
                func = keymap.InputKeyCommand(key_list[0])
            else:
                func = lambda: None

        def _func():
            if check_func():
                command()
            else:
                func()
        return _func

    def self_insert_command(*keys):
        func = keymap.InputKeyCommand(*list(map(addSideOfModifierKey, keys)))
        def _func():
            func()
            fakeymacs.ime_cancel = False
        return _func

    def self_insert_command2(*keys):
        func = self_insert_command(*keys)
        def _func():
            correctImeStatus()
            func()
            if fc.use_emacs_ime_mode:
                if keymap.getWindow().getImeStatus():
                    enable_emacs_ime_mode()
        return _func

    def self_insert_command3(*keys):
        func = self_insert_command(*keys)
        def _func():
            func()
            keymap.getWindow().setImeStatus(0)
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

            for i in range(repeat_counter):
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
        imeStatus = keymap.getWindow().getImeStatus()
        if imeStatus:
            keymap.getWindow().setImeStatus(0)
        keymap.InputTextCommand(str)()
        if imeStatus:
            keymap.getWindow().setImeStatus(1)

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
                        define_key2(keymap_emacs, mkey, self_insert_command(mkey))

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
    define_key(keymap_emacs, "C-OpenBracket C-OpenBracket", reset_undo(reset_counter(self_insert_command("Esc"))))
    if fc.use_esc_as_meta:
        define_key(keymap_emacs, "Esc Esc", reset_undo(reset_counter(self_insert_command("Esc"))))
    else:
        define_key(keymap_emacs, "Esc", reset_undo(reset_counter(self_insert_command("Esc"))))

    ## universal-argumentキーの設定
    define_key(keymap_emacs, "C-u", universal_argument)

    ## 「IME の切り替え」のキー設定
    define_key(keymap_emacs, "(243)",  toggle_input_method)
    define_key(keymap_emacs, "(244)",  toggle_input_method)
    define_key(keymap_emacs, "A-(25)", toggle_input_method)

    define_key(keymap_ime,   "(243)",  toggle_input_method)
    define_key(keymap_ime,   "(244)",  toggle_input_method)
    define_key(keymap_ime,   "A-(25)", toggle_input_method)

    ## 「ファイル操作」のキー設定
    define_key(keymap_emacs, "Ctl-x C-f", reset_search(reset_undo(reset_counter(reset_mark(find_file)))))
    define_key(keymap_emacs, "Ctl-x C-s", reset_search(reset_undo(reset_counter(reset_mark(save_buffer)))))
    define_key(keymap_emacs, "Ctl-x C-w", reset_search(reset_undo(reset_counter(reset_mark(write_file)))))
    define_key(keymap_emacs, "Ctl-x d",   reset_search(reset_undo(reset_counter(reset_mark(dired)))))

    ## 「カーソル移動」のキー設定
    define_key(keymap_emacs, "C-b",        reset_search(reset_undo(reset_counter(mark(repeat(backward_char), False)))))
    define_key(keymap_emacs, "C-f",        reset_search(reset_undo(reset_counter(mark(repeat(forward_char), True)))))
    define_key(keymap_emacs, "M-b",        reset_search(reset_undo(reset_counter(mark(repeat(backward_word), False)))))
    define_key(keymap_emacs, "M-f",        reset_search(reset_undo(reset_counter(mark(repeat(forward_word), True)))))
    define_key(keymap_emacs, "C-p",        reset_search(reset_undo(reset_counter(mark(repeat(previous_line), False)))))
    define_key(keymap_emacs, "C-n",        reset_search(reset_undo(reset_counter(mark(repeat(next_line), True)))))
    define_key(keymap_emacs, "C-a",        reset_search(reset_undo(reset_counter(mark(move_beginning_of_line, False)))))
    define_key(keymap_emacs, "C-e",        reset_search(reset_undo(reset_counter(mark(move_end_of_line, True)))))
    define_key(keymap_emacs, "M-S-Comma",  reset_search(reset_undo(reset_counter(mark(beginning_of_buffer, False)))))
    define_key(keymap_emacs, "M-S-Period", reset_search(reset_undo(reset_counter(mark(end_of_buffer, True)))))
    define_key(keymap_emacs, "M-g g",      reset_search(reset_undo(reset_counter(reset_mark(goto_line)))))
    define_key(keymap_emacs, "M-g M-g",    reset_search(reset_undo(reset_counter(reset_mark(goto_line)))))
    define_key(keymap_emacs, "C-l",        reset_search(reset_undo(reset_counter(recenter))))

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
    define_key(keymap_emacs, "C-Slash",  reset_search(reset_counter(reset_mark(undo))))
    define_key(keymap_emacs, "Ctl-x u",  reset_search(reset_counter(reset_mark(undo))))

    define_key(keymap_emacs, "Back",     reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_backward_char))))))
    define_key(keymap_emacs, "Delete",   reset_search(reset_undo(reset_counter(reset_mark(repeat2(delete_char))))))
    define_key(keymap_emacs, "C-Back",   reset_search(reset_undo(reset_counter(reset_mark(repeat3(backward_kill_word))))))
    define_key(keymap_emacs, "C-Delete", reset_search(reset_undo(reset_counter(reset_mark(repeat3(kill_word))))))
    define_key(keymap_emacs, "C-c",      reset_search(reset_undo(reset_counter(reset_mark(kill_ring_save)))))
    define_key(keymap_emacs, "C-v",      reset_search(reset_undo(reset_counter(reset_mark(repeat(yank)))))) # scroll_key の設定で上書きされない場合
    define_key(keymap_emacs, "C-z",      reset_search(reset_counter(reset_mark(undo))))

    # C-Underscore を機能させるための設定
    if is_japanese_keyboard:
        define_key(keymap_emacs, "C-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(undo)))))
    else:
        define_key(keymap_emacs, "C-S-Minus", reset_search(reset_undo(reset_counter(reset_mark(undo)))))

    # C-Atmark を機能させるための設定
    if is_japanese_keyboard:
        define_key(keymap_emacs, "C-Atmark", reset_search(reset_undo(reset_counter(set_mark_command))))
    else:
        define_key(keymap_emacs, "C-S-2", reset_search(reset_undo(reset_counter(set_mark_command))))

    define_key(keymap_emacs, "C-Space",   reset_search(reset_undo(reset_counter(set_mark_command))))
    define_key(keymap_emacs, "Ctl-x h",   reset_search(reset_undo(reset_counter(mark_whole_buffer))))
    define_key(keymap_emacs, "Ctl-x C-p", reset_search(reset_undo(reset_counter(mark_page))))

    ## 「バッファ / ウィンドウ操作」のキー設定
    define_key(keymap_emacs, "M-k",     reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
    define_key(keymap_emacs, "Ctl-x k", reset_search(reset_undo(reset_counter(reset_mark(kill_buffer)))))
    define_key(keymap_emacs, "Ctl-x b", reset_search(reset_undo(reset_counter(reset_mark(switch_to_buffer)))))
    define_key(keymap_emacs, "Ctl-x o", reset_search(reset_undo(reset_counter(reset_mark(other_window)))))

    ## 「文字列検索 / 置換」のキー設定
    define_key(keymap_emacs, "C-r",   reset_undo(reset_counter(reset_mark(isearch_backward))))
    define_key(keymap_emacs, "C-s",   reset_undo(reset_counter(reset_mark(isearch_forward))))
    define_key(keymap_emacs, "M-S-5", reset_search(reset_undo(reset_counter(reset_mark(query_replace)))))

    ## 「キーボードマクロ」のキー設定
    if is_japanese_keyboard:
        define_key(keymap_emacs, "Ctl-x S-8", kmacro_start_macro)
        define_key(keymap_emacs, "Ctl-x S-9", kmacro_end_macro)
    else:
        define_key(keymap_emacs, "Ctl-x S-9", kmacro_start_macro)
        define_key(keymap_emacs, "Ctl-x S-0", kmacro_end_macro)

    define_key(keymap_emacs, "Ctl-x e", reset_search(reset_undo(reset_counter(repeat(kmacro_end_and_call_macro)))))

    ## 「その他」のキー設定
    define_key(keymap_emacs, "Enter",     reset_undo(reset_counter(reset_mark(repeat(newline)))))
    define_key(keymap_emacs, "C-m",       reset_undo(reset_counter(reset_mark(repeat(newline)))))
    define_key(keymap_emacs, "C-j",       reset_undo(reset_counter(reset_mark(newline_and_indent))))
    define_key(keymap_emacs, "C-o",       reset_undo(reset_counter(reset_mark(repeat(open_line)))))
    define_key(keymap_emacs, "Tab",       reset_undo(reset_counter(reset_mark(repeat(indent_for_tab_command)))))
    define_key(keymap_emacs, "C-g",       reset_search(reset_counter(reset_mark(keyboard_quit))))
    define_key(keymap_emacs, "Ctl-x C-c", reset_search(reset_undo(reset_counter(reset_mark(kill_emacs)))))
    define_key(keymap_emacs, "M-S-1",     reset_search(reset_undo(reset_counter(reset_mark(shell_command)))))

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
            try:
                del keymap_emacs[addSideOfModifierKey(fc.ime_cancel_key)]
            except:
                pass

        for key in fc.reconversion_key:
            define_key(keymap_emacs, key, reset_undo(reset_counter(reset_mark(reconversion(fc.ime_reconv_key, fc.ime_cancel_key)))))


    ###########################################################################
    ## Emacs日本語入力モードの設定
    ###########################################################################
    if fc.use_emacs_ime_mode:

        def is_emacs_ime_mode(window):
            if fakeymacs.ei_last_window == window:
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
                if (fakeymacs.last_keys[0] == keymap_ei and
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
                if (fakeymacs.last_keys[0] == keymap_ei and
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
            self_insert_command("Esc")()

        def ei_newline():
            self_insert_command("Enter")()
            fakeymacs.ime_cancel = True
            disable_emacs_ime_mode()

        def ei_keyboard_quit():
            self_insert_command("Esc")()
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

        ## 全てのキーパターンの設定（キーの入力記録を残すための設定）
        for vkey in vkeys():
            key = vkToStr(vkey)
            for mod1 in ["", "A-"]:
                for mod2 in ["", "C-"]:
                    for mod3 in ["", "S-"]:
                        mkey = mod1 + mod2 + mod3 + key
                        define_key2(keymap_ei, mkey, self_insert_command(mkey))

        ## 「IME の切り替え」のキー設定
        define_key(keymap_ei, "(243)",  ei_disable_input_method)
        define_key(keymap_ei, "(244)",  ei_disable_input_method)
        define_key(keymap_ei, "A-(25)", ei_disable_input_method)

        ## Escキーの設定
        define_key(keymap_ei, "Esc",           ei_esc)
        define_key(keymap_ei, "C-OpenBracket", ei_esc)

        ## 「カーソル移動」のキー設定
        define_key(keymap_ei, "C-b", backward_char)
        define_key(keymap_ei, "C-f", forward_char)
        define_key(keymap_ei, "C-p", previous_line)
        define_key(keymap_ei, "C-n", next_line)
        define_key(keymap_ei, "C-a", move_beginning_of_line)
        define_key(keymap_ei, "C-e", move_end_of_line)

        ## 「カット / コピー / 削除 / アンドゥ」のキー設定
        define_key(keymap_ei, "C-h", delete_backward_char)
        define_key(keymap_ei, "C-d", delete_char)

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
            define_key(keymap_ei, disable_key, ei_disable_input_method2(keymap_ei_dup, disable_key))
            define_key(keymap_ei, enable_key,  ei_enable_input_method2(keymap_ei_dup, enable_key))


    ###########################################################################
    ## Emacs キーバインドの切り替えのキー設定
    ###########################################################################

    keymap_global = keymap.defineWindowKeymap()

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

        define_key(keymap_global, "A-Minus", self_insert_command(vkToStr(VK_F11)))

        if is_japanese_keyboard:
            define_key(keymap_global, "A-Caret", self_insert_command(vkToStr(VK_F12)))
        else:
            define_key(keymap_global, "A-Plus",  self_insert_command(vkToStr(VK_F12)))

    ## Alt+Shift+数字キー列の設定
    if fc.use_alt_shift_digit_key_for_f13_to_f24:
        for i in range(10):
            define_key(keymap_global, "A-S-{}".format((i + 1) % 10), self_insert_command(vkToStr(VK_F13 + i)))

        define_key(keymap_global, "A-S-Minus", self_insert_command(vkToStr(VK_F23)))

        if is_japanese_keyboard:
            define_key(keymap_global, "A-S-Caret", self_insert_command(vkToStr(VK_F24)))
        else:
            define_key(keymap_global, "A-S-Plus",  self_insert_command(vkToStr(VK_F24)))


    ###########################################################################
    ## デスクトップの設定
    ###########################################################################

    ##################################################
    ## ウィンドウ操作（デスクトップ用）
    ##################################################

    def popWindow(wnd):
        def _func():
            try:
                if wnd.isMinimized():
                    wnd.restore()
                delay() # ウィンドウフォーカスが適切に移動しない場合があることの対策
                wnd.getLastActivePopup().setForeground()
            except:
                print("選択したウィンドウは存在しませんでした")
        return _func

    def getWindowList():
        def makeWindowList(wnd, arg):
            if wnd.isVisible() and not wnd.getOwner():

                class_name = wnd.getClassName()
                title = wnd.getText()

                if class_name == "Emacs" or title != "":
                    if not re.match(fc.window_operation_exclusion_class, class_name):
                        process_name = wnd.getProcessName()
                        if not re.match(fc.window_operation_exclusion_process, process_name):
                            # 表示されていないストアアプリ（「設定」等）が window_list に登録されるのを抑制する
                            if class_name == "Windows.UI.Core.CoreWindow":
                                if title in window_dict:
                                    if window_dict[title] in window_list:
                                        window_list.remove(window_dict[title])
                                else:
                                    window_dict[title] = wnd

                            elif class_name == "ApplicationFrameWindow":
                                if title not in window_dict:
                                    window_dict[title] = wnd
                                    window_list.append(wnd)
                            else:
                                window_list.append(wnd)
            return True

        window_dict = {}
        window_list = []
        Window.enum(makeWindowList, None)

        return window_list

    def previous_window():
        self_insert_command("A-S-Tab")()

    def next_window():
        self_insert_command("A-Tab")()

    def move_window_to_previous_display():
        self_insert_command("W-S-Left")()

    def move_window_to_next_display():
        self_insert_command("W-S-Right")()

    def minimize_window():
        wnd = keymap.getTopLevelWindow()
        if wnd and not wnd.isMinimized():
            wnd.minimize()

    def restore_window():
        window_list = getWindowList()

        # ウィンドウのリストアが最小化した順番の逆順にならないときは次の行を無効化
        # （コメント化）してください
        window_list.reverse()

        for wnd in window_list:
            if wnd.isMinimized():
                wnd.restore()
                break

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
    define_key(keymap_tsw, "A-g", self_insert_command("A-Esc"))

    define_key(keymap_tsw, "C-b", backward_char)
    define_key(keymap_tsw, "C-f", forward_char)
    define_key(keymap_tsw, "C-p", previous_line)
    define_key(keymap_tsw, "C-n", next_line)
    define_key(keymap_tsw, "C-g", self_insert_command("Esc"))


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
        self_insert_command("Esc")()

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
    define_key(keymap_lw, "Esc",           lw_reset_search(self_insert_command("Esc")))
    define_key(keymap_lw, "C-OpenBracket", lw_reset_search(self_insert_command("Esc")))

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
        ["MSEdge",      keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "", "")],
        ["Chrome",      keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "", "")],
        ["Firefox",     keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe", "", "")],
        ["Thunderbird", keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Mozilla Thunderbird\thunderbird.exe", "", "")],
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
        ["Reload config.py", keymap.command_ReloadConfig],
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

                formatter = "{0:" + str(process_name_length) + "} | {1}"
                for wnd in window_list:
                    window_items.append([formatter.format(wnd.getProcessName(), wnd.getText()), popWindow(wnd)])

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
