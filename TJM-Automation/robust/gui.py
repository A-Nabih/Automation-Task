import os
import time
import subprocess
import logging
from pathlib import Path
import pyautogui
import pygetwindow as gw

from .clipboard import ClipboardManager
from .waiter import Waiter


class GuiController:
    def __init__(self, logger: logging.Logger, typing_interval: float, waits):
        self.logger = logger
        self.typing_interval = typing_interval
        self.waits = waits
        self.notepad_win = None
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

    def launch_or_focus_notepad(self) -> bool:
        try:
            windows = gw.getWindowsWithTitle('Notepad')
            if windows:
                self.notepad_win = windows[0]
            else:
                subprocess.Popen(['notepad.exe'])
                ok = Waiter.wait_for(lambda: len(gw.getWindowsWithTitle('Notepad')) > 0, self.waits.get('window', 5))
                if not ok:
                    self.logger.error('Notepad window did not appear')
                    return False
                self.notepad_win = gw.getWindowsWithTitle('Notepad')[0]
            self.notepad_win.activate()
            time.sleep(0.3)
            return True
        except Exception as exc:
            self.logger.error(f"Failed to launch/focus Notepad: {exc}")
            return False

    def replace_editor_text(self, text: str, clipboard: ClipboardManager) -> bool:
        try:
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.05)
            pyautogui.press('delete')
            time.sleep(0.05)
            if clipboard.set_text(text):
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                pyautogui.hotkey('ctrl', 'home')
                pyautogui.hotkey('ctrl', 'shift', 'end')
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(0.05)
                pasted = clipboard.get_text()
                if pasted and pasted[:64] == text[:64]:
                    return True
                self.logger.warning('Clipboard paste verification weak; falling back to typing')
            pyautogui.write(text, interval=self.typing_interval)
            return True
        except Exception as exc:
            self.logger.error(f"Failed to input text: {exc}")
            return False

    def save_via_ui(self, directory: Path, filename: str) -> bool:
        try:
            self.notepad_win.activate()
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'shift', 's')
            ok = Waiter.wait_for(lambda: True, self.waits.get('save_dialog', 1.0))
            if not ok:
                self.logger.warning('Save dialog wait elapsed; proceeding')
            pyautogui.write(str(directory))
            pyautogui.press('enter')
            time.sleep(0.2)
            pyautogui.write(filename)
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.hotkey('alt', 'y')
            time.sleep(0.2)
            pyautogui.press('enter')
            return True
        except Exception as exc:
            self.logger.error(f"Save via UI failed: {exc}")
            return False

    def handle_unexpected_dialogs(self) -> None:
        try:
            pyautogui.press('esc')
            time.sleep(0.1)
            pyautogui.press('enter')
        except Exception:
            pass

    def close_notepad(self) -> None:
        try:
            if self.notepad_win:
                self.notepad_win.close()
                time.sleep(0.2)
                self.handle_unexpected_dialogs()
        except Exception:
            pass


