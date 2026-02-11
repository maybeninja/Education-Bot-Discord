from __future__ import annotations

from school.state import load_school_state, save_school_state


def get_library_sessions(guild_id: int) -> dict:
    state = load_school_state(guild_id)
    return state.get("library_sessions", {})


def upsert_library_session(guild_id: int, user_id: int, channel_id: int | None = None) -> None:
    state = load_school_state(guild_id)
    sessions = state.setdefault("library_sessions", {})
    entry = sessions.setdefault(str(user_id), {})
    if channel_id is not None:
        entry["channel_id"] = channel_id
    save_school_state(guild_id, state)


def remove_library_session(guild_id: int, user_id: int) -> None:
    state = load_school_state(guild_id)
    state.setdefault("library_sessions", {}).pop(str(user_id), None)
    save_school_state(guild_id, state)
