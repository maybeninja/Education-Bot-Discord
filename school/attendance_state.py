from __future__ import annotations

from pathlib import Path

from core.config import GUILDS_DIR
from core.json_store import load_json, save_json
from core.time_utils import now_ist
from school.config import load_school_config


def _attendance_path(guild_id: int) -> Path:
    return GUILDS_DIR / str(guild_id) / "attendance.json"


def _default_attendance() -> dict:
    return {"is_open": False, "present_users": [], "opened_at": None, "closed_at": None}


def load_attendance(guild_id: int) -> dict:
    payload = load_json(_attendance_path(guild_id), _default_attendance())
    for k, v in _default_attendance().items():
        payload.setdefault(k, v)
    return payload


def save_attendance(guild_id: int, payload: dict) -> None:
    save_json(_attendance_path(guild_id), payload)


def open_attendance(guild_id: int) -> dict:
    payload = load_attendance(guild_id)
    payload.update({"is_open": True, "opened_at": now_ist().isoformat(), "present_users": []})
    save_attendance(guild_id, payload)
    return payload


def mark_attendance(guild_id: int, user_id: int) -> bool:
    payload = load_attendance(guild_id)
    if not payload.get("is_open"):
        return False
    uid = str(user_id)
    if uid not in payload["present_users"]:
        payload["present_users"].append(uid)
        save_attendance(guild_id, payload)
        return True
    return False


def close_attendance(guild_id: int) -> dict:
    payload = load_attendance(guild_id)
    payload["is_open"] = False
    payload["closed_at"] = now_ist().isoformat()
    save_attendance(guild_id, payload)
    return payload


def get_attendance_stats(guild_id: int) -> dict:
    payload = load_attendance(guild_id)
    return {"status": "open" if payload.get("is_open") else "closed", "present": len(payload.get("present_users", []))}


async def process_attendance_windows(bot) -> None:
    now = now_ist().time()
    for guild in bot.guilds:
        config = load_school_config(guild.id)
        attendance = load_attendance(guild.id)
        periods = config.get("periods", [])
        first_start = periods[0]["start"] if periods else "09:00"
        h, m = [int(x) for x in first_start.split(":")]
        if now.hour == h and now.minute < m + 5 and not attendance.get("is_open"):
            open_attendance(guild.id)
        if now.hour == h and now.minute >= m + 10 and attendance.get("is_open"):
            close_attendance(guild.id)
