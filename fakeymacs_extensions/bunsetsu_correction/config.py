# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 旧 Microsoft IME を使って文節長を変更した際、文節の表示が正しく行われないアプリの対策を行う
####################################################################################################

try:
    # 設定されているか？
    fc.bunsetsu_correction_app_list
except:
    # 本機能を適用するアプリを指定する
    fc.bunsetsu_correction_app_list = ["chrome.exe",
                                       "msedge.exe",
                                       ]

# --------------------------------------------------------------------------------------------------

if fc.use_emacs_ime_mode:
    if fc.ime == "old_Microsoft_IME":
        command_keep = {}

        # 「IME のショートカットの置き換え」のキー設定
        for replace_key, original_key in fc.emacs_ime_mode_key:
            if original_key == "S-Left":
                key_list = [original_key, "Right", "Left"]
            elif original_key == "S-Right":
                key_list = [original_key, "Left",  "Right"]
            else:
                continue

            define_key3(keymap_ei, replace_key,
                        self_insert_command(*key_list),
                        lambda: any(checkWindow(*app) if type(app) is list else
                                    checkWindow(app) for app in fc.bunsetsu_correction_app_list))

            command_keep[replace_key] = getKeyCommand(keymap_ei, replace_key)

        ## 「IME の切り替え」のキー設定
        for key in fc.toggle_input_method_key:
            if key in command_keep:
                define_key(keymap_ei, key, ei_disable_input_method2(key, command_keep[key]))

        ## 「IME の切り替え」のキー設定
        for disable_key, enable_key in fc.set_input_method_key:
            if disable_key in command_keep:
                define_key(keymap_ei, disable_key,
                           ei_disable_input_method2(disable_key, command_keep[disable_key]))
            if enable_key in command_keep:
                define_key(keymap_ei, enable_key,
                           ei_enable_input_method2(enable_key, command_keep[enable_key]))
