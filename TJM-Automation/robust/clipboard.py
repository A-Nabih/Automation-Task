import logging
import pyperclip


class ClipboardManager:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def set_text(self, text: str) -> bool:
        try:
            pyperclip.copy(text)
            return True
        except Exception as exc:
            self.logger.warning(f"Clipboard set failed: {exc}")
            return False

    def get_text(self) -> str:
        try:
            return pyperclip.paste()
        except Exception as exc:
            self.logger.warning(f"Clipboard get failed: {exc}")
            return ''


