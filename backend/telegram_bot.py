import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from pathlib import Path

# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

class Telebot:
    def __init__(self, token):
        global chat_ids
        Path('./tele_bot_receivers.txt').touch(exist_ok=True)
        f = open('./tele_bot_receivers.txt', 'r+') 
        chat_ids = f.read().splitlines()
        f.close()
        self.application = ApplicationBuilder().token(token).build()
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.save_chat_id(str(update.effective_chat.id))
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully subbed to the bot")

    #blocks main thread
    def run(self):
        self.application.run_polling(close_loop=False)

    async def send_message(self, msg):
        global chat_ids
        for chat_id in chat_ids:
            await self.application.bot.send_message(chat_id=chat_id, text=msg)
            print("sent msg: " + msg + " to chat_id " + chat_id)

    def save_chat_id(self, chat_id):
        global chat_ids
        if not chat_id in chat_ids:
            chat_ids.append(chat_id)
            f = open('./tele_bot_receivers.txt', 'w+')
            f.write("\n".join(chat_ids))
            f.close()
            print("saved chat_id " + chat_id)
