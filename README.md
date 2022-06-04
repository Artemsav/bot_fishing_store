# Bot fishing store

## Project description

Placeholder

To run telegram_bot:

```bash
python telegram_bot.py
```

Example of telegram bot (or you can find it here: @fixme):
![Example](./images/fish-shop.gif)


## Instalation

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

There is enviroment variables using in the application, you will need tp create ```.env``` file. A ```.env``` file is a text file containing key value pairs of all the environment variables required by the application. You can see example of it below:

```python
# example of environment variables defined inside a .env file
TOKEN_TELEGRAM=1253123421:FFA1DSGOh_dfQACXYT5IiQwEBP5CwJozyP8
TG_TOKEN_LOGGING = 9817234321:SSA1DSGOh_dfQACXYT5IiQwEBP5CwCagaV7
TG_USER_ID=612578269
```

TOKEN_TELEGRAM - to get it please writte to Telegram @BotFather bot, first you shall ```/start``` command, than ```/newbot```, than follow the instruction in Telegram.  

TG_TOKEN_LOGGING - to get it please writte to Telegram @BotFather bot, first you shall ```/start``` command, than ```/newbot```, than follow the instruction in Telegram.

TG_USER_ID - to get it please writte to Telegram @userinfobot. Send ```/start``` command to the bot.


## Project Goals

The code is written for educational purposes on online-course for web-developers [Devman](https://dvmn.org)
