; -*- coding: utf-8-with-signature-dos -*-

#NoTrayIcon
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.

InputBox, ShellCommand, Command dialog, Shell command on region:,,,130
If ErrorLevel = 0
{
        clipboard = %ShellCommand%
        Sleep, 100
        Send, ^+\
}
