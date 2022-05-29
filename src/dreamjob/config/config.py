import os
from pathlib import Path

THIS_DIR = Path(__file__).resolve(strict=True).parent
ROOT_DIR = THIS_DIR.parent.parent.parent
LOG_DIR = os.environ.get("RECSYS_LOG_DIR", ROOT_DIR / "log")
