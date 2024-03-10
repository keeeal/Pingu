from __future__ import annotations

from datetime import datetime, timezone
from functools import partial
from typing import Optional, Union

from discord import Embed, Intents, Thread
from discord.abc import GuildChannel
from discord.ext.commands import Bot
from tqdm import tqdm

from pingu.commands import Commands
from pingu.utils.logging import get_logger

logger = get_logger(__name__)


class Pingu(Bot):
    def __init__(self, command_prefix: str) -> None:
        super().__init__(command_prefix, intents=Intents.default())

    async def embed(
        self, channel: Union[GuildChannel, Thread], max_pins: int = 50
    ) -> str:
        if channel.created_at is None:
            raise ValueError

        pins = await channel.pins()
        _format_meter = partial(
            tqdm.format_meter,
            len(pins),
            total=max_pins,
            elapsed=(
                (datetime.now(timezone.utc) - channel.created_at).total_seconds()
                if pins
                else 0
            ),
        )

        embed = (
            Embed(title=None if len(pins) < max_pins else "⚠️🚨🚧 FULL PINS 🚧🚨⚠️")
            .add_field(
                name="📌",
                value="",
            )
            .add_field(
                name=f"{len(pins)} pin{'' if len(pins) == 1 else 's'} in {channel.name}",
                value=_format_meter(
                    bar_format="`[{bar}] {percentage:.0f}%`",
                    ascii="-#",
                    ncols=35,
                ),
            )
        )
        if pins:
            embed.add_field(
                name="full pins",
                value=_format_meter(bar_format="`{eta:%d %b %Y}`"),
            )

        return embed

    async def on_ready(self) -> None:
        await self.add_cog(Commands(bot=self))
        await self.tree.sync()
        logger.info(f"Logged in as {self.user}")

    async def on_guild_channel_pins_update(
        self, channel: Union[GuildChannel, Thread], last_pin: Optional[datetime]
    ) -> None:
        await channel.send(embed=await self.embed(channel))
