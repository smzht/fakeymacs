# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## ウィンドウ操作のための設定を行う
####################################################################################################

try:
    # 設定されているか？
    fc.minimize_window_key
except:
    # ウィンドウを最小化、リストアするキーの組み合わせ（リストア、最小化 の順）を指定する（複数指定可）
    fc.minimize_window_key = []
    fc.minimize_window_key += [["A-S-m", "A-m"]]

try:
    # 設定されているか？
    fc.maximize_window_key
except:
    # ウィンドウを最大化、リストアするキーの組み合わせ（リストア、最大化 の順）を指定する（複数指定可）
    # （マルチディスプレイでの最大化にも対応しています）
    fc.maximize_window_key = []
    fc.maximize_window_key += [["W-S-q", "W-q"]] # Windows ショートカットキーの W-q の機能は、W-s で代用可
    # fc.maximize_window_key += [["W-S-m", "W-m"]] # Windows ショートカットキーの W-m の機能は、W-d で代用可
    # fc.maximize_window_key += [["W-S-s", "W-s"]] # Windows ショートカットキーの W-s の機能は、W-q で代用可

try:
    # 設定されているか？
    fc.switch_windows_key
except:
    # アクティブウィンドウを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （A-Esc キーの動作とは異なり、仮想デスクトップを跨ぎ、最小化されていないウィンドウを順に切り替え
    #   ます。初期設定は ["A-p", "A-n"] としていますが、Emacs の shell-mode のキーバインドなどと設定が
    #   被る場合には、["A-S-p", "A-S-n"] などの異なる設定とするか、Emacs 側に次の設定を入れて、Emacs 側
    #   のキーの設定を置き換えてご利用ください。
    #     (define-key key-translation-map (kbd "M-S-p") (kbd "M-p"))
    #     (define-key key-translation-map (kbd "M-S-n") (kbd "M-n"))
    #  ）
    fc.switch_windows_key = []
    fc.switch_windows_key += [["A-p", "A-n"]]
    # fc.switch_windows_key += [["A-S-p", "A-S-n"]]
    # fc.switch_windows_key += [["A-Up", "A-Down"]]

try:
    # 設定されているか？
    fc.switch_windows_key2
except:
    # アクティブなウィンドウと同じプロセスのウィンドウを順に切り替えるキーの組み合わせ（前、後 の順）
    # を指定する（複数指定可）
    fc.switch_windows_key2 = []
    fc.switch_windows_key2 += [["A-S-p", "A-S-n"]]
    # fc.switch_windows_key2 += [["W-Tab", "W-S-Tab"]]

try:
    # 設定されているか？
    fc.move_window_key_for_displays
except:
    # アクティブウィンドウをディスプレイ間で移動するキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （デフォルトキーは、["W-S-Left", "W-S-Right"]）
    fc.move_window_key_for_displays = []
    fc.move_window_key_for_displays += [[None, "W-o"]]
    # fc.move_window_key_for_displays += [[None, "A-S-o"]]

try:
    # 設定されているか？
    fc.transpose_windows_key
except:
    # デュアルディスプレイにそれぞれ表示されているウィンドウを入れ替えるキーを指定する
    fc.transpose_windows_key = "W-t"

try:
    # 設定されているか？
    fc.switch_desktops_key
except:
    # 仮想デスクトップを切り替えるキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （仮想デスクトップを切り替えた際にフォーカスのあるウィンドウを適切に処理するため、設定するキーは
    #   Win キーとの組み合わせとしてください）
    # （デフォルトキーは、["W-C-Left", "W-C-Right"]）
    fc.switch_desktops_key = []
    fc.switch_desktops_key += [["W-b", "W-f"]]
    # fc.switch_desktops_key += [["W-Left", "W-Right"]]

try:
    # 設定されているか？
    fc.move_window_key_for_desktops
except:
    # アクティブウィンドウを仮想デスクトップ間で移動するキーの組み合わせ（前、後 の順）を指定する（複数指定可）
    # （本機能を利用する場合は、次のページから SylphyHornPlus をインストールしてください。
    #   ・https://github.com/hwtnb/SylphyHornPlusWin11/releases
    #   SylphyHornPlus は、Microsoft Store からインストール可能な SylphyHorn の Fork で、Windows 11 の
    #   対応など、改良が加えられたものとなっています。）
    # （アクティブウィンドウを仮想デスクトップ間で移動するためのデフォルトキーは、["W-C-A-Left", "W-C-A-Right"]
    #   です。この設定は変更しないでください。）
    fc.move_window_key_for_desktops = []
    # fc.move_window_key_for_desktops += [["W-p", "W-n"]]
    # fc.move_window_key_for_desktops += [["W-Up", "W-Down"]]

# --------------------------------------------------------------------------------------------------

def minimize_window():
    window = getTopLevelWindow()
    if window and not window.isMinimized():
        window.minimize()
        delay()
        window_list = getWindowList()
        if window in window_list:
            if window is window_list[-1]:
                fakeymacs.reverse_window_to_restore = False
            else:
                fakeymacs.reverse_window_to_restore = True

def restore_minimized_window():
    window_list = getWindowList(True)
    if window_list:
        if not fakeymacs.reverse_window_to_restore:
            window_list.reverse()
        window_list[0].restore()

display_areas = [monitor[1] for monitor in pyauto.Window.getMonitorInfo()]
display_cnt = len(display_areas)

max_rect = [min([left   for left, top, right, bottom in display_areas]) - 8,
            max([top    for left, top, right, bottom in display_areas]) - 8,
            max([right  for left, top, right, bottom in display_areas]) + 8,
            min([bottom for left, top, right, bottom in display_areas]) + 8]

window_dict = {}

def resize_window(forward_direction):
    def _setRect(rect):
        # setRect 関数を２回繰り返して実行しているのは、DPI スケールが異なるディスプレイがある
        # 場合、表示されているウィンドウの位置によってウィンドウを表示するスケールが決まるため、
        # 一回目でウインドウの位置決めをして、二回目で表示スケールを確定させている。
        window.setRect(rect)
        window.setRect(rect)

    window = getTopLevelWindow()
    if window:
        if display_cnt == 1:
            if window.isMaximized():
                window.restore()
            else:
                window.maximize()
        else:
            if window.isMaximized():
                if forward_direction:
                    window.restore()
                    delay()
                    if window not in window_dict:
                        window_dict[window] = list(window.getRect())
                    _setRect(max_rect)
                else:
                    if window in window_dict:
                        _setRect(window_dict[window])
                        del window_dict[window]
                    else:
                        window.restore()
            else:
                if window in window_dict:
                    _setRect(window_dict[window])
                    del window_dict[window]

                    if not forward_direction:
                        window.maximize()
                else:
                    if forward_direction:
                        window.maximize()
                    else:
                        window_dict[window] = list(window.getRect())
                        _setRect(max_rect)

def maximize_window():
    resize_window(True)

def restore_maximized_window():
    resize_window(False)

window_list = []
window_switching_time = 0

def windowList():
    global window_list
    global window_switching_time

    if time.time() - window_switching_time > 1.5:
        window_list = getWindowList(False)

    window_switching_time = time.time()
    return window_list

process_name = ""
window_list2 = []
window_switching_time2 = 0

def windowList2():
    global process_name
    global window_list2
    global window_switching_time2

    if (process_name != getProcessName() or
        (time.time() - window_switching_time2 > 1.5)):
        process_name = getProcessName()
        window_list2 = getWindowList(None, process_name)

    window_switching_time2 = time.time()
    return window_list2

def switchWindows(window_list_func, direction):
    window_list = window_list_func()

    # ２つのリストに差異があるか？
    if set(window_list) ^ set(fakeymacs.window_list):
        fakeymacs.window_list = window_list

    if fakeymacs.window_list:
        index = {"previous":-1, "next":1}[direction]
        window_list = fakeymacs.window_list[index:] + fakeymacs.window_list[:index]
        popWindow(window_list[0])()
        fakeymacs.window_list = window_list

def previous_window(window_list_func):
    def _func():
        keymap.delayedCall(lambda: switchWindows(window_list_func, "previous"), 0)
    return _func

def next_window(window_list_func):
    def _func():
        keymap.delayedCall(lambda: switchWindows(window_list_func, "next"), 0)
    return _func

def move_window_to_previous_display():
    self_insert_command("W-S-Left")()

def move_window_to_next_display():
    self_insert_command("W-S-Right")()

def transpose_windows():
    if display_cnt == 2:
        def _transpose_windows():
            window_list = getWindowList()
            if len(window_list) >= 2:
                first_window = None
                for window in window_list:
                    window_rect = window.getRect()
                    for display_area in display_areas:
                        if (window_rect[0] >= display_area[0] - 16 and
                            window_rect[1] >= display_area[1] - 16 and
                            window_rect[2] <= display_area[2] + 16 and
                            window_rect[3] <= display_area[3] + 16):
                            if first_window:
                                if display_area != first_window:
                                    popWindow(window)()
                                    delay()
                                    move_window_to_previous_display()
                                    other_window()
                                    delay()
                                    move_window_to_next_display()
                                    return
                            else:
                                popWindow(window)()
                                delay()
                                first_window = display_area
                            break

        keymap.delayedCall(_transpose_windows, 0)

def previous_desktop():
    self_insert_command("W-C-Left")()

def next_desktop():
    self_insert_command("W-C-Right")()

def move_window_to_previous_desktop():
    self_insert_command("LW-LC-LA-Left")()

def move_window_to_next_desktop():
    self_insert_command("LW-LC-LA-Right")()

# ウィンドウの最小化、リストア
for restore_key, minimize_key in fc.minimize_window_key:
    define_key(keymap_global, restore_key,  restore_minimized_window)
    define_key(keymap_global, minimize_key, minimize_window)

# ウィンドウの最大化、リストア
for restore_key, maximize_key in fc.maximize_window_key:
    define_key(keymap_global, restore_key,  restore_maximized_window)
    define_key(keymap_global, maximize_key, maximize_window)

# アクティブウィンドウの切り替え
for previous_key, next_key in fc.switch_windows_key:
    define_key(keymap_global, previous_key, previous_window(windowList))
    define_key(keymap_global, next_key,     next_window(windowList))

# アクティブなウィンドウと同じプロセスのウィンドウの切り替え
for previous_key, next_key in fc.switch_windows_key2:
    define_key(keymap_global, previous_key, previous_window(windowList2))
    define_key(keymap_global, next_key,     next_window(windowList2))

# アクティブウィンドウのディスプレイ間移動
for previous_key, next_key in fc.move_window_key_for_displays:
    define_key(keymap_global, previous_key, move_window_to_previous_display)
    define_key(keymap_global, next_key,     move_window_to_next_display)

# デュアルディスプレイにそれぞれ表示されているウィンドウの入れ替え
define_key(keymap_global, fc.transpose_windows_key, transpose_windows)

# 仮想デスクトップの切り替え
for previous_key, next_key in fc.switch_desktops_key:
    define_key(keymap_global, previous_key, previous_desktop)
    define_key(keymap_global, next_key,     next_desktop)

# アクティブウィンドウの仮想デスクトップ間移動
for previous_key, next_key in fc.move_window_key_for_desktops:
    define_key(keymap_global, previous_key, move_window_to_previous_desktop)
    define_key(keymap_global, next_key,     move_window_to_next_desktop)
