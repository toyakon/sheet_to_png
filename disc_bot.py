import os

import discord
from discord.ext import commands

import sheet_to_png

token = os.getenv("DISCORD_TOKEN")
SHEET_URL = os.getenv("SHEET_URL")

bot = commands.Bot(command_prefix="/")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def sheet(ctx, start, end):
    sti = sheet_to_png.SheetToPng(SHEET_URL)
    img = sti.sheet_to_png(start, end)
    await ctx.send(file=discord.File(img, "sheet.png"))

bot.run(token)
