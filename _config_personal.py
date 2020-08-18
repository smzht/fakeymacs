# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで個人設定用ファイルとして機能します。
# 本ファイルの設定には [] で括られたセクション名が定義されており、その単位で config.py の中に設定が
# 取り込まれ、exec 関数により実行されます。config.py ファイル内の exec 関数をコールしているところを
# 検索すると、何のセクションがどこで読み込まれるかが分かると思います。

# このファイル内で関数を定義した場合、その関数内では上位のローカルスコープで定義している変数や関数
# を利用できません。（python の仕様だと思います。）このため、このファイル内で定義する関数内で上位の
# ローカルスコープの変数や関数を利用したい場合には、引数を使って明示的に引き渡してあげる必要があり
# ます。（emacsclient 関数の実装例を参考としてください。）

# 本ファイルはサンプルファイルです。本ファイルに記載のない設定でも、config.py から設定を取り込み、
# カスタマイズしてご利用ください。

####################################################################################################
## 機能オプションの選択
####################################################################################################
# [section-options] --------------------------------------------------------------------------------

# IMEの設定（３つの設定のいずれか一つを True にする）
P.use_old_Microsoft_IME = True
P.use_new_Microsoft_IME = False
P.use_Google_IME = False

# 追加機能のオプションの設定
P.use_clipboardList = True
P.use_lancherList = True
P.use_edit_mode = False
P.use_real_emacs = False
P.use_change_keyboard = False

####################################################################################################
## 基本設定
####################################################################################################
# [section-base-1] ---------------------------------------------------------------------------------

# Emacs のキーバインドに“したくない”アプリケーションソフトを指定する
# P.not_emacs_target.remove("Code.exe")
P.not_emacs_target    += [
                         ]

# IME の切り替え“のみをしたい”アプリケーションソフトを指定する
# P.ime_target.remove("Code.exe")
P.ime_target          += [
                         ]

# キーマップ毎にキー設定をスキップするキーを指定する
# （リストに指定するキーは、define_key の第二引数に指定する記法のキーとしてください。"A-v" や "C-v"
#   のような指定の他に、"M-f" や "Ctl-x d" などの指定も可能です。）
# （ここで指定したキーに新たに別のキー設定をしたいときには、「-2」が付くセクション内で define_key2
#   関数を利用して定義してください）
P.skip_settings_key    = {"keymap_global"    : [],
                          "keymap_emacs"     : [],
                          "keymap_ime"       : [],
                          "keymap_ei"        : [],
                          "keymap_tsw"       : [],
                          "keymap_lw"        : [],
                          "keymap_edit_mode" : [],
                         }

# Emacs のキーバインドにするアプリケーションソフトで、Emacs キーバインドから除外するキーを指定する
# （リストに指定するキーは、Keyhac で指定可能なマルチストロークではないキーとしてください。
#   Fakeymacs の記法の "M-f" や "Ctl-x d" などの指定はできません。"A-v"、"C-v" などが指定可能です。）
P.emacs_exclusion_key  = {"chrome.exe"       : ["C-l", "C-t"],
                          "msedge.exe"       : ["C-l", "C-t"],
                          "firefox.exe"      : ["C-l", "C-t"],
                         }

# 左右どちらの Ctrlキーを使うかを指定する（"L": 左、"R": 右）
P.side_of_ctrl_key = "R"

#---------------------------------------------------------------------------------------------------
# IME を切り替えるキーの組み合わせ（disable、enable の順）を指定する（複数指定可）

## LAlt の単押しで英数入力、RAlt の単押しで日本語入力となる
# P.set_input_method_key += [["O-LAlt", "O-RAlt"]]

## C-j や C-j C-j で 英数入力となる（toggle_input_method_key の設定と併せ、C-j C-o で日本語入力となる）
# P.set_input_method_key += [["C-j", None]]

## C-j で英数入力、C-o で日本語入力となる（toggle_input_method_key の設定より優先）
# P.set_input_method_key += [["C-j", "C-o"]]
#---------------------------------------------------------------------------------------------------

# [section-base-2] ---------------------------------------------------------------------------------

# https://w.atwiki.jp/ntemacs/pages/75.html

# emacsclient プログラムを起動するキーを指定する
emacsclient_key = None
# emacsclient_key = "C-Period"

# emacsclient プログラムを指定する
emacsclient_name = r"<Windows パス>\wslclient-n.exe"

# emacsclient プログラムの起動
def emacsclient(keymap, emacsclient_name):
    def _func():
        clipboard_text = getClipboardText()
        if clipboard_text:
            path = re.sub("\n|\r", "", clipboard_text.strip())
            path = re.sub(r'(\\+)"', r'\1\1"', path)
            path = re.sub('"', r'\"', path)
            path = re.sub('^', '"', path)
            keymap.ShellExecuteCommand(None, emacsclient_name, path, "")()
    return _func

define_key(keymap_emacs, emacsclient_key, emacsclient(keymap, emacsclient_name))

####################################################################################################
## クリップボードリストの設定
####################################################################################################
# [section-clipboardList-1] ------------------------------------------------------------------------

# 定型文
P.fixed_items = [
    ["---------+ x 8", "---------+" * 8],
    ["メールアドレス", "user_name@domain_name"],
    ["住所",           "〒999-9999 ＮＮＮＮＮＮＮＮＮＮ"],
    ["電話番号",       "99-999-9999"],
]
P.fixed_items[0][0] = list_formatter.format(P.fixed_items[0][0])

# 日時
P.datetime_items = [
    ["YYYY/MM/DD HH:MM:SS", dateAndTime("%Y/%m/%d %H:%M:%S")],
    ["YYYY/MM/DD",          dateAndTime("%Y/%m/%d")],
    ["HH:MM:SS",            dateAndTime("%H:%M:%S")],
    ["YYYYMMDD_HHMMSS",     dateAndTime("%Y%m%d_%H%M%S")],
    ["YYYYMMDD",            dateAndTime("%Y%m%d")],
    ["HHMMSS",              dateAndTime("%H%M%S")],
]
P.datetime_items[0][0] = list_formatter.format(P.datetime_items[0][0])

P.cblisters = [
    ["定型文", cblister_FixedPhrase(P.fixed_items)],
    ["日時",   cblister_FixedPhrase(P.datetime_items)],
]

# [section-clipboardList-2] ------------------------------------------------------------------------

####################################################################################################
## ランチャーリストの設定
####################################################################################################
# [section-lancherList-1] --------------------------------------------------------------------------

# アプリケーションソフト
P.application_items = [
    ["Notepad",     keymap.ShellExecuteCommand(None, r"notepad.exe", "", "")],
    ["Explorer",    keymap.ShellExecuteCommand(None, r"explorer.exe", "", "")],
    ["Cmd",         keymap.ShellExecuteCommand(None, r"cmd.exe", "", "")],
    ["MSEdge",      keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "", "")],
    ["Chrome",      keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", "", "")],
    ["Firefox",     keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe", "", "")],
    ["Thunderbird", keymap.ShellExecuteCommand(None, r"C:\Program Files (x86)\Mozilla Thunderbird\thunderbird.exe", "", "")],
]
P.application_items[0][0] = list_formatter.format(P.application_items[0][0])

# ウェブサイト
P.website_items = [
    ["Google",          keymap.ShellExecuteCommand(None, r"https://www.google.co.jp/", "", "")],
    ["Facebook",        keymap.ShellExecuteCommand(None, r"https://www.facebook.com/", "", "")],
    ["Twitter",         keymap.ShellExecuteCommand(None, r"https://twitter.com/", "", "")],
    ["Keyhac",          keymap.ShellExecuteCommand(None, r"https://sites.google.com/site/craftware/keyhac-ja", "", "")],
    ["Fakeymacs",       keymap.ShellExecuteCommand(None, r"https://github.com/smzht/fakeymacs", "", "")],
    ["NTEmacs＠ウィキ", keymap.ShellExecuteCommand(None, r"https://w.atwiki.jp/ntemacs/", "", "")],
]
P.website_items[0][0] = list_formatter.format(P.website_items[0][0])

# その他
P.other_items = [
    ["Edit   config.py", keymap.command_EditConfig],
    ["Reload config.py", keymap.command_ReloadConfig],
]
P.other_items[0][0] = list_formatter.format(P.other_items[0][0])

P.lclisters = [
    ["App",     cblister_FixedPhrase(P.application_items)],
    ["Website", cblister_FixedPhrase(P.website_items)],
    ["Other",   cblister_FixedPhrase(P.other_items)],
]

# [section-lancherList-2] --------------------------------------------------------------------------

####################################################################################################
## C-Enter に F2（編集モード移行）を割り当てる（オプション）
####################################################################################################
# [section-edit_mode-1] ----------------------------------------------------------------------------

P.edit_mode_target = [["EXCEL.EXE",    "EXCEL*"],
                      ["explorer.exe", "DirectUIHWND"]]

# [section-edit_mode-2] ----------------------------------------------------------------------------

####################################################################################################
## Emacs の場合、IME 切り替え用のキーを C-\ に置き換える（オプション）
####################################################################################################
# [section-real_emacs-1] ---------------------------------------------------------------------------
# [section-real_emacs-2] ---------------------------------------------------------------------------

####################################################################################################
## 英語キーボード設定をした OS 上で、日本語キーボードを利用する場合の切り替えを行う（オプション）
####################################################################################################
# [section-change_keyboard-1] ----------------------------------------------------------------------
# [section-change_keyboard-2] ----------------------------------------------------------------------
