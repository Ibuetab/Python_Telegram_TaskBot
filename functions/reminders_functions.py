from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


import data.persistence as persistence





NAME,DAY,HOUR,MINUTE = range(4)

async def reminder_name(update:Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in persistence.REGISTERED_USERS:
        await update.message.reply_text(f"No eres un usuario registrado")
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"Escribe un nombre para el recordatorio")
        return NAME


async def get_reminder_name(update:Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    reminder_name_raw = update.message.text
    reminder_name = reminder_name_raw.lower()

    context.user_data["temp"] = {"name": reminder_name}

    
    await update.message.reply_text(f"Nombre de recordatorio guardado como {reminder_name.capitalize()} \n"
                                        f"Selecciona los días que quieres establecer para el recordatorio")
        
    return DAY

