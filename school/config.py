from __future__ import annotations

from pathlib import Path

from core.config import GUILDS_DIR
from core.json_store import load_json, save_json

DEFAULT_GUILD_CONFIG = {
    "channels": {
        "bell": None,
        "class_category": None,
        "status_stage": None,
        "attendance_channel": None,
        "library_lobby": None,
    },
    "periods": [
        {"name": "Period 1", "start": "09:00", "end": "09:45", "type": "period"},
        {"name": "Short Break", "start": "09:45", "end": "10:00", "type": "break"},
        {"name": "Period 2", "start": "10:00", "end": "10:45", "type": "period"},
        {"name": "Lunch", "start": "12:30", "end": "13:00", "type": "lunch"},
    ],
}


def _config_path(guild_id: int) -> Path:
    return GUILDS_DIR / str(guild_id) / "school_config.json"


def load_school_config(guild_id: int) -> dict:
    payload = load_json(_config_path(guild_id), DEFAULT_GUILD_CONFIG.copy())
    return payload


def save_school_config(guild_id: int, payload: dict) -> None:
    save_json(_config_path(guild_id), payload)
