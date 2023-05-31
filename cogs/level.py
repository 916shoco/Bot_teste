from discord.ext import commands
import discord
import aiosqlite
import random
import asyncio


class level(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  async def on_ready(self, bot):
      setattr(bot, "db", await aiosqlite.connect("level.sql"))
      await asyncio.sleep(3)
      async with bot.db.cursor() as cursor:
          await cursor.execute("CREATE A TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")

  async def on_message(self, message, bot):
      if message.author.bot:
         return
      author = message.author
      guild = message.guild
      async with bot.db.cursor() as cursor:
          await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
          xp = await cursor.fetchone()
          await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?." (author.id, guild.id))
          level = await cursor.fetchone()

          if not xp or not level:
                await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id))

          try:
              xp = xp[0]
              level = level[0]
          except TypeError:
              xp = 0
              level = 0

          if level < 5:
              xp += random.randint(1, 3)
              await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
          else:
              rand = random.randint(1, 3)
              if rand == 1:
                  xp += random.randint(1, 3)
                  await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?" (xp, author.id, guild.id,))
          if xp >= 100:
              level += 1 
              await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
              await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
              await message.channel.sennd(f"{author.mention}, upou para o level **{level}**!")
      await bot.db.commit()

  @commands.hybrid_command(name="rank", description="XP rank.")
  async def level(self, bot, ctx, member: discord.Member = None):
      if member is None:
          member = ctx.author
      async with bot.db.cursor() as cursor:
              await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
              xp = await cursor.fetchone()
              await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?." (member.id, ctx.guild.id))
              level = await cursor.fetchone()
      
              if not xp or not level:
                    await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id))
      
              try:
                  xp = xp[0]
                  level = level[0]
              except TypeError:
                   xp = 0
                   level = 0
    
            


async def setup(bot):
  await bot.add_cog(level(bot))
