from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import datetime

import data.persistence as persistence
from data.time_zone import ZONE,DIAS


NAME,DAY,HOUR,MINUTE = range(4)


#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

#Función auxiliar que responde al comando /reminder para preguntar el nombre del recordatorio
async def reminder_name(update:Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id not in persistence.REGISTERED_USERS:
        await update.message.reply_text(f"No eres un usuario registrado")
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"Escribe un nombre para el recordatorio")
        return NAME
    

#Función que obtiene el nombre del recordatorio, lo almacena temporalmente, y pasa al siguiente estado
async def get_reminder_name(update:Update, context: CallbackContext):

    reminder_name_raw = update.message.text
    reminder_name = reminder_name_raw.lower()

    context.user_data["temp"] = {"name": reminder_name}

    reply_markup = get_day_frequency() #Muestra los botones de los días, definidos en la función get_day_frequency depués de obtener el nombre del recordatorio

    await update.message.reply_text(f"Nombre de recordatorio guardado como {reminder_name.capitalize()} \n"
                                    f"Selecciona los días que quieres establecer para el recordatorio",
                                    reply_markup=reply_markup) #Siguiente estado

    return DAY



#SELECCIONAR LOS DÍAS
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------

#Función que solo muestra los botones
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

#------------------------------------------------------------------------------------------------------------------------------------------------

#Función auxiliar que muestra con un tic verde los días seleccionados
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

#------------------------------------------------------------------------------------------------------------------------------------------------

#Función que selecciona los días y los almacena temporalmente, posteriormente pasa al siguiente estado para pedir la hora
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
            
        
        await query.edit_message_text(f"Días guardados: {', '.join(selected_days)} \n \n"
                                      f"Escribe la hora (Sin los minutos) a la que quieras recibir el recordatorio (En formato 24h)")
        return HOUR 
    
    return DAY


#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------



async def get_hour(update:Update, context:CallbackContext):

    hour = update.message.text.strip()
    

    if len(hour) > 2 or not hour.isnumeric():
        await update.message.reply_text(f"Escribe solo la hora sin los minutos")
        return HOUR

    hour_int = int(hour)

    if hour_int < 0 or hour_int > 23:
        await update.message.reply_text(f"Escribe un numero ente 0 y 23 (Ambos inclusive)")
        return HOUR

    formatted_hour = f"{hour_int:02d}"
    context.user_data.setdefault("temp", {})["hour"] = formatted_hour

    await update.message.reply_text(f"Hora guardada como {formatted_hour} \n"
                                    f"Escribe los minutos (Por defecto es 00)")
    return MINUTE


async def get_minute(update:Update, context:CallbackContext):
    reminder_minute = update.message.text.strip()

    try:
        minute = int(reminder_minute)
        if not 0<= minute <= 59:
            raise ValueError("Minuto fuera de rango")
            
    except ValueError:
        await update.message.reply_text(f"Introduce un numero entre 0 y 59")
        return MINUTE

    formatted_minute = f"{minute:02d}"
    context.user_data.setdefault("temp", {})["minute"] = formatted_minute

    await update.message.reply_text(
        f"Minuto guardado como {formatted_minute} \n",
        parse_mode="MarkdownV2"
    )
    
    return await save_and_finish(update, context)



async def save_and_finish(update:Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    datos_finales = context.user_data.get("temp")

    dias_numeros = tuple(DIAS[d] for d in datos_finales["selected_days"])
    dias_para_bot = tuple(DIAS[d] for d in datos_finales["selected_days"])

    persistence.save_reminders(chat_id, datos_finales)

    await update.message.reply_text(f"Recordatorio guardado como {datos_finales['name']} \n"
                             f"Los días {datos_finales['selected_days']} \n"
                             f"A la hora {datos_finales['hour']} : {datos_finales['minute']}")
    
    


    ahora = datetime.datetime.now(ZONE)
    print(f"DEBUG: Configurando run_daily")
    print(f"DEBUG: Hora: {datos_finales['hour']}:{datos_finales['minute']}")
    print(f"DEBUG: Días (tupla de ints): {dias_numeros}")
    print(f"DEBUG: Hoy es día número {ahora.weekday()} (0=Lunes, 1=Martes...)")
    print(f"Reloj Sistema: {datetime.datetime.now()}")
    print(f"Reloj Madrid:  {datetime.datetime.now(ZONE)}")

    try:
        nuevo_job = context.job_queue.run_daily(
            callback=nombre_alarma,
            time=datetime.time(
                hour=int(datos_finales['hour']), 
                minute=int(datos_finales['minute']), 
                tzinfo=ZONE
            ),
            days=dias_para_bot,
            chat_id=int(chat_id),
            data=datos_finales['name']
        )
        if nuevo_job:
            print(f"✅ Job creado con éxito. Próxima ejecución: {nuevo_job.next_t}")
        else:
            print("❌ El Job no se pudo crear.")
    except Exception as e:
        print(f"❌ Error crítico al programar run_daily: {e}")

    context.user_data.pop("temp", None)
    return ConversationHandler.END


async def nombre_alarma(context:CallbackContext):
    job = context.job
    chat_id = str(job.chat_id)
    nombre_job = job.data 
    
    await context.bot.send_message(chat_id, f"⏰ Recordatorio: {nombre_job}")
    