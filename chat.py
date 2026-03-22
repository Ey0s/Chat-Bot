from pathlib import Path
import sys


def main() -> None:
    project_root = Path(__file__).resolve().parent
    src_path = project_root / "src"

    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from chatbot.app import main as run_app

    run_app()


if __name__ == "__main__":
    main()
