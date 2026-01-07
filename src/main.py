from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from src.config import TOKEN
from src.handlers import start, button_handler

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot Démarré...")
    app.run_polling()

if __name__ == "__main__":
    main()