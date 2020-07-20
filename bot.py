import discord
import os
from discord.ext import commands
import json

client = commands.Bot(command_prefix="frados/")

client.remove_command("help")
with open("config.json", mode="r") as b:
    c = json.load(b)
    token = c["discord"]["botToken"]


@client.event
async def on_ready():
    print("bot ready")
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game(name="🌴 Frados le bête de server !!"),
    )


@client.command()
@commands.is_owner()
async def cogs_load(ctx, extension):
    try:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f"""```CSS\ncogs.{extension} Loaded```""")
    except:
        await ctx.send(f"""```fix\ncogs.{extension} not found```""")


@client.command()
@commands.is_owner()
async def cogs_unload(ctx, extension):
    try:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"""```CSS\ncogs.{extension} Unloaded```""")
    except:
        await ctx.send(f"""```fix\ncogs.{extension} not found```""")


@client.command()
@commands.is_owner()
async def cogs_reload(ctx, extension):
    try:
        client.reload_extension(f"cogs.{extension}")
        await ctx.send(f"""```CSS\ncogs.{extension} Reloaded```""")
    except:
        await ctx.send(f"""```fix\ncogs.{extension} not found```""")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


@client.command()
@commands.is_owner()
async def cogs_list(ctx):
    cogs = []
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cogs.append(filename[:-3])
    embed = discord.Embed(color=0xFF007D)
    embed.add_field(name="Cogs : ", value="".join(f"`{i}` " for i in cogs), inline=False)
    embed.set_footer(text="shibaeo.xyz - Frados")
    await ctx.send(embed=embed)


client.run(token)
