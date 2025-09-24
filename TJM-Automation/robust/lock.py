import os
import logging
from pathlib import Path


class InstanceLock:
    def __init__(self, lockfile: Path, logger: logging.Logger):
        self.lockfile = lockfile
        self.logger = logger
        self._acquired = False

    def acquire(self) -> bool:
        try:
            self.lockfile.parent.mkdir(parents=True, exist_ok=True)
            fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(str(os.getpid()))
            self._acquired = True
            self.logger.info(f"Acquired instance lock at {self.lockfile}")
            return True
        except FileExistsError:
            try:
                pid_text = self.lockfile.read_text(encoding='utf-8', errors='ignore').strip()
                existing_pid = int(pid_text) if pid_text.isdigit() else None
            except Exception:
                existing_pid = None
            self.logger.error(f"Another instance appears to be running (lock: {self.lockfile}, pid={existing_pid}).")
            return False
        except Exception as exc:
            self.logger.error(f"Failed to acquire lock: {exc}")
            return False

    def release(self) -> None:
        if self._acquired:
            try:
                self.lockfile.unlink(missing_ok=True)
                self.logger.info("Released instance lock")
            except Exception as exc:
                self.logger.warning(f"Failed to release lock: {exc}")
            finally:
                self._acquired = False


