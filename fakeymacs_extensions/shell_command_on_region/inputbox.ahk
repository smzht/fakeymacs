; -*- coding: utf-8-with-signature-dos -*-

#NoTrayIcon
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.

WinGetPos, win_x, win_y, win_width, win_height, A

dialog_width := 400
dialog_height := 130

dialog_x := win_x + win_width / 2 - dialog_width / 2
dialog_y := win_y + win_height / 2 - dialog_height / 2

InputBox, ShellCommand, Command dialog, Shell command on region:,, dialog_width, dialog_height, dialog_x, dialog_y
If ErrorLevel = 0
{
        clipboard = %ShellCommand%
        Sleep, 500
        Send, ^+{F12}
}
