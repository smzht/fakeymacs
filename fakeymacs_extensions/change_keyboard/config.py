# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 英語キーボード設定をした OS 上で日本語キーボードを利用する場合の設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.change_keyboard_key
except:
    # 利用するキーボードを切り替えるキーを指定する
    fc.change_keyboard_key = "C-A-S-Space"

try:
    # 設定されているか？
    fc.change_keyboard_startup
except:
    # Keyhac 起動時に利用するキーボードの種類を指定する
    fc.change_keyboard_startup = "US"
    # fc.change_keyboard_startup = "JP"

# OS の設定を英語キーボードにして日本語キーボードを利用する場合のお勧め設定
# （予め Change Key を使って、日本語キーボードの <￥> キーにスキャンコード 0x6F を
#   <変換> キーにスキャンコード 0x7F を割り当ててください。）

keymap.replaceKey(235, 29)               # <無変換> キーを OS が認識可能なキーにする
keymap.replaceKey(236, 28)               # <変換> キーを OS が認識可能なキーにする
keymap.replaceKey(193, "RShift")         # <＼> キーを RShift キーにする
keymap.replaceKey(237, "BackSlash")      # <￥> キーを BackSlash キーにする
keymap.replaceKey("BackSlash", "Return") # <］> キーを Enter キーにする

# リモートデスクトップで接続する場合など、一つの OS を英語キーボードと日本語キーボード
# とで混在して利用する場合の切り替えの設定

def change_keyboard(popBalloon=True):
    if fakeymacs.change_keyboard_status == "US":
        # 日本語キーボードの利用に切り替える

        # 日本語キーボードの <］> キーを Enter キーにする
        keymap.replaceKey("BackSlash", "Return")

        if popBalloon:
            keymap.popBalloon("keyboard", "[JP Keyboard]", 1000)

        fakeymacs.change_keyboard_status = "JP"
    else:
        # 英語キーボードの利用に切り替える

        # 日本語キーボードの <］> キーを元の設定に戻す
        keymap.replaceKey("BackSlash", "BackSlash")

        if popBalloon:
            keymap.popBalloon("keyboard", "[US Keyboard]", 1000)

        fakeymacs.change_keyboard_status = "US"

if fc.change_keyboard_startup == "US":
    fakeymacs.change_keyboard_status = "JP"
else:
    fakeymacs.change_keyboard_status = "US"

change_keyboard(False)

define_key(keymap_global, fc.change_keyboard_key, change_keyboard)
