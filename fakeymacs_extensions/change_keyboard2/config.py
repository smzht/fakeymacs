# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 日本語キーボード設定をした OS 上で日本語キーボードを英語配列で利用する場合の設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.change_keyboard2_key
except:
    # 利用するキーボードを切り替えるキーを指定する
    fc.change_keyboard2_key = "C-A-S-Space"

try:
    # 設定されているか？
    fc.change_keyboard2_startup
except:
    # Keyhac 起動時に利用するキーボードの種類を指定する
    fc.change_keyboard2_startup = "US"
    # fc.change_keyboard2_startup = "JP"

if not is_japanese_keyboard and use_usjis_keyboard_conversion:

    # 日本語キーボードの <＼> キーを Shift キーにする
    keymap.replaceKey("BackSlash", "Shift")

    # リモートデスクトップで接続する場合など、一つの OS を英語キーボードと日本語キーボード
    # とで混在して利用する場合の切り替えの設定

    def change_keyboard2(popBalloon=True):
        global change_keyboard2_status

        if change_keyboard2_status == "US":
            # 日本語キーボードの利用に切り替える

            # 日本語キーボードの <］> キーを Enter キーにする
            keymap.replaceKey("CloseBracket", "Enter")

            if popBalloon:
                keymap.popBalloon("keyboard", "[JP Keyboard]", 1000)

            change_keyboard2_status = "JP"
        else:
            # 英語キーボードの利用に切り替える

            # 日本語キーボードの <］> キーを元の設定に戻す
            keymap.replaceKey("CloseBracket", "CloseBracket")

            if popBalloon:
                keymap.popBalloon("keyboard", "[US Keyboard]", 1000)

            change_keyboard2_status = "US"

    if fc.change_keyboard2_startup == "US":
        change_keyboard2_status = "JP"
    else:
        change_keyboard2_status = "US"

    change_keyboard2(False)

    define_key(keymap_global, fc.change_keyboard2_key, change_keyboard2)
