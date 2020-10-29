# -*- mode: python; coding: utf-8-with-signature-dos -*-

####################################################################################################
## shell-command-on-region の機能をサポートする
####################################################################################################

import subprocess

def shell_command_inputbox():
    if fakeymacs.is_universal_argument:
        fakeymacs.replace_region = True
    else:
        fakeymacs.replace_region = False

    # keymap.ShellExecuteCommand(None, r"fakeymacs_extensions\shell_command_on_region\inputbox.ahk", "", "")()
    keymap.ShellExecuteCommand(None, r"fakeymacs_extensions\shell_command_on_region\inputbox.exe", "", "")()

def shell_command_on_region():
    def executeShellCommand():
        shell_command = getClipboardText()
        print("$ cat region | " + shell_command)

        setClipboardText("")
        copyRegion()
        delay()
        clipboard_text = re.sub("\r", "", getClipboardText())

        command = [r"C:\WINDOWS\SysNative\wsl.exe", "bash", "-c"]
        command += [r" tr -d '\r' | " + shell_command]

        proc = subprocess.run(command,
                              input=clipboard_text,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              creationflags=subprocess.CREATE_NO_WINDOW,
                              encoding="utf8")

        stdout_text = proc.stdout
        stdout_list = stdout_text.splitlines()

        print("-" * 80)
        print("\n".join(stdout_list[0:10]))
        if len(stdout_list) > 10:
            print("...")
        print("-" * 80)
        print("\n")

        if proc.returncode == 0:
            setClipboardText(stdout_text)

            if fakeymacs.replace_region:
                keymap.delayedCall(yank, 30)

    # キーフックの中で時間のかかる処理を実行できないので、delayedCall() を使って遅延実行する
    keymap.delayedCall(executeShellCommand, 100)

define_key(keymap_emacs, "M-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_inputbox)))))
define_key(keymap_emacs, "C-S-BackSlash", reset_search(reset_undo(reset_counter(reset_mark(shell_command_on_region)))))
