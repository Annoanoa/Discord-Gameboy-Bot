A discord bot for playing gameboy games through Python.
Place the .py file in its own folder, alongside a file named "rom.gbc" if using a gameboy color rom.
Open bot.py and edit lines 10 and 11 for your Discord bot token and the channel ID of the channel you want the bot running in(reccomended to use a special channel that anyone can see but noone has perms to message in)
If you're using a rom with a seperate file extension, go in to the .py, find the reference to "rom.gbc" and change it to the name of your rom.

This was made for Pokemon, so it comes with a savestates feature. A state is saved every 20 minutes, and the latest state(if one exists) is automatically loaded when the bot starts.

![](https://files.catbox.moe/g0gazr.png)
