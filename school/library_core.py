from __future__ import annotations

import discord
from discord.ext import commands

from school.config import load_school_config
from school.library_state import remove_library_session, upsert_library_session


class LibraryVC(commands.Cog):
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = member.guild
        config = load_school_config(guild.id)
        lobby_id = config.get("channels", {}).get("library_lobby")
        class_category_id = config.get("channels", {}).get("class_category")
        if not lobby_id or not class_category_id:
            return

        if after.channel and after.channel.id == int(lobby_id):
            category = guild.get_channel(int(class_category_id))
            if isinstance(category, discord.CategoryChannel):
                room = await guild.create_voice_channel(name=f"library-{member.display_name}", category=category)
                await member.move_to(room)
                upsert_library_session(guild.id, member.id, room.id)

        if before.channel and before.channel.name.startswith("library-") and len(before.channel.members) == 0:
            await before.channel.delete(reason="Cleanup empty library VC")
            remove_library_session(guild.id, member.id)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(LibraryVC())
