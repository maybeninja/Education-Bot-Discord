from __future__ import annotations

from core.time_utils import now_ist
from school.library_state import get_library_sessions, remove_library_session


async def run_library_cleanup(bot) -> None:
    for guild in bot.guilds:
        sessions = get_library_sessions(guild.id)
        for user_id, session in list(sessions.items()):
            channel = guild.get_channel(int(session.get("channel_id", 0)))
            if channel is None:
                remove_library_session(guild.id, int(user_id))
                continue
            if len(getattr(channel, "members", [])) == 0:
                await channel.delete(reason=f"Stale cleanup {now_ist().date().isoformat()}")
                remove_library_session(guild.id, int(user_id))
