from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

TEMPLATE, CUSTOMER_NAME, SERVICE, PRICE = range(4)

message = (
    "<b>Salut Raph !</b> 👋\n"
    "Quel type de facture veux tu générer aujourd'hui ? \n"
    "Choisi une des options ci-dessous :"
)

async def generate_receipt(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("✨ Moncler", callback_data='moncler.html')],
        [InlineKeyboardButton("✨ Golden Goose", callback_data='test2.html')],
        [InlineKeyboardButton("✨ Stock X", callback_data='test3.html')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=message,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )

    return TEMPLATE


async def get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    active_template = query.data
    context.user_data['template'] = active_template

    await query.edit_message_text(f"Quel est le nom de l'acheteur (nom + prénom) ?")
    
    return CUSTOMER_NAME

async def get_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    context.user_data['customer_name'] = name
    
    await update.message.reply_text(f"Quel est le nom de l'article ?")
    return SERVICE

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['service'] = update.message.text
    await update.message.reply_text("Quel est le Prix ?")
    return PRICE

async def generate_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    customer_name = context.user_data.get('customer_name', 'Client Inconnu')
    price = update.message.text
    service = context.user_data['service']

    template_name = context.user_data.get('template', 'simple.html')

    date_jour = datetime.now().strftime("%d/%m/%Y")

    await update.message.reply_text("Génération en cours...")

    try:
        env = Environment(loader=FileSystemLoader('src/templates'))
        template = env.get_template(template_name)
        
        html_out = template.render(
            customer_name=customer_name, service=service, price=price, date=date_jour
        )
        
        file_buffer = BytesIO(html_out.encode('utf-8'))
        file_buffer.name = f"Facture_{service}.html"
        file_buffer.seek(0)
        
        await update.message.reply_document(
            document=file_buffer,
            filename=f"Facture_{service}.html",
            caption="Voici ta facture ! Ouvre-la avec ton navigateur 🌐"
        )

    except Exception as e:
        await update.message.reply_text(f"Erreur technique : {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Annulé.")
    return ConversationHandler.END