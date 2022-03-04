import discord
import os
import asyncio
from discord.utils import get
from keep_alive import keep_alive
import random

keep_alive()
client = discord.Client()

botchannel = {
  909782965544964096,
  747355506913443852,
  928351060609892363,
  848935586005123083,
  818455248401989702,
  818453614329724990
}
allowedbot = {
  408785106942164992,
  270904126974590976,
  559426966151757824,
  235148962103951360
}

warword = [
  'địt',
  'ukrs',
  'uk rs',
  '??',
  'mẹ mày',
  'don\'t care',
  'dont care',
  'did\'t ask',
  'didnt ask',
  'cmm',
  'đéo',
  'mẹ m',
  'mẹ',
  'như lồn',
  'cặc',
]

recent10mes = {}

voteEmoji = ['✅', '⛔']


global premes
global pendingMessage
global pendingMessageid
global pos
global neg

pendingMessageid = 0

@client.event
async def on_ready():
  print('Logged In')

@client.event
async def on_message(ctx):
  global premes
  global pendingMessage
  global pendingMessageid
  global pos
  global neg

  a = ctx
  channelid = ctx.channel.id
  category = ctx.channel.category_id
  uid = ctx.author.id
  tag = ctx.author.discriminator
  message = ctx.content
  #save recent 10 messages
  if channelid not in recent10mes:
    a = []
    recent10mes[channelid] = a
  l = recent10mes[channelid]
  l.append(ctx)
  if len(l) > 10:
    l.pop()

  #check if bot
  if ctx.author.bot and uid != 937375787529678910:
    if uid in allowedbot or category in botchannel or tag == '0000':
      return
    if channelid not in botchannel:
      await ctx.delete()
      print('Deleted')
      await premes.delete()
  premes = ctx

  #action vote
  id = 0
  action = 'none'
  try:
    x = 0
    if message[x:x + 3] == 'cs!':
        x = 3
        if 'kick' == message[x:x + 4]:
            action = 'kick'
            x = x + 5
        elif 'mute' == message[x:x + 4]:
          action = 'mute'
          x = x + 5
        elif 'unmute' == message[x:x + 6]:
          action = 'unmute'
          x = x + 7
        elif 'ban' == message[x:x + 3]:
            action = 'ban'
            x = x + 4
        elif 'antiwar' == message[x:x + 7]:
          action = 'antiwar'
          x = x + 8
        elif 'help' == message[x:x + 4]:
          action = 'help'
          x = x + 5
        elif 'changenickname' == message[x:x + 14]:
          action = 'changenickname'
          x = x + 15
        elif 'howcringe' == message[x:x + 9]:
          action = 'howcringe'
          x = x + 9
        #get id
        try:
          if message[x+3] == '!':
              x = x + 3
          elif message[x+3] != '!':
              x = x + 1
          y = x + 1
          while message[x] != '>':
              x = x + 1
          id = message[y:x]
          x = x + 1
        except:
          id = 0
        x = x + 1
  except:
    print('Caught an exception')
    return
  #mod thing
  if action == 'mute':
    print(ctx.content)
    channel = client.get_channel(channelid)
    user = await ctx.guild.query_members(user_ids=int(id))
    user = user[0]
    username = await client.fetch_user(int(id))
    role = discord.utils.get(ctx.guild.roles,name='tù nhân')
    rep = '**' + str(ctx.author) + '**' + ' ' + 'required to ' + action + ' **' + str(username) + '**'
    #do action
    if pendingMessageid == 0:
      ctx = await channel.send(rep)
      pendingMessageid = ctx.id
      for e in voteEmoji:
        await ctx.add_reaction(e)
      pendingMessage = ctx
      pos = 0
      neg = 0
      await asyncio.sleep(60)
      ctx = pendingMessage
      res = ''

      if pos > neg and pos > 3:
        res = 'Proceed to mute ' + str(user)
        await user.add_roles(role)
      elif pos > neg and pos <= 3:
        res = 'Rejected the request (Reason: Not enough ✅)'
      else:
        res = 'Rejected the request (Reason: ⛔ has more vote)'
      rep = 'Result: ' + res
      pendingMessageid = 0
      pos = 0
      neg = 0
      await pendingMessage.reply(rep)
    else:
      await channel.send('Cannot start poll (Reason: A poll is happening right now)')

  elif action == 'unmute':
    channel = client.get_channel(channelid)
    user = await ctx.guild.query_members(user_ids=int(id))
    user = user[0]
    username = await client.fetch_user(int(id))
    role = discord.utils.get(ctx.guild.roles,name='tù nhân')
    rep = '**' + str(ctx.author) + '**' + ' ' + 'required to ' + action + ' **' + str(username) + '**'
    #do action
    if pendingMessageid == 0:
      ctx = await channel.send(rep)
      pendingMessageid = ctx.id
      for e in voteEmoji:
        await ctx.add_reaction(e)
      pendingMessage = ctx
      pos = 0
      neg = 0
      await asyncio.sleep(60)
      ctx = pendingMessage
      res = ''

      if pos > neg and pos > 3:
        res = 'Proceed to unmute ' + str(user)
        await user.remove_roles(role)
      elif pos > neg and pos <= 3:
        res = 'Rejected the request (Reason: Not enough ✅)'
      else:
        res = 'Rejected the request (Reason: ⛔ has more vote)'
      rep = 'Result: ' + res
      pendingMessageid = 0
      pos = 0
      neg = 0
      await pendingMessage.reply(rep)
    else:
      await channel.send('Cannot start poll (Reason: A poll is happening right now)')

  elif action == 'changenickname':
    nickname = message[x:len(message)]
    channel = client.get_channel(channelid)
    user = await ctx.guild.query_members(user_ids=int(id))
    user = user[0]
    username = await client.fetch_user(int(id))
    rep = '**' + str(ctx.author) + '**' + ' ' + 'required to change **' + str(username) + '**' + ' nickname to \"' + nickname + '\"'
    #do action
    if pendingMessageid == 0:
      ctx = await channel.send(rep)
      pendingMessageid = ctx.id
      for e in voteEmoji:
        await ctx.add_reaction(e)
      pendingMessage = ctx
      pos = 0
      neg = 0
      await asyncio.sleep(60)
      ctx = pendingMessage
      res = ''

      if pos > neg and pos > 3:
        try:
          res = 'Proceed to change ' + str(user) + ' nickname'
          await user.edit(nick=nickname)
        except:
          res = 'Have enough vote but cannot change nickname'
      elif pos > neg and pos <= 3:
        res = 'Rejected the request (Reason: Not enough ✅)'
      else:
        res = 'Rejected the request (Reason: ⛔ has more vote)'
      rep = 'Result: ' + res
      pendingMessageid = 0
      pos = 0
      neg = 0
      await pendingMessage.reply(rep)
    else:
      await channel.send('Cannot start poll (Reason: A poll is happening right now)')
  elif action == 'antiwar':
    channel = client.get_channel(channelid)
    await channel.send('Scanning 10 most recent messages...')
    wCount = 0
    willmute = []
    role = discord.utils.get(ctx.guild.roles,name='tù nhân')
    for c in l:
      msg = c.content
      for e in warword:
        if e in msg:
          wCount = wCount + 1
      if wCount > 1:
        if str(c.author) not in willmute and str(c.author) != 'Cộng Sả#0102':
          willmute.append(str(c.author))
    if len(willmute) > 1:
      rep = 'War detected'
      a = await channel.send(rep)
      channel = client.get_channel(909799079037517844)
      s = str(willmute)
      messagelink = 'https://discordapp.com/channels/' + str(a.guild.id) + '/' + str(a.channel.id) + '/' + str(a.id)
      rep = 'War detected!\nMember: ' + str(s) + '\nMessage link: ' + messagelink
      await channel.send(rep)
    else:
      await channel.send('No war detected')

  elif action == 'help':
    rep = '> **Available Commands**\ncs!mute *@member* : Open mute member poll (duration 60s)\ncs!unmute *@member* : Open unmute member poll (duration 60s)\ncs!changenickname *@member* *nickname* : Open change member nickname poll\ncs!antiwar : Scan 10 most recent message for war'
    channel = client.get_channel(channelid)
    await channel.send(rep)

    """
  elif action == 'kick':
    channel = client.get_channel(channel)
    user = await client.fetch_user(int(id))
    rep = '**' + str(ctx.author) + '**' + ' ' + 'required to ' + action + ' **' + str(user) + '**'
    await channel.send(rep)
  elif action == 'ban':
    channel = client.get_channel(channel)
    user = await client.fetch_user(int(id))
    rep = '**' + str(ctx.author) + '**' + ' ' + 'required to ' + action + ' **' + str(user) + '**'
    await channel.send(rep)
    """
  elif action == 'howcringe':
    rate = random.randrange(0, 101)
    rep = 'This message is ' + str(rate) + '% cringe.'
    channel = client.get_channel(channelid)
    if ctx.reference:
      ms = await channel.fetch_message(ctx.reference.message_id)
      await ms.reply(rep)
    else:
      await channel.send('No message referenced.')
  else:
    return

@client.event
async def on_raw_reaction_add(payload):
  try:
    global pendingMessageid
    global pos
    global neg
    if payload.message_id == pendingMessageid:
      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      reaction = get(message.reactions, emoji=payload.emoji.name)
      if payload.emoji.name == '✅':
        pos = reaction.count
      elif payload.emoji.name == '⛔':
        neg = reaction.count
  except:
    pendingMessageid = 0

client.run(os.environ['DISCORD_TOKEN'])