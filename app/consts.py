from pathlib import Path
from typing import Final

ROOT_DIR: Final[Path] = Path(__file__).parent.parent
env_file_path: Final[Path] = ROOT_DIR / ".env"
env_file_encoding: Final[str] = "utf-8"
