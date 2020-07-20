import discord
from discord.ext import commands


class Maincog(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, client, *, message):
        text = message
        await ctx.send(f"le message est **{text}** {ctx.message.author.mention}")

    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx, ammount=10):
        await ctx.channel.purge(limit=ammount + 1)

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        commandsList = {
            "status": "Retourne des info sur le serveur minecraft",
            "force_restart": "Kill le processus du serveur en cas de crash non resolvable depuis le apen admin ATTENTION : command a utliser en cas de probleme & réservé au administrateur ",
            "send_command": "Permet d'envoyer des commandes au server INFO : commande non disponible & réservé au administrateur",
        }
        embed = discord.Embed(description="Prefix : `frados/`", color=0x2B2B2B)
        embed.set_author(name="Liste des commandes Frados", icon_url="https://cdn.discordapp.com/attachments/713841107875659827/734751097377390592/server-icon.png")
        embed.add_field(name="Commandes : ", value="".join(f"**{i}** : `{commandsList[i]}`\n\n" for i in commandsList), inline=False)
        embed.set_footer(text="shibaeo.xyz - Frados")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Maincog(client))
