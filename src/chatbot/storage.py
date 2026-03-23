from __future__ import annotations

import json
from pathlib import Path
from typing import List

#history saving class
class JSONStorage:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load_history(self) -> List[str]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

        if isinstance(data, list):
            return [str(item) for item in data]
        return []

    def save_history(self, history: List[str]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)
