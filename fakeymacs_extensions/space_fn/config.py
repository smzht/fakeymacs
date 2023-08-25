# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## SpaceFn を実現する設定を行う
####################################################################################################

keymap.defineModifier("Space", "User0")

for mod in ["", "S-"]:
    mkey0 = mod + "Space"
    mkey1 = mod + "O-Space"

    func = getKeyCommand(keymap_emacs, mkey0)
    if func:
        define_key(keymap_emacs, mkey0, lambda: None)
        define_key(keymap_emacs, mkey1, func)

def define_key_f(keys, command):
    define_key(keymap_emacs, keys, command)

def replicate_key(keys, originalKeys):
    func = getKeyCommand(keymap_emacs, originalKeys)
    if func:
        define_key(keymap_emacs, keys, func)

## config_personal.py ファイルの読み込み
exec(readConfigExtension(r"space_fn\config_personal.py", msg=False), dict(globals(), **locals()))
