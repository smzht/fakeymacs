# -*- mode: python; coding: utf-8-with-signature-dos -*-

# 本ファイルは、config_personal.py というファイル名にすることで browser_key Extension の
# 機能拡張ファイルとして機能します。以下はサンプルコードです。

# --------------------------------------------------------------------------------------------------

try:
    # chrome_quick_tabs Extension が有効になっているか？
    fc.quick_tabs_shortcut_key

    # ブラウザをポップアップしてから Quick Tabs を起動する
    define_key(keymap_global, "C-A-;", browser_popup(fc.quick_tabs_shortcut_key, 0, fc.chrome_list))
except:
    pass

# --------------------------------------------------------------------------------------------------
