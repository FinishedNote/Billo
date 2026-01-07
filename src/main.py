from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler, filters
from src.config import TOKEN
from src.handlers import generate_receipt, get_product, get_client_name, get_price, generate_pdf, cancel, TEMPLATE, CUSTOMER_NAME, SERVICE, PRICE

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('generate_receipt', generate_receipt)],
        states={
            TEMPLATE: [CallbackQueryHandler(get_product)],
            CUSTOMER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_client_name)],
            SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, generate_pdf)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()