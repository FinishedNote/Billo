from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Moncler", callback_data='mc')],
        [InlineKeyboardButton("Golden Goose", callback_data='gg')],
        [InlineKeyboardButton("Stock x", callback_data='sx')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "<b>Salut Raph !</b> 👋\n"
        "Quel type de facture veux tu générer aujourd'hui ? \n"
        "Choisi une des options ci-dessous :"
    )

    await update.message.reply_text(
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    await query.answer()
    
    if query.data == 'mc':
        await query.edit_message_text(text="Facture Moncler en cours de création...")
    elif query.data == 'gg':
        await query.edit_message_text(text="Facture Golden Goose en cours de création...")
    elif query.data == 'sx':
        await query.edit_message_text(text="Facture Stock x en cours de création...")