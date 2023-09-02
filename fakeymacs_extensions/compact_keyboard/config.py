# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## 60% US キーボードのキー不足（Delete キー、Backquote キー不足）の対策を行う
####################################################################################################

define_key(keymap_base, "C-A-Back", getKeyAction("C-A-Delete"))

if not is_japanese_keyboard:

    define_key(keymap_base, "S-Back", keymap.defineMultiStrokeKeymap("S-Back"))

    for mod1, mod2, mod3, mod4 in itertools.product(["", "W-"], ["", "A-"], ["", "C-"], ["", "S-"]):
        mkey  = mod1 + mod2 + mod3 + mod4
        mkey1 = mkey + "Back"
        mkey2 = mkey + "BackQuote"
        define_key(keymap_base, f"S-Back {mkey1}", getKeyAction(mkey2))
