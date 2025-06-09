from typing import Final
from pathlib import Path


ROOT_DIR: Final[Path] = Path(__file__).parent.parent
env_file_path: Final[Path] = ROOT_DIR / ".env"
env_file_encoding: Final[str] = "utf-8"
