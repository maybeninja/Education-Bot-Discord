from __future__ import annotations

from pathlib import Path

from core.config import GUILDS_DIR
from core.json_store import load_json, save_json

DEFAULT_SCHOOL_STATE = {
    "is_open": False,
    "block_index": -1,
    "library_open": True,
    "class_vcs": {},
    "library_sessions": {},
    "last_period_key": "",
}


def _state_path(guild_id: int) -> Path:
    return GUILDS_DIR / str(guild_id) / "school_state.json"


def load_school_state(guild_id: int) -> dict:
    state = load_json(_state_path(guild_id), DEFAULT_SCHOOL_STATE.copy())
    for k, v in DEFAULT_SCHOOL_STATE.items():
        state.setdefault(k, v)
    return state


def save_school_state(guild_id: int, payload: dict) -> None:
    save_json(_state_path(guild_id), payload)
