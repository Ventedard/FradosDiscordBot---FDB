from discord.ext import commands
import psutil
from mcipc.query import Client
import socket
import discord
import unicodedata


class mcServer(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.command()
    async def status(self, ctx):
        await ctx.message.delete()
        splitter = " "

        # Trouver le pid du server
        """with open("C:\\AA_App\\crafty\\crafty\\logs\\crafty.log", mode="r") as f:
            pidList = []
            a = f.readlines()
            for i in a:
                if "PID" in i:
                    pidList.append(i)
                    lastPid = pidList[len(pidList) - 1].split(" ")
                    lastPidIndex = lastPid.index("PID")

                    pid = int(lastPid[lastPidIndex + 1])
                    print(pid)
                    print(pidList)"""
        PROCNAME = "python.exe"

        for proc in psutil.process_iter():
            if "java.exe" in proc.name():
                pid = proc.pid
        # Conditions qui check si le process du server est en route
        try:
            processState = psutil.Process(pid).status()
            cpuUsage = f"{psutil.cpu_percent(interval=0.1)} %"
            memUsage = f"{round(psutil.Process(pid).memory_full_info().uss / 1000000, 2)} mb"
        except:
            processState = "failed"
            cpuUsage = "failed"
            memUsage = "failed"
        # connection querry au serveur
        try:
            with Client("192.168.1.35", 25565, timeout=1.5) as mClient:
                full_stats = mClient.full_stats

                # plugin
                pluginList = []
                for i in range(len(full_stats[6]["Paper on Bukkit 1.16.1-R0.1-SNAPSHOT"])):
                    pluginList.append(full_stats[6]["Paper on Bukkit 1.16.1-R0.1-SNAPSHOT"][i])

                # Player
                playerList = []
                for i in range(len(full_stats[12])):
                    playerList.append(full_stats[12][i])

                # autre info
                serverVersion = full_stats[5]
                serverPort = full_stats[10]
                currentPlayer = full_stats[8]
                maxPlayer = full_stats[9]

                embed = discord.Embed(color=0xFF007D)
                embed.set_author(name="Frados server :", icon_url="https://cdn.discordapp.com/attachments/713841107875659827/734751097377390592/server-icon.png")
                embed.add_field(
                    name="Minecraft : ",
                    value=f"Proccess : ***{processState}***\n Mem Usage : ***{memUsage}***\n CPU Usage : ***{cpuUsage}***\n Version server : ***{serverVersion}***\n Port : ***{serverPort}***\n Nombre joueurs : ***{currentPlayer}/{maxPlayer}***\n Joueurs connectés : {''.join(f'***   {i}  *** ' for i in playerList)}\n Plugins : {''.join(f'`{i.split(splitter)[0]}` ' for i in pluginList)}",
                    inline=False,
                )
                embed.set_footer(text="shibaeo.xyz - Frados")
                await ctx.send(embed=embed)
        except socket.timeout as timeout:
            embed = discord.Embed(color=0xFF007D)
            embed.set_author(name="Frados server :", icon_url="https://cdn.discordapp.com/attachments/713841107875659827/734751097377390592/server-icon.png")
            embed.add_field(name="Minecraft : ", value=f"Proccess : ***{processState}***\n Status server : ***{timeout} / Stopped***", inline=False)
            embed.set_footer(text="shibaeo.xyz - Frados")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_role(734795725027672116)
    async def force_restart(self, ctx):
        await ctx.message.delete()
        # Trouver le pid du server
        """with open("C:\\AA_App\\crafty\\crafty\\logs\\crafty.log", mode="r") as f:
            pidList = []
            a = f.readlines()
            for i in a:
                if "PID" in i:
                    pidList.append(i)
                    lastPid = pidList[len(pidList) - 1].split(" ")
                    lastPidIndex = lastPid.index("PID")

                    pid = int(lastPid[lastPidIndex + 1])
                    print(pid)"""
        for proc in psutil.process_iter():
            if "java.exe" in proc.name():
                pid = proc.pid

        # Conditions qui check si le process du server est en route
        try:
            psutil.Process(pid).terminate()
            await ctx.send((f"""```css\nProcess killed ({pid})```"""))
        except psutil.AccessDenied:
            await ctx.send((f"""```fix\nErreur : psutil.AccessDenied : ({pid})```"""))
        except psutil.NoSuchProcess:
            await ctx.send((f"""```fix\nErreur : psutil.NoSuchProces ({pid})```"""))

    @commands.command()
    @commands.has_role(734795725027672116)
    async def send_command(self, ctx, *, message):
        await ctx.message.delete()
        from mcipc.rcon import Client

        try:
            with Client("192.168.1.35", 25575) as client:
                client.login("")

                if message.startswith("/"):
                    message.replace("/", "")
                client.run(message)
        except socket.timeout as timeout:
            await ctx.send(timeout)

    @commands.command()
    async def send_message(self, ctx, *, message):
        await ctx.message.delete()
        from mcipc.rcon import Client

        try:
            with Client("192.168.1.35", 25575, timeout=1.5) as client:
                client.login("")
                msg = unicodedata.normalize("NFKD", message).encode("ASCII", "ignore").decode("utf-8")
                author = unicodedata.normalize("NFKD", ctx.message.author.name).encode("ASCII", "ignore").decode("utf-8")
                client.me(f"§9[Discord]§c[{author}]§f {str(msg)}")
        except socket.timeout as timeout:
            await ctx.send(timeout)


def setup(client):
    client.add_cog(mcServer(client))
