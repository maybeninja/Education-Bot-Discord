from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GUILDS_DIR = DATA_DIR / "guilds"
USERS_DIR = DATA_DIR / "users"
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

for directory in (DATA_DIR, GUILDS_DIR, USERS_DIR):
    directory.mkdir(parents=True, exist_ok=True)
