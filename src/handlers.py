from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Test 1", callback_data='test1')],
        [InlineKeyboardButton("Test 2", callback_data='test2')],
        [InlineKeyboardButton("Test 3", callback_data='test3')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Salut ! C'est Billo", 
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    await query.answer()
    
    if query.data == 'test1':
        await query.edit_message_text(text="Test 1")
    elif query.data == 'test2':
        await query.edit_message_text(text="Test 2")
    elif query.data == 'test3':
        await query.edit_message_text(text="Test 3")