# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 60% US キーボードのキー不足（Delete キー、Backquote キー不足）の対策を行う
####################################################################################################

define_key(keymap_global, "C-A-Back", self_insert_command("C-A-Delete"))

if not is_japanese_keyboard:
    define_key(keymap_global, "S-Back", keymap.defineMultiStrokeKeymap("S-Back"))

    for mod1 in ["", "W-"]:
        for mod2 in ["", "A-"]:
            for mod3 in ["", "C-"]:
                for mod4 in ["", "S-"]:
                    mkey  = mod1 + mod2 + mod3 + mod4
                    mkey1 = mkey + "Back"
                    mkey2 = mkey + "BackQuote"
                    define_key(keymap_global, "S-Back " + mkey1, self_insert_command(mkey2))

    # vscode_key Extension が有効な場合の追加設定
    try:
        # vscode_key Extension は有効か？
        fakeymacs.keymap_vscode

        def define_key_vsc(keys, command):
            define_key3(keymap_global, keys, command,
                        lambda: (fakeymacs.is_vscode_target(keymap.getWindow()) and
                                 (checkWindow(process_name="Code.exe") or
                                  checkWindow(text="* - Visual Studio Code*"))))

        define_key_vsc("S-Back C-S-Back", getKeyCommand(fakeymacs.keymap_vscode, "C-S-`"))
        define_key_vsc("S-Back C-Back",   getKeyCommand(fakeymacs.keymap_vscode, "C-`"))

    except:
        pass
