from __future__ import annotations

import discord

from school.config import load_school_config
from school.state import load_school_state


async def update_status(bot, guild: discord.Guild) -> None:
    config = load_school_config(guild.id)
    state = load_school_state(guild.id)
    stage_id = config.get("channels", {}).get("status_stage")
    if stage_id:
        stage = guild.get_channel(int(stage_id))
        if isinstance(stage, discord.StageChannel):
            status = "School Open" if state.get("is_open") else "School Closed"
            try:
                await stage.edit(topic=f"{status} | Block: {state.get('block_index', -1)}")
            except discord.HTTPException:
                pass
    activity = discord.Game(name="School Open" if state.get("is_open") else "School Closed")
    await bot.change_presence(activity=activity)


async def refresh_all_status_channels(bot) -> None:
    for guild in bot.guilds:
        await update_status(bot, guild)
