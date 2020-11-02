# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 英語キーボード設定をした OS 上で、日本語キーボードを利用する場合の切り替えを行う
####################################################################################################

# https://w.atwiki.jp/ntemacs/pages/90.html

# OS の設定を英語キーボードにして日本語キーボードを利用する場合のお勧め設定
# （予め、Change Key を使って、<￥> キーにスキャンコード 0x7F を割り当ててください）

try:
    # 設定されているか？
    fc.change_keyboard_key
except:
    fc.change_keyboard_key = "C-A-S-Space"

keymap.replaceKey(235, 29)               # <無変換> キーを OS が認識可能なキーにする
keymap.replaceKey(255, 28)               # <変換> キーを OS が認識可能なキーにする
keymap.replaceKey(193, "RShift")         # <＼> キーを RShift キーにする
keymap.replaceKey(236, "BackSlash")      # <￥> キーを BackSlash キーにする
keymap.replaceKey("BackSlash", "Return") # < ]> キーを Enter キーにする

# リモートデスクトップで接続する場合など、一つの OS を英語キーボードと日本語キーボード
# とで混在して利用する場合の切り替えの設定

def change_keyboard():
    if fakeymacs.keyboard_status == "US":
        # 日本語キーボードの利用に切り替える

        # 日本語キーボードの < ]> キーを Enter キーにする
        keymap.replaceKey("BackSlash", "Return")

        keymap.popBalloon("keyboard", "[JP Keyboard]", 1000)
        fakeymacs.keyboard_status = "JP"

    else:
        # 英語キーボードの利用に切り替える

        # 日本語キーボードの < ]> キーを元の設定に戻す
        keymap.replaceKey("BackSlash", "BackSlash")

        if fakeymacs.keyboard_status == "JP":
            keymap.popBalloon("keyboard", "[US Keyboard]", 1000)
        fakeymacs.keyboard_status = "US"

fakeymacs.keyboard_status = None
change_keyboard()

define_key(keymap_global, fc.change_keyboard_key, change_keyboard)
