import os
import discord
import requests
import json
import random
from replit import db
from keepRunning import keep_alive

BOTTOKEN = os.environ['TOKEN']

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserabel", "depressing"]

if "responding" not in db.keys():
	db["responding"] = True

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return(quote)

def update_encouragements(encouraging_message):
	if "encouragements" in db.keys():
		encouragements = db["encouragements"]
		encouragements.append(encouraging_message)
		db["encouragements"] = encouragements
	else:
		db["encouragements"] = [encouraging_message]

def delete_encouragements(index):
	encouragements = db["encouragements"]

	if len(encouragements) > index:
		del encouragements[index]
		db["encouragements"] = encouragements


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


'''
@client.event
async def on_member_update(before, after):
  if str(after.status) == "offline":
    print("{} has gone {}.".format(after.name,after.status))
'''


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('$Inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	if db["responding"]:
		options = [
			"Cheer up!", 
			"Hang in there.", 
			"You are a great person / bot!"
		]

		if "encouragements" in db.keys():
			options = options + list(db["encouragements"])

		if any(word in message.content for word in sad_words):
			await message.channel.send(random.choice(options))

	if message.content.startswith('$New'):
		encouraging_message = message.content.split("$New ", 1)[1]
		update_encouragements(encouraging_message)
		await message.channel.send("New encouraging message added.")

	if message.content.startswith('$Del'):
		encouragements = []

		if "encouragements" in db.keys():
			index = int(message.content.split("$Del ", 1)[1])
			delete_encouragements(index)
			encouragements = db["encouragements"]

		await message.channel.send(encouragements)

	if message.content.startswith('$List'):
		encouragements = []

		if "encouragements" in db.keys():
			encouragements = db["encouragements"]
		
		await message.channel.send(encouragements)

	if message.content.startswith('$Responding'):
		value = message.content.split("$Responding ", 1)[1]

		if value.lower() == "true":
			db["responding"] = True
			await message.channel.send("Robot response has been turned on.")
		else:
			db["responding"] = False
			await message.channel.send("Robot response has been turned off.")

keep_alive()
client.run(BOTTOKEN)
