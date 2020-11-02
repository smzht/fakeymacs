# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## Emacs の shell-command-on-region の機能をサポートする
####################################################################################################

try:
    # 設定されているか？
    fc.Linux_tool
except:
    # 次の設定のいずれかを有効にする
    fc.Linux_tool = "Busybox"
    # fc.Linux_tool = "WSL"

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

            if fc.Linux_tool == "Busybox":
                command = [dataPath() + r"\fakeymacs_extensions\shell_command_on_region\busybox64.exe",
                           "bash", "-c"]
                command += [shell_command]
                encoding = "cp932"

            if fc.Linux_tool == "WSL":
                command = [r"C:\WINDOWS\SysNative\wsl.exe", "bash", "-c"]
                command += [r"tr -d '\r' | " + re.sub(r"(\$)", r"\\\1", shell_command)]
                encoding = "utf-8"

            try:
                proc = subprocess.run(command,
                                      input=clipboard_text,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT,
                                      creationflags=subprocess.CREATE_NO_WINDOW,
                                      encoding=encoding,
                                      timeout=5)
            except:
                print("プログラムがエラー終了しました（タイムアウトによる終了含む）\n")
                return

            stdout_text = proc.stdout
            stdout_list = stdout_text.splitlines()

            print("$ cat region | " + shell_command)
            print("-" * 80)
            print("\n".join(stdout_list[0:10]))
            if len(stdout_list) > 10:
                print("...")
            print("-" * 80)
            print("")

            setClipboardText(stdout_text)
            if keymap.getWindow().getProcessName() in fc.not_clipboard_target:
                keymap.clipboard_history._push(stdout_text)

            if fakeymacs.replace_region:
                keymap.delayedCall(yank, 30)
        else:
            print("コマンドが指定されていません\n")

    # キーフックの中で時間のかかる処理を実行できないので、delayedCall() を使って遅延実行する
    keymap.delayedCall(executeShellCommand, 100)

define_key(keymap_emacs, "M-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_inputbox)))))
define_key(keymap_emacs, "LC-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_on_region)))))
