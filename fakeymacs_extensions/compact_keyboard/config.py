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
                    mkey2 = mkey + "Backquote"
                    define_key(keymap_global, "S-Back " + mkey1, self_insert_command(mkey2))
