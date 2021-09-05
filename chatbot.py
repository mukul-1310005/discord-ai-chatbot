import discord
import os
import requests
import json
import random
from neuralintents import GenericAssistant
from dotenv import load_dotenv

assistant = GenericAssistant('intents.json')
assistant.train_model()
assistant.save_model()


client = discord.Client()

dice_roll = [1,2,3,4,5,6]

coins = ["heads", "tails"]

sad_words = ["sad", "depress", "depressed", "unhappy", "miserable", "broken", "angry", "depressing"]

starter_encouragements = ["Cheer up! buddy", "You are a great person.",
"Come on, Don't be sad, You can do it", "You can do it"]

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " _" + json_data[0]['a']
	return quote

def get_joke():
	response = requests.get("https://api.chucknorris.io/jokes/random")
	json_data = json.loads(response.text)
	joke = json_data['value']
	return joke


@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	msg = message.content.lower()

	if msg.startswith('>dice'):
		await message.channel.send(random.choice(dice_roll))

	if msg.startswith('>quote'):
		quote = get_quote()
		await message.channel.send(quote)

	if msg.startswith('>joke'):
		joke = get_joke()
		await message.channel.send(joke)

	if msg.startswith('>coin'):
		await message.channel.send(random.choice(coins))

	if msg.startswith('>'):
		res = assistant.request(message.content[1:])
		await message.channel.send(res)

	if any(word in message.content.lower() for word in sad_words):
		await message.channel.send(random.choice(starter_encouragements))


load_dotenv()
TOKEN = os.getenv('TOKEN')
client.run(TOKEN)