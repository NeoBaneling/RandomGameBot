import discord
from discord.ext import tasks
import os
import random
import time

client = discord.Client()
gameList = []
zergProne = False
zergProneChecked = False
zergProneTick = 20
rushTick = 2

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  setZergProne.start()

@client.event
async def on_message(message):
  global zergProne
  global zergProneChecked

  if (message.author == client.user):
    return

  sender = str(message.author)

  response = 'ERROR! That is not a valid command! Please retype your command, or consult my available commands with \'!help GAMEINATOR\'.'

  if message.content.startswith('!help GAMEINATOR'):
    response = getHelp()

  if message.content.startswith('/debug'):
    await message.channel.send('Running diagnostics...')

    time.sleep(2)
    if (not zergProne):
      response = 'No zerglings found here! Thank you for being vigilant ' + sender + '.'
    else:
      zergProne = False
      await message.channel.send('ERR█R! Zerglings everywh█re!')
      await message.channel.send('La█nching an█ivirus s█ftware...')
      time.sleep(9)
      response = 'Zerglings eradicated. I would have been assimilated if it weren\'t for you ' + sender + '!'
      addZergling.stop()

    zergProneChecked = False
    setZergProne.restart()

  if message.content.startswith('/feed '):
    saveGameName(message.content[6:len(message.content)])
    response = 'Delicious bytes. I will have to lie down.'

  if (message.content.startswith('/prod')):
    response = getRandomGames(1)

  if (message.content.startswith('/prod ')):
    response = getRandomGames(message.content[6:7])

  if message.content.startswith('/storage'):
    response = gameList

  if (message.content.startswith('/vomit ')):
    response = removeGameName(message.content[7:len(message.content)])

  await message.channel.send(response)

def getHelp():
  return ('I am {0.user}. I suggest games at random when prodded. You can feed me games that you would like to play. Prone to zerg rushes if not properly monitored.\n\n------------------\n\n/debug\nRemoves any zerglings from my shell.\n\n/feed <game>\nAdds the game to my random storage.\n\n/prod (quantity)\nGets a random game from my storage. You can prod an optional quantity from one to three.\n\n/storage\nLists all games in my random storage.\n\n/vomit <game>\nRemoves a game from my random storage.\n\n------------------\n\n'.format(client))

def getRandomGames(number):
  prodCount = int(number)
  if (len(gameList) == 0):
    return 'ERROR! Feed me some games with \'/feed\' before prodding me!'
  elif (prodCount < 1 or prodCount > 3):
    return 'ERROR! You can only prod for up to three games!'
  else:
    prodGameList = gameList[:]
    games = ''
    i = 0
    while(len(prodGameList) > 0 and i < prodCount):
      game = prodGameList[random.randint(0, len(prodGameList) - 1)]
      games = games + game + '\n'
      prodGameList.remove(game)
      i = i + 1
    return games

def saveGameName(game):
  if (not game.lower() in gameList or game == 'zergling'):
    gameList.append(game.lower())

def removeGameName(game):
  if (not game.lower() in gameList):
    return 'I can\'t find that game in my RAM. It sounds delicious though!'
  gameList.remove(game.lower())
  return 'https://media.giphy.com/media/QVbghw1ThCJNK/giphy.gif'

@tasks.loop(hours=rushTick)
async def addZergling():
  saveGameName('zergling')

@tasks.loop(hours=zergProneTick)
async def setZergProne():
  global zergProne
  global zergProneChecked
  if (not zergProneChecked):
    zergProneChecked = True
    print('zerg prone has been checked')
  else:
    zergProne = True
    addZergling.start()
    setZergProne.stop()
    zergProneChecked = False
    print('beginning zerg rush')

client.run(os.getenv('TOKEN'))