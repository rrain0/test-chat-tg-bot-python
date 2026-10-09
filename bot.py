import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from env import TG_BOT_TOKEN

# Enable logging to keep track of errors or connection issues
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the reaction to the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Hello {update.effective_user.first_name}! I am your Python bot. How can I help you today?"
    )

# Define an echo function that copies incoming user text messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    await update.message.reply_text(f"You said: {user_text}")

if __name__ == '__main__':
    # Initialize the application with your BotFather token
    # REPLACE 'YOUR_TOKEN_HERE' with the actual string token from BotFather
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    # Register the command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start polling the Telegram servers for updates
    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()
