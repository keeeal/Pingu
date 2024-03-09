from __future__ import annotations

from typing import TYPE_CHECKING

from discord import Interaction
from discord.app_commands import command
from discord.ext.commands import Cog

if TYPE_CHECKING:
    from pingu.bot import Pingu


class Commands(Cog):
    def __init__(self, bot: Pingu):
        self.bot = bot

    @command(name="noot", description="Report on this channel")
    async def list(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        await interaction.channel.send(
            embed=await self.bot.embed(channel=interaction.channel)
        )
        await interaction.delete_original_response()
