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

    reply_markup = get_day_frequency()

    
    await update.message.reply_text(f"Nombre de recordatorio guardado como {reminder_name.capitalize()} \n"
                                    f"Selecciona los días que quieres establecer para el recordatorio",
                                    reply_markup=reply_markup)
    

    return DAY


#Solo muestra los botones
def get_day_frequency():
    
    keyboard = [
        [InlineKeyboardButton(f"Lunes", callback_data="LU")],
        [InlineKeyboardButton(f"Martes", callback_data="MA")],
        [InlineKeyboardButton(f"Miércoles", callback_data="MI")],
        [InlineKeyboardButton(f"Jueves", callback_data="JU")],
        [InlineKeyboardButton(f"Viernes", callback_data="VI")],
        [InlineKeyboardButton(f"Sábado", callback_data="SA")],
        [InlineKeyboardButton(f"Domingo", callback_data="DO")],
        [InlineKeyboardButton(f"Hecho", callback_data="DONE")],
        [InlineKeyboardButton(f"Cancelar", callback_data="CANCEL")],
    ]
    return InlineKeyboardMarkup(keyboard)



def auxiliar_day_function(selected_days: list) -> InlineKeyboardMarkup:

    DAYS = {"LU": "Lunes", "MA": "Martes", "MI": "Miércoles", 
            "JU": "Jueves", "VI": "Viernes", "SA": "Sábado", "DO": "Domingo"}
    
    def get_button_selected(key):
        text = DAYS[key]
        return f"✅ {text}" if key in selected_days else text
    
    keyboard = [
        [InlineKeyboardButton(get_button_selected("LU"), callback_data="LU")],
        [InlineKeyboardButton(get_button_selected("MA"), callback_data="MA")],
        [InlineKeyboardButton(get_button_selected("MI"), callback_data="MI")],
        [InlineKeyboardButton(get_button_selected("JU"), callback_data="JU")],
        [InlineKeyboardButton(get_button_selected("VI"), callback_data="VI")],
        [InlineKeyboardButton(get_button_selected("SA"), callback_data="SA")],
        [InlineKeyboardButton(get_button_selected("DO"), callback_data="DO")],
        [InlineKeyboardButton(f"Hecho", callback_data="DONE")],
        [InlineKeyboardButton(f"Cancelar", callback_data="CANCEL")]
    ]
    
    return InlineKeyboardMarkup(keyboard)



async def get_day_frequency_buttons(update:Update, context:CallbackContext):
    query = update.callback_query
    await query.answer()
    data = query.data


    if data == "CANCEL":
        await update.message.reply_text(f"Recordatorio Cancelado")
        ConversationHandler.END
    
    elif data in ["LU","MA","MI","JU","VI","SA","DO"]:
        selected_days = context.user_data["temp"].get("selected_days", [])

        if data in selected_days:
            selected_days.remove(data)
        else:
            selected_days.append(data)
        
        context.user_data["temp"]["selected_days"] = selected_days

        new_markup = auxiliar_day_function(selected_days)

        await query.edit_message_reply_markup(reply_markup=new_markup)

        return DAY
    
    elif data =="DONE":
        selected_days = context.user_data.get("temp", {}).get("selected_days", [])
        
        if not selected_days:
            await query.answer("Debes seleccionar al menos un día.", show_alert=True)
            return DAY
            
        
        await query.edit_message_text(f"Días guardados: {', '.join(selected_days)}")
        return HOUR 
    
    return DAY
