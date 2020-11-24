# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Emacs の shell-command-on-region の機能をサポートする
####################################################################################################

try:
    # 設定されているか？
    fc.Linux_tool
except:
    # Linux コマンドを起動するために利用する Linux ツールを指定する
    fc.Linux_tool = "WSL"
    # fc.Linux_tool = "MSYS2"
    # fc.Linux_tool = "Cygwin"
    # fc.Linux_tool = "BusyBox"

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

import subprocess

def shell_command_inputbox():
    if fakeymacs.is_universal_argument:
        fakeymacs.replace_region = True
    else:
        fakeymacs.replace_region = False

    # inputbox_command = dataPath() + r"\fakeymacs_extensions\shell_command_on_region\inputbox.ahk"
    inputbox_command = dataPath() + r"\fakeymacs_extensions\shell_command_on_region\inputbox.exe"

    keymap.ShellExecuteCommand(None, inputbox_command, "", "")()

def shell_command_on_region():
    def executeShellCommand():
        shell_command = getClipboardText()

        if shell_command:
            setClipboardText("")
            copyRegion()
            delay(0.5)
            clipboard_text = re.sub("\r", "", getClipboardText())

            env = dict(os.environ)

            # 以降で実行するコマンドは、bash に -l オプションを付け、その配下で実行するようにしています。
            # このため、bash を起動する環境の .bash_profile に多くの設定を記入していると、コマンドの
            # 実行が遅かったり、コマンドが正しくフィルタとして機能しなかったりする場合があります。
            # このようなときに .bash_profile 内の設定をコントロール（スキップ）できるようにするため、
            # FAKEYMACS 環境変数を設定しています。
            env["FAKEYMACS"] = "1"

            if fc.Linux_tool == "WSL":
                command = [r"C:\WINDOWS\SysNative\wsl.exe", "bash", "-l", "-c"]
                command += [r"tr -d '\r' | " + re.sub(r"(\$)", r"\\\1", shell_command)]
                env["LANG"] = "ja_JP.UTF8"
                env["WSLENV"] = "FAKEYMACS:LANG"
                encoding = "utf-8"

            elif fc.Linux_tool == "MSYS2":
                command = [fc.MSYS2_path + r"\usr\bin\bash.exe", "-l", "-c"]
                command += [shell_command]
                env["LANG"] = "ja_JP.UTF8"
                encoding = "utf-8"

            elif fc.Linux_tool == "Cygwin":
                command = [fc.Cygwin_path + r"\bin\bash.exe", "-l", "-c"]
                command += [r"tr -d '\r' | " + shell_command]
                env["LANG"] = "ja_JP.UTF8"
                encoding = "utf-8"

            elif fc.Linux_tool == "BusyBox":
                command = [fc.BusyBox_path + r"\busybox64.exe", "bash", "-l", "-c"]
                command += [shell_command]
                encoding = "cp932"

            try:
                proc = subprocess.run(command,
                                      input=clipboard_text,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      timeout=10,
                                      creationflags=subprocess.CREATE_NO_WINDOW,
                                      encoding=encoding,
                                      env=env)
            except:
                print("プログラムがエラー終了しました（タイムアウトによる終了も含む）\n")
                return

            stdout_text = proc.stdout
            stdout_list = stdout_text.splitlines()

            print("$ cat region | " + shell_command)
            print("-" * 80)

            # Keyhac コンソールにタブを出力すると出力結果が不正になる場合があるため、expandtabs() で
            # スペースに変換してから出力する
            print("\n".join(stdout_list[0:10]).expandtabs())
            if len(stdout_list) > 10:
                print("...")

            print("-" * 80)
            print("")

            setClipboardText(stdout_text)
            if keymap.getWindow().getProcessName() in fc.not_clipboard_target:
                keymap.clipboard_history._push(stdout_text)

            if fakeymacs.replace_region:
                # delay() のコールでは yank に失敗することがあるため、delayedCall() 経由で実行する
                keymap.delayedCall(yank, 30)
        else:
            print("コマンドが指定されていません\n")

    # キーフックの中で時間のかかる処理を実行できないので、delayedCall() を使って遅延実行する
    keymap.delayedCall(executeShellCommand, 100)

define_key(keymap_emacs, "M-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_inputbox)))))
define_key(keymap_emacs, "LC-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_on_region)))))
