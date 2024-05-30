import io
import asyncio
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import discord
from PIL import Image
import os
import hashlib
SAVE_STATE_FILE='save.state'
TOKEN='YOURTOKEN' #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
CHANNEL_ID=YOURCHANNELID #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
last_image_hash=None
pyboy=PyBoy('rom.gbc',window='null')
pyboy.set_emulation_speed(2)
intents=discord.Intents.default()
intents.messages=True
intents.message_content=True
intents.reactions=True
intents.members=True
client=discord.Client(intents=intents)
emoji_to_input={'🅰️':WindowEvent.PRESS_BUTTON_A,'🅱️':WindowEvent.PRESS_BUTTON_B,'⬆️':WindowEvent.PRESS_ARROW_UP,'⬇️':WindowEvent.PRESS_ARROW_DOWN,'⬅️':WindowEvent.PRESS_ARROW_LEFT,'➡️':WindowEvent.PRESS_ARROW_RIGHT,'⭐':WindowEvent.PRESS_BUTTON_START,'🌕':WindowEvent.PRESS_BUTTON_SELECT}
async def manage_savestates():
	while not client.is_closed():await asyncio.sleep(20*60);pyboy.save_state(open(SAVE_STATE_FILE,'wb'))
async def send_initial_message(channel):
	embed=discord.Embed(title='<3 - AnoAno');file=discord.File(fp=io.BytesIO(b'\x89PNG\r\n\x1a\n'),filename='screenshot.png');message=await channel.send(embed=embed,file=file)
	for emoji in emoji_to_input.keys():await message.add_reaction(emoji)
	return message
async def update_game_frame(message):
	global last_image_idx,last_image_hash;frame_counter=0
	while not client.is_closed():
		pyboy.tick();frame_counter+=1
		if frame_counter%(60//2)==0:
			screen_data=pyboy.screen.image.convert('RGB')
			with io.BytesIO()as image_binary:
				screen_data.save(image_binary,format='PNG');image_binary.seek(0);current_image_hash=hashlib.md5(image_binary.getvalue()).hexdigest()
				if current_image_hash!=last_image_hash:new_file=discord.File(fp=image_binary,filename='screenshot.png');new_embed=discord.Embed(title='<3 - AnoAno');new_embed.set_image(url='attachment://screenshot.png');await message.edit(embed=new_embed,attachments=[new_file]);last_image_hash=current_image_hash
		await asyncio.sleep(1/(60//2))
@client.event
async def on_reaction_add(reaction,user):
	if user.bot:return
	if reaction.message.id==initial_message.id:
		input_event=emoji_to_input.get(str(reaction))
		if input_event:pyboy.send_input(input_event);await reaction.remove(user)
@client.event
async def on_ready():
	print(f"{client.user} has connected to Discord!")
	if os.path.exists(SAVE_STATE_FILE):
		try:pyboy.load_state(open(SAVE_STATE_FILE,'rb'));print('Successfully loaded savestate.')
		except Exception as e:print(f"Failed to load savestate: {e}")
	channel=client.get_channel(CHANNEL_ID);global initial_message;initial_message=await send_initial_message(channel);client.loop.create_task(update_game_frame(initial_message));client.loop.create_task(manage_savestates())
client.run(TOKEN)