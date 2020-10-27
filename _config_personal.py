# -*- mode: python; coding: utf-8-with-signature-dos -*-

# https://stackoverflow.com/questions/2904274/globals-and-locals-in-python-exec
# https://docs.python.org/3/library/functions.html?highlight=exec%20global#exec

# 本ファイルは、config_personal.py というファイル名にすることで個人設定ファイルとして機能します。
# 本ファイルの設定には [] で括られたセクション名が定義されており、その単位で config.py の中に設定
# が取り込まれ、exec関数により実行されます。config.py ファイル内の exec関数をコールしているところ
# を検索すると、何のセクションがどこで読み込まれるかが分かると思います。

# 本ファイルはサンプルファイルです。本ファイルに記載のない設定でも、config.py から設定を取り込み、
# カスタマイズしてご利用ください。

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

# IMEの設定（３つの設定のいずれか一つを True にする）
fc.use_old_Microsoft_IME = True
fc.use_new_Microsoft_IME = False
fc.use_Google_IME = False

####################################################################################################
## 基本設定
####################################################################################################
# [section-base-1] ---------------------------------------------------------------------------------

# Emacs のキーバインドに“したくない”アプリケーションソフトを指定する
# （Keyhac のメニューから「内部ログ」を ON にすると processname や classname を確認することができます）
fc.not_emacs_target    += [
                          ]

# IME の切り替え“のみをしたい”アプリケーションソフトを指定する
# （指定できるアプリケーションソフトは、not_emacs_target で（除外）指定したものからのみとなります）
fc.ime_target          += [
                          ]

# キーマップ毎にキー設定をスキップするキーを指定する
# （リストに指定するキーは、define_key の第二引数に指定する記法のキーとしてください。"A-v" や "C-v"
#   のような指定の他に、"M-f" や "Ctl-x d" などの指定も可能です。）
# （ここで指定したキーに新たに別のキー設定をしたいときには、「-2」が付くセクション内で define_key2
#   関数を利用して定義してください）
fc.skip_settings_key    = {"keymap_global"    : [],
                           "keymap_emacs"     : [],
                           "keymap_ime"       : [],
                           "keymap_ei"        : [],
                           "keymap_tsw"       : [],
                           "keymap_lw"        : [],
                          }

# Emacs のキーバインドにするアプリケーションソフトで、Emacs キーバインドから除外するキーを指定する
# （リストに指定するキーは、Keyhac で指定可能なマルチストロークではないキーとしてください。
#   Fakeymacs の記法の "M-f" や "Ctl-x d" などの指定はできません。"A-v"、"C-v" などが指定可能です。）
fc.emacs_exclusion_key  = {"chrome.exe"       : ["C-l", "C-t"],
                           "msedge.exe"       : ["C-l", "C-t"],
                           "firefox.exe"      : ["C-l", "C-t"],
                           "Code.exe"         : ["C-S-b", "C-S-f", "C-S-p", "C-S-n", "C-S-a", "C-S-e"],
                          }

# 左右どちらの Ctrlキーを使うかを指定する（"L": 左、"R": 右）
# fc.side_of_ctrl_key = "R"

# Escキーを Metaキーとして使うかどうかを指定する（True: 使う、False: 使わない）
# （True（Metaキーとして使う）に設定されている場合、ESC の二回押下で ESC が入力されます）
# fc.use_esc_as_meta = True

#---------------------------------------------------------------------------------------------------
# IME を切り替えるキーの組み合わせ（disable、enable の順）を指定する（複数指定可）
# （toggle_input_method_key のキー設定より優先します）
fc.set_input_method_key = []

## 日本語キーボードを利用している場合、<無変換> キーで英数入力、<変換> キーで日本語入力となる
fc.set_input_method_key += [["(29)", "(28)"]]

## LAlt の単押しで英数入力、RAlt の単押しで日本語入力となる
## （JetBrains 製の IDE でこの設定を利用するためには、ツールボタンをオンにする必要があるようです。
##   設定は、View -> Appearance -> Tool Window Bars を有効にしてください。）
# fc.set_input_method_key += [["O-LAlt", "O-RAlt"]]

## C-j や C-j C-j で 英数入力となる（toggle_input_method_key の設定と併せ、C-j C-o で日本語入力となる）
# fc.set_input_method_key += [["C-j", None]]

## C-j で英数入力、C-o で日本語入力となる（toggle_input_method_key の設定より優先）
# fc.set_input_method_key += [["C-j", "C-o"]]
#---------------------------------------------------------------------------------------------------

# VSCode の Terminal内 で ４つのキー（Ctrl+k、Ctrl+r、Ctrl+s、Ctrl+y）のダイレクト入力機能を使うか
# どうかを指定する（True: 使う、False: 使わない）
# fc.use_vscode_terminal_key_direct_input = True

# アプリケーションキーとして利用するキーを指定する
# （修飾キーに Alt は使えないようです）
# fc.application_key = "O-RCtrl"
# fc.application_key = "W-m"

# [section-base-2] ---------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# VSCode で Extension のインストールが必要な機能は、個人設定ファイルで設定する

if 0:
    # VSCode に vscode-dired Extension をインストールしてお使いください
    # （Ctrl+x f に設定されているキーバインドは、Ctrl+x（Cut）の機能とバッティングするので、削除して
    #   ください（Open Keyboard Shortcuts コマンドで削除可能です）)

    def dired(func=dired):
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Open dired buffer
            vscodeExecuteCommand("Op-di-bu")
        else:
            func()

    define_key(keymap_emacs, "Ctl-x d", reset_search(reset_undo(reset_counter(reset_mark(dired)))))

if 0:
    # VSCode に Center Editor Window Extension をインストールしてお使いください

    def recenter(func=recenter):
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Center Editor Window
            self_insert_command("C-l")()
        else:
            func()

    define_key(keymap_emacs, "C-l", reset_search(reset_undo(reset_counter(recenter))))

if 0:
    # VSCode に Search in Current File Extension をインストールしてお使いください
    # （アクティビティバーの SEARCH アイコンをパネルのバーにドラッグで持っていくと、検索結果が
    #   パネルに表示されるようになり、使いやすくなります）

    def occur():
        if checkWindow("Code.exe", "Chrome_WidgetWin_1"): # VSCode
            # VSCode Command : Search in Current File
            vscodeExecuteCommand("Se-in-Cu-Fi")

    define_key(keymap_emacs, "Ctl-x C-o", reset_search(reset_undo(reset_counter(reset_mark(occur)))))
#---------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# Everything プログラムを起動するキーを指定する

if 0:
    # Everything を起動するキーを指定する
    everything_key = "C-A-v"

    # Everything プログラムを指定する
    everything_name = r"C:\Program Files\Everything\everything.exe"

    def everything():
        keymap.ShellExecuteCommand(None, everything_name, "", "")()

    define_key(keymap_global, everything_key, everything)
#---------------------------------------------------------------------------------------------------

####################################################################################################
## クリップボードリストの設定
####################################################################################################
# [section-clipboardList-1] ------------------------------------------------------------------------

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

# [section-lancherList-2] --------------------------------------------------------------------------

####################################################################################################
## 拡張機能の設定
####################################################################################################
# [section-extensions] -----------------------------------------------------------------------------

# C-Enter に F2（編集モード移行）を割り当てる
# exec(readConfigExtension("extension-edit_mode.py"), dict(globals(), **locals()))

# Emacs の場合、IME 切り替え用のキーを C-\ に置き換える
# exec(readConfigExtension("extension-real_emacs.py"), dict(globals(), **locals()))

# 英語キーボード設定をした OS 上で、日本語キーボードを利用する場合の切り替えを行う
# exec(readConfigExtension("extension-change_keyboard.py"), dict(globals(), **locals()))
