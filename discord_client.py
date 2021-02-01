#!/usr/bin/env python3

import json
from datetime import datetime
from discord.ext import commands
import discord
from get_file import rdm
import os
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# read our environment variables
with open("./env.json", "r") as env:
    ENV = json.load(env)


COMMAND_RESET = ENV["command_reset"]
COMMAND_ROLL_INITIATIVE = ENV["command_initiative"]
COMMAND_REMOVE_INITIATIVE = ENV["command_remove_initiative"]

COMMAND_CHAR = ENV['command_char']  # Command used to activate bot on discord


COLORS = {
    "BLACK": "\033[30m",
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[33m",
    "BLUE": "\033[34m",
    "PURPLE": "\033[35m",
    "CYAN": "\033[36m",
    "GREY": "\033[37m",
    "WHITE": "\033[38m",
    "NEUTRAL": "\033[00m"
}

SIGN = (
    COLORS["RED"] + "/" +
    COLORS["YELLOW"] + "!" +
    COLORS["RED"] + "\\" +
    COLORS["NEUTRAL"] +
    " "
)


class InitItem():
    def __init__(self, name, value, dex=0):
        self.name = name
        self.value = value
        self.dex = dex
        self.total = value + dex


class InitTable():

    initiative_table = []

    def add(self, name, value, dex=0):
        self.initiative_table.append(InitItem(name, value, dex))
        self.initiative_table = sorted(self.initiative_table, key=lambda x: x.total, reverse=True)

    def reset(self):
        self.initiative_table = []

    async def remove_index(self, context, index):
        self.initiative_table.remove(self.initiative_table[index-1])
        await self.show(context)

    async def show(self, context):
        text = "```"
        for i, item in enumerate(self.initiative_table):
            text += f"{i+1}: {item.name} [{item.value}] + {item.dex} = Total: {item.total}\n"
        text += "```"
        await context.send(text)

init_items = InitTable()

# read our discord acces token
with open("secrets.json", "r") as secrets:
    DISCORD_TOKEN = json.load(secrets)["discord"]

bot = commands.Bot(
    command_prefix=COMMAND_CHAR,
    description="Roll a random initiative, store and sort"
)


# COMMANDS ================
@bot.command(
    name=COMMAND_RESET,
    description="Reset the initiative table"
)
async def roll_reset_initiative(context):
    init_items.reset()
    await context.send("OK, limpei a tabela. Bons dados :)")


@bot.command(
    name=COMMAND_REMOVE_INITIATIVE,
    description="Remove item from table"
)
async def remove_initiative(context, index=0):
    await init_items.remove_index(context, index)


@bot.command(
    name=COMMAND_ROLL_INITIATIVE,
    description="Send an help for critical command!"
)
async def roll_initiative(context, dex="", name_arg=""):
    try:
        if not dex:
            await init_items.show(context)
            return
        dex = int(dex)
        name = name_arg if name_arg else context.message.author.display_name

        init_items.add(name, random.randint(1, 20), dex)
        await init_items.show(context)

    except Exception as e:
        await context.send(f"Digite um numero (normalmente sua destreza). {dex} não é válido... ")
        await context.send(f"Exception {e}")
                

@bot.event
async def on_ready():
    print(
        COLORS["YELLOW"] +
        "I'm logged in as {name} !\n".format(name=bot.user.name) +
        COLORS["NEUTRAL"]
    )


bot.run(DISCORD_TOKEN)
