import discord
from discord.ext import commands
import random
import asyncio
import datetime
import time
import traceback
import sys
import aiohttp

startTime = datetime.datetime.now()

class Info:
    """Info Commands"""
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.command(aliases=['si', 'sinfo'])
    async def serverinfo(self, ctx):
        """Get some Server info!"""
        guild = None
        if guild_name == None:
            guild = ctx.guild
        else:
            for g in self.bot.guilds:
                if g.name.lower() == guild_name.lower():
                    guild = g
                    break
                if str(g.id) == str(guild_name):
                    guild = g
                    break
        if guild == None:
            # We didn't find it
            await ctx.send("I couldn't find that guild...")
            return
        
        server_embed = discord.Embed(color=ctx.author.color)
        server_embed.title = guild.name
        server_embed.description = "Some server stats"
        online_members = 0
        bot_member     = 0
        bot_online     = 0
        for member in guild.members:
            if member.bot:
                bot_member += 1
                if not member.status == discord.Status.offline:
                        bot_online += 1
                continue
            if not member.status == discord.Status.offline:
                online_members += 1
        # bot_percent = "{:,g}%".format((bot_member/len(guild.members))*100)
        user_string = "{:,}/{:,} online ({:,g}%)".format(
                online_members,
                len(guild.members) - bot_member,
                round((online_members/(len(guild.members) - bot_member) * 100), 2)
        )
        b_string = "bot" if bot_member == 1 else "bots"
        user_string += "\n{:,}/{:,} {} online ({:,g}%)".format(
                bot_online,
                bot_member,
                b_string,
                round((bot_online/bot_member)*100, 2)
        )
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = f"Server created on {guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
        color = discord.Color.green()
        roles = [x.name for x in guild.roles]
        role_length = len(roles)
        roles = ', '.join(roles)
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        try:
            ban_count = len(await guild.bans())
        except discord.Forbidden:
            ban_count = "Kala Lacks the `ban members` permission. (In order to retrieve bans)"
        verification_levels = {
            0: "**None** No Security measures have been taken.",
            1: "**Low** Light Security measures have been taken. (Verified Email)",
            2: "**Moderate** Moderate Security measures have been taken. (Registered on Discord for longer than 5 minutes)",
            3: "**High** High Security measures have been taken. (Member of server for longer than 10 minutes)",
            4: "**Fort Knox** Almost inpenetrable Security measures have been taken. (Verified Phone)"
        }
        content_filter = {
            0: "**None** No Scanning enabled. (Don't scan any messages.)",
            1: "**Moderate** Moderate Scanning enabled. (Scan messages from members without a role.)",
            2: "**High** High Scanning enabled. (Scans every message.)"
        }
        mfa_levels = {
            0: "Does not require 2FA for members with Admin permission.",
            1: "Requires 2FA for members with Admin permission."
        }
        regular_emojis = len([x for x in guild.emojis if not x.animated])
        animated_emojis = len([x for x in guild.emojis if x.animated])
        textchannels = guild.text_channels
        voicechannels = guild.voice_channels
        
        server_embed.set_thumbnail(url=guild.icon_url)
        server_embed.add_field(name='Server ID', value=str(guild.id))
        server_embed.add_field(name='Owner', value=guild.owner.name + "#" + guild.owner.discriminator)
        server_embed.add_field(name='Members ({:,} total)'.format(len(guild.members), value=user_string)
        server_embed.add_field(name="AFK Channel & Time:", value = f"Channel: **{guild.afk_channel}**" "Time: **{} minutes**".format(int(guild.afk_timeout / 60)))
        server_embed.add_field(name='Emoji Count', value=regular_emojis + animated_emojis)
        server_embed.add_field(name='Normal Emojis', value=regular_emojis)
        server_embed.add_field(name='Animated Emojis', value=animated_emojis)
        server_embed.add_field(name='Server Region', value=str(guild.region))
        server_embed.add_field(name='Roles', value=str(len(guild.roles))
        server_embed.add_field(name='Default Role', value=guild.default_role)
        server_embed.add_field(name='Considered Large', value=guild.large)                
        server_embed.add_field(name='Server Verification Level', value=verification_levels[guild.verification_level])
        server_embed.add_field(name='Explicit Content Filter', value=content_filter[guild.explicit_content_filter])
        server_embed.add_field(name='2FA Requirement', value=mfa_levels[guild.mfa_level])
        server_embed.add_field(name='Ban Count', value=ban_count)
        server_embed.set_footer(text='Created - %s' % time)
        joinedList = []
        popList    = []
        for g in self.bot.guilds:
            joinedList.append({ 'ID' : g.id, 'Joined' : g.me.joined_at })
            popList.append({ 'ID' : g.id, 'Population' : len(g.members) })
        
        # sort the guilds by join date
        joinedList = sorted(joinedList, key=lambda x:x['Joined'])
        popList = sorted(popList, key=lambda x:x['Population'], reverse=True)
        
        check_item = { "ID" : guild.id, "Joined" : guild.me.joined_at }
        total = len(joinedList)
        position = joinedList.index(check_item) + 1
        server_embed.add_field(name="Join Position", value="{:,} of {:,}".format(position, total), inline=True)
        
        # Get our population position
        check_item = { "ID" : guild.id, "Population" : len(guild.members) }
        total = len(popList)
        position = popList.index(check_item) + 1
        server_embed.add_field(name="Population Rank", value="{:,} of {:,}".format(position, total), inline=True)
        
        emojitext = ""
        emojicount = 0
        for emoji in guild.emojis:
            if emoji.animated:
                emojiMention = "<a:"+emoji.name+":"+str(emoji.id)+">"
            else:
                emojiMention = "<:"+emoji.name+":"+str(emoji.id)+">"
            test = emojitext + emojiMention
            if len(test) > 1024:
                # TOOO BIIIIIIIIG
                emojicount += 1
                if emojicount == 1:
                    ename = "Emojis ({:,} total)".format(len(guild.emojis))
                else:
                    ename = "Emojis (Continued)"
                server_embed.add_field(name=ename, value=emojitext, inline=True)
                emojitext=emojiMention
            else:
                emojitext = emojitext + emojiMention

        if len(emojitext):
            if emojicount == 0:
                emojiname = "Emojis ({} total)".format(len(guild.emojis))
            else:
                emojiname = "Emojis (Continued)"
            server_embed.add_field(name=emojiname, value=emojitext, inline=True)


        if len(guild.icon_url):
            server_embed.set_thumbnail(url=guild.icon_url)
        else:
            # No Icon
            server_embed.set_thumbnail(url=ctx.author.default_avatar_url)
        server_embed.set_footer(text="Server ID: {}".format(guild.id))
        
        await ctx.send(embed=server_embed)


    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        '''Get user info for yourself or someone in the guild'''
        if user is None:
            user = ctx.author
        color = discord.Color.green()
        guild = ctx.message.guild
        roles = sorted(user.roles, key=lambda r: r.position)
        rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
        shared = sum(1 for m in self.bot.get_all_members() if m.id == user.id)
        highrole = user.top_role.name
        if highrole == "@everyone":
            role = "N/A"

        if user.avatar_url[54:].startswith('a_'):
            avi = 'https://cdn.discordapp.com/avatars/' + user.avatar_url[35:-10]
        else:
            avi = user.avatar_url

        
        time = ctx.message.created_at
        desc = f'{user.name} is currently in {user.status} mode.'
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(color=color, description=desc, timestamp=time)
        em.add_field(name=f'{self.bot.get_emoji(430850541959118880)} Username', value=f'{user.name}#{user.discriminator}')
        em.add_field(name=f'{self.bot.get_emoji(450882580716453888)} User ID', value= user.id)
        em.add_field(name=f'{self.bot.get_emoji(450867126639788038)} Servers Shared', value=f'{shared}')
        em.add_field(name=f'{self.bot.get_emoji(433736508038578179)} Highest Role', value=highrole)
        
        em.add_field(name=f'{self.bot.get_emoji(450878488736432128)} Account Created At', value = user.created_at.__format__('Date: **%d/%b/%Y**\nTime: **%H:%M:%S**'))
        em.add_field(name=f'{self.bot.get_emoji(432191587850780682)} Member Number', value=member_number)
        em.add_field(name=f'{self.bot.get_emoji(393514807371890688)} Joined At', value=user.joined_at.__format__('%d/%b/%Y at %H:%M:%S'))
        em.add_field(name=f'{self.bot.get_emoji(449683164110127104)} Roles', value=rolenames)
        em.set_footer(text = f"Member since: {user.joined_at.__format__('%d/%b/%Y at %H:%M:%S')}")
        em.set_thumbnail(url=avi or None)
        await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        # Gets the current uptime for the bot
        timedifference_seconds = (datetime.datetime.now().second - startTime.second)
        timedifference_minutes = (datetime.datetime.now().minute - startTime.minute)
        timedifference_hours = (datetime.datetime.now().hour - startTime.hour)
        old_timedifference = (datetime.datetime.now() - startTime)
        print("I have been up for {0} hours, {1} minutes, and {2} seconds".format(timedifference_hours, timedifference_minutes, timedifference_seconds))
        await ctx.send("I have been up for {}".format(old_timedifference))

    @commands.command(aliases=['kalastats'])
    async def kala(self, ctx):
        """Get some bot stats about me!"""
        member = 0
        for i in self.bot.guilds:
            for x in i.members:
                member += 1
        color = discord.Color(value=0xe212d1)
        embed = discord.Embed(color=color, title="Kala Bot Statistics")
        embed.description = "Kala#6605 Stats"
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/449682597937807363/450339949384826880/asdf.png")
        embed.add_field(name=f"{self.bot.get_emoji(449682671862546443)} Creator", value=f'BloodyPikachu#0638 {self.bot.get_emoji(449682671862546443)}')
        embed.add_field(name=f"{self.bot.get_emoji(450791022541406209)} Servers", value=f"{len(self.bot.guilds)}")
        embed.add_field(name=f'{self.bot.get_emoji(450791226459815936)} Users', value=member)
        embed.add_field(name=f'{self.bot.get_emoji(412747044403544074)} Ping', value=f'{self.bot.latency * 100:.4f} ms')
        embed.add_field(name=f'{self.bot.get_emoji(439557226969956363)} Version', value='0.0.2')
        embed.add_field(name=f'{self.bot.get_emoji(424265677642268676)} Start Date', value="5/27/18")
        embed.add_field(name=f'{self.bot.get_emoji(422527903658672148)} Coding Language', value=f'{self.bot.get_emoji(418934774623764491)} Python, discord.py rewrite')
        await ctx.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Info(bot))
