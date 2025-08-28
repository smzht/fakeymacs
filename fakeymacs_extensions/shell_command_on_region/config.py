# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Emacs の shell-command-on-region の機能をサポートする
####################################################################################################

try:
    # 設定されているか？
    fc.output_line_count
except:
    # 実行結果を Keyhac コンソールに出力する行数を指定する
    fc.output_line_count = 78

try:
    # 設定されているか？
    fc.foreground_timeout
except:
    # フォアグラウンド処理（C-u の前置が１回以下の場合）のタイムアウト値（秒）を指定する
    fc.foreground_timeout = 10

try:
    # 設定されているか？
    fc.background_timeout
except:
    # バックグラウンド処理（C-u を２回前置した場合）のタイムアウト値（秒）を指定する
    fc.background_timeout = 600

try:
    # 設定されているか？
    fc.unix_tool
except:
    # Unix コマンドを起動するために利用する Unix ツールを指定する
    fc.unix_tool = "WSL"
    # fc.unix_tool = "MSYS2"
    # fc.unix_tool = "Cygwin"
    # fc.unix_tool = "BusyBox"

try:
    # 設定されているか？
    fc.bash_options
except:
    # Bash のオプション（-c 以外）を指定する
    fc.bash_options = ["-l"]

try:
    # 設定されているか？
    fc.MSYS2_path
except:
    # MSYS2 をインストールしているパスを指定する
    fc.MSYS2_path = r"C:\msys64"

try:
    # 設定されているか？
    fc.Cygwin_path
except:
    # Cygwin をインストールしているパスを指定する
    fc.Cygwin_path = r"C:\cygwin64"

try:
    # 設定されているか？
    fc.BusyBox_path
except:
    # BusyBox をインストールしているパスを指定する
    fc.BusyBox_path = dataPath() + r"\fakeymacs_extensions\shell_command_on_region"
    # fc.BusyBox_path = r"C:\busybox64"

# --------------------------------------------------------------------------------------------------

import sys
import subprocess
import threading

def shell_command_inputbox():
    global forward_direction
    global command_mode
    global clipboard_text

    forward_direction = fakeymacs.forward_direction

    if not fakeymacs.is_universal_argument:
        command_mode = 1
    else:
        if fakeymacs.repeat_counter == 4:
            command_mode = 2
        else:
            command_mode = 3

    setClipboardText("")
    copyRegion()
    delay(0.5)
    clipboard_text = re.sub("\r", "", getClipboardText())

    # inputbox_command = dataPath() + r"\fakeymacs_extensions\shell_command_on_region\inputbox.ahk"
    inputbox_command = dataPath() + r"\fakeymacs_extensions\shell_command_on_region\inputbox.exe"

    keymap.ShellExecuteCommand(None, inputbox_command, "", "")()

def executeShellCommand():
    shell_command_mode = command_mode
    shell_command = input_command
    region_text = clipboard_text

    env = dict(os.environ)

    # bash に -l オプションを付け実行する場合、bash を起動する環境の .bash_profile に多くの
    # 設定を記入していると、コマンドの実行が遅かったり、コマンドが正しくフィルタとして機能
    # しなかったりする場合があります。
    # このようなときに .bash_profile 内の設定をコントロール（スキップ）できるようにするため、
    # FAKEYMACS 環境変数を設定しています。
    env["FAKEYMACS"] = "1"

    bash_options = []
    if fc.bash_options:
        bash_options += fc.bash_options
    bash_options += ["-c"]

    if fc.unix_tool == "WSL":
        if sys.maxsize > 2*32:
            # for Keyhac v1.83
            command = [r"C:\Windows\System32\wsl.exe", "bash"]
        else:
            # for Keyhac v1.82
            command = [r"C:\Windows\SysNative\wsl.exe", "bash"]

        command += bash_options
        command += [r"cd; tr -d '\r' | " + re.sub(r"(\$)", r"\\\1", shell_command)]
        env["LANG"] = "ja_JP.UTF8"
        env["WSLENV"] = "FAKEYMACS:LANG"
        encoding = "utf-8"

    elif fc.unix_tool == "MSYS2":
        command = [fc.MSYS2_path + r"\usr\bin\bash.exe"]
        command += bash_options
        command += [shell_command]
        env["LANG"] = "ja_JP.UTF8"
        encoding = "utf-8"

    elif fc.unix_tool == "Cygwin":
        command = [fc.Cygwin_path + r"\bin\bash.exe"]
        command += bash_options
        command += [r"tr -d '\r' | " + shell_command]
        env["LANG"] = "ja_JP.UTF8"
        encoding = "utf-8"

    elif fc.unix_tool == "BusyBox":
        command = [fc.BusyBox_path + r"\busybox64.exe", "bash"]
        command += bash_options
        command += [shell_command]
        encoding = "cp932"

    try:
        if shell_command_mode == 1 or shell_command_mode == 2:
            timeout = fc.foreground_timeout
        else:
            timeout = fc.background_timeout

        proc = subprocess.run(command,
                              input=region_text,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              timeout=timeout,
                              creationflags=subprocess.CREATE_NO_WINDOW,
                              encoding=encoding,
                              env=env)

        stdout_text = proc.stdout
        stdout_list = stdout_text.splitlines()

        print("$ cat region | " + shell_command)
        print("-" * 80)

        # Keyhac コンソールにタブを出力すると出力結果が不正になる場合があるため、expandtabs() で
        # スペースに変換してから出力する
        print("\n".join(stdout_list[0:fc.output_line_count]).expandtabs())
        if len(stdout_list) > fc.output_line_count:
            print("...")

        print("-" * 80)
        print("")

        setClipboardText(stdout_text)
        pushToClipboardList()

        if shell_command_mode == 1:
            keymap.popBalloon("shell_command", "[Stored on the clipboard.]", 1000)

        elif shell_command_mode == 2:
            # delay() のコールでは yank に失敗することがあるため、delayedCall() 経由で実行する
            keymap.delayedCall(yank, 30)
            fakeymacs.forward_direction = None
            keymap.closeBalloon("shell_command")
    except:
        if shell_command_mode == 1 or shell_command_mode == 2:
            keymap.popBalloon("shell_command", "[An error has occurred (including timeout).]", 2000)

        print(f"エラーが発生しました（タイムアウト（設定値：{timeout}秒）を含む）")

        if shell_command_mode == 1 or shell_command_mode == 2:
            print("時間の掛かる処理は、C-u を２回前置して、バックグラウンドで処理を実行してください\n")

def shell_command_on_region():
    global input_command

    input_command = getClipboardText()
    fakeymacs.forward_direction = forward_direction

    if input_command:
        if command_mode == 1 or command_mode == 2:
            keymap.popBalloon("shell_command", "[Processing...]")
            keymap.delayedCall(executeShellCommand, 100)
        else:
            keymap.popBalloon("shell_command", "[Start in the background]", 1000)
            keymap.delayedCall(threading.Thread(target=executeShellCommand, daemon=True).start, 100)
    else:
        keymap.popBalloon("shell_command", "[No command specified]", 1000)
        print("コマンドが指定されていません\n")

define_key(keymap_emacs, "M-|", reset_search(reset_undo(reset_counter(reset_mark(shell_command_inputbox)))))
define_key(keymap_emacs, f"LC-S-{vkToStr(VK_F12)}", reset_search(reset_undo(reset_counter(shell_command_on_region))))
