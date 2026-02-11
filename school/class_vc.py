from __future__ import annotations

import discord
from discord.ext import commands

from school.config import load_school_config
from school.state import load_school_state, save_school_state


async def sync_class_voice_channels(bot) -> None:
    for guild in bot.guilds:
        state = load_school_state(guild.id)
        if not state.get("is_open"):
            continue
        block = state.get("block_index", -1)
        for user_id, channel_id in list(state.get("class_vcs", {}).items()):
            channel = guild.get_channel(int(channel_id))
            if channel is None:
                continue
            try:
                await channel.edit(name=f"class-{user_id}-block-{block}")
            except discord.HTTPException:
                continue


class ClassVC(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        config = load_school_config(guild.id)
        state = load_school_state(guild.id)
        lobby_id = config.get("channels", {}).get("class_category")
        if lobby_id is None:
            return
        category = guild.get_channel(int(lobby_id))
        if not isinstance(category, discord.CategoryChannel):
            return

        if after.channel and after.channel.category_id == category.id and str(member.id) not in state.get("class_vcs", {}):
            created = await guild.create_voice_channel(name=f"class-{member.id}", category=category)
            await member.move_to(created)
            state.setdefault("class_vcs", {})[str(member.id)] = created.id
            save_school_state(guild.id, state)

        if before.channel and before.channel.id in [int(x) for x in state.get("class_vcs", {}).values()]:
            if len(before.channel.members) == 0:
                await before.channel.delete(reason="Empty personal class VC")
                for uid, cid in list(state.get("class_vcs", {}).items()):
                    if int(cid) == before.channel.id:
                        state["class_vcs"].pop(uid, None)
                save_school_state(guild.id, state)


async def cleanup_class_vcs(guild: discord.Guild) -> None:
    state = load_school_state(guild.id)
    for channel_id in state.get("class_vcs", {}).values():
        channel = guild.get_channel(int(channel_id))
        if channel:
            await channel.delete(reason="School closed cleanup")
    state["class_vcs"] = {}
    save_school_state(guild.id, state)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClassVC())
