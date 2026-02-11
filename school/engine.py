from __future__ import annotations

from datetime import time

from core.time_utils import now_ist
from school.bell import announce_block
from school.config import load_school_config
from school.state import load_school_state, save_school_state


def _hhmm_to_time(hhmm: str) -> time:
    h, m = hhmm.split(":")
    return time(hour=int(h), minute=int(m))


def should_advance_block(config: dict, state: dict) -> int:
    current = now_ist().time()
    for idx, block in enumerate(config.get("periods", [])):
        if _hhmm_to_time(block["start"]) <= current < _hhmm_to_time(block["end"]):
            return idx
    return -1


async def advance_block(guild, config: dict, state: dict, new_index: int) -> None:
    state["block_index"] = new_index
    period_key = config["periods"][new_index]["name"] if new_index >= 0 else "After School"
    if state.get("last_period_key") != period_key:
        await announce_block(guild, config, period_key)
        state["last_period_key"] = period_key


async def process_period_transitions(bot) -> None:
    for guild in bot.guilds:
        config = load_school_config(guild.id)
        state = load_school_state(guild.id)
        if not state.get("is_open"):
            continue
        new_index = should_advance_block(config, state)
        if new_index != state.get("block_index", -1):
            await advance_block(guild, config, state, new_index)
            save_school_state(guild.id, state)
