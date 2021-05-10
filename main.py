import discord
import os
import random

client = discord.Client()
gameList = []

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if (message.author == client.user):
    return

  response = 'ERROR! That is not a valid command! Please retype your command, or consult my available commands with \'!help\'.'

  if message.content.startswith('!help'):
    response = getHelp()

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
  return ('I am {0.user}. I suggest games at random when prodded. You can also feed me games that you would like to play.\n\n------------------\n\n/feed <game>\nAdds the game to my random storage.\n\n/prod <quantity?>\nGets a random game from my storage. You can prod an optional quantity from one to three.\n\n------------------\n\n'.format(client))

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
  if (not game.lower() in gameList):
    gameList.append(game.lower())

def removeGameName(game):
  if (not game.lower() in gameList):
    return 'I can\'t find that game in my RAM. It sounds delicious though!'
  gameList.remove(game.lower())
  return 'https://media.giphy.com/media/QVbghw1ThCJNK/giphy.gif'

client.run(os.getenv('TOKEN'))