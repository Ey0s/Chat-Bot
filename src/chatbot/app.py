from __future__ import annotations

from pathlib import Path

import customtkinter as ctk

from .bot import ChatBot
from .storage import JSONStorage
from .ui import ChatApp

#data path
def resolve_data_paths(project_root: Path) -> tuple[Path, Path]:
    responses_path = project_root / "data" / "responses.json"
    legacy_responses_path = project_root / "responses.json"

    if not responses_path.exists() and legacy_responses_path.exists():
        responses_path = legacy_responses_path

    history_path = project_root / "data" / "history.json"
    return responses_path, history_path


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    responses_path, history_path = resolve_data_paths(project_root)

    chatbot = ChatBot(responses_path, creator_name="Eyosyas")
    storage = JSONStorage(history_path)

    root = ctk.CTk()
    ChatApp(root, chatbot, storage)
    root.mainloop()


if __name__ == "__main__":
    main()
