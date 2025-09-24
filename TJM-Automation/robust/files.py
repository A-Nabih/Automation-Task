import os
import shutil
import hashlib
import logging
from pathlib import Path
from typing import Optional


class FileManager:
    INVALID_CHARS = '<>:"/\\|?*'

    def __init__(self, output_dir: Path, conflict: str, logger: logging.Logger):
        self.output_dir = output_dir
        self.conflict = conflict
        self.logger = logger

    def ensure_output_dir(self) -> bool:
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            return os.access(self.output_dir, os.W_OK)
        except Exception as exc:
            self.logger.error(f"Cannot create/access output directory {self.output_dir}: {exc}")
            return False

    def has_enough_space(self, estimated_bytes: int = 1024) -> bool:
        try:
            total, used, free = shutil.disk_usage(self.output_dir)
            return free > max(estimated_bytes, 1024 * 1024)
        except Exception as exc:
            self.logger.warning(f"Failed to check disk space: {exc}")
            return True

    def sanitize_filename(self, name: str, extension: str) -> str:
        base = ''.join('_' if c in self.INVALID_CHARS else c for c in name).strip()
        if not base:
            base = 'untitled'
        base = base[:240]
        return f"{base}.{extension.strip('.')}"

    def resolve_conflict(self, filepath: Path) -> Optional[Path]:
        if not filepath.exists():
            return filepath
        if self.conflict == 'skip':
            self.logger.info(f"File exists; skipping: {filepath.name}")
            return None
        if self.conflict == 'overwrite':
            return filepath
        counter = 1
        while True:
            candidate = filepath.with_stem(f"{filepath.stem} ({counter})")
            if not candidate.exists():
                return candidate
            counter += 1

    def write_text(self, path: Path, content: str) -> bool:
        try:
            with open(path, 'w', encoding='utf-8', errors='replace') as f:
                f.write(content)
            return True
        except PermissionError as exc:
            self.logger.error(f"Permission denied writing {path}: {exc}")
            return False
        except OSError as exc:
            self.logger.error(f"Disk/IO error writing {path}: {exc}")
            return False

    @staticmethod
    def sha256_of_text(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8', errors='replace')).hexdigest()


