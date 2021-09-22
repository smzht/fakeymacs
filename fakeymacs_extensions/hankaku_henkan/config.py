# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 入力した文字を半角に変換し、IME を OFF にするキーを設定する（Emacs日本語入力モード用）
####################################################################################################

try:
    # 設定されているか？
    fc.hankaku_henkan_key
except:
    # 本機能を利用するためのキーを指定する
    fc.hankaku_henkan_key = "C-Enter"

if fc.use_emacs_ime_mode:

    def hankaku_henkan_key():
        self_insert_command("F10", "Enter")()
        ei_disable_input_method()

    define_key(keymap_ei, fc.hankaku_henkan_key, hankaku_henkan_key)
