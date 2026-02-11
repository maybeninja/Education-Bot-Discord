from __future__ import annotations

import discord


async def announce_block(guild: discord.Guild, config: dict, block_name: str) -> None:
    bell_channel_id = config.get("channels", {}).get("bell")
    if not bell_channel_id:
        return
    channel = guild.get_channel(int(bell_channel_id))
    if channel is None:
        return
    await channel.send(f"🔔 **{block_name}** is now active.")
