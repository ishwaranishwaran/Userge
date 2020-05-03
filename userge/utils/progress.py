# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import time
from math import floor

from pyrogram.errors.exceptions import FloodWait

import userge
from .tools import humanbytes, time_formatter


async def progress(current: int,
                   total: int,
                   ud_type: str,
                   client: 'userge.Userge',
                   message: 'userge.Message',
                   start: int) -> None:
    if message.process_is_canceled:
        await client.stop_transmission()
    now = time.time()
    diff = now - start
    if diff % 10 < 0.25 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        time_to_completion = time_formatter(int((total - current) / speed))
        progress_str = \
            "__{}__\n" + \
            "```[{}{}]```\n" + \
            "**Progress** : `{}%`\n" + \
            "**Completed** : `{}`\n" + \
            "**Total** : `{}`\n" + \
            "**Speed** : `{}/s`\n" + \
            "**ETA** : `{}`"
        progress_str = progress_str.format(
            ud_type,
            ''.join(["█" for i in range(floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - floor(percentage / 5))]),
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            time_to_completion if time_to_completion else "0 s")
        if message.text != progress_str:
            try:
                await message.edit(progress_str)
            except FloodWait as f_e:
                time.sleep(f_e.x)
