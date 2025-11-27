from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler


#LOCAL IMPORTS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
import persistence


#TASK FUNCTIONS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

async def add_task(update:Update, context):
    chat_id = update.effective_chat.id

    #If users only write /addtask without task
    if not context.args:
        await context.bot.send_message(chat_id=chat_id, text=f"Debes escribir el comando y el nombre de la tarea")
        return

    task = " ".join(context.args)

    if chat_id in persistence.TASKLIST:

        user_tasklist = persistence.TASKLIST[chat_id]["pending_tasks"]
        if task in user_tasklist:
            await context.bot.send_message(chat_id=chat_id, text=f"{task} ya existe como tarea pendiente")

        else:
            persistence.TASKLIST[chat_id]["pending_tasks"].append(task)
            await context.bot.send_message(chat_id=chat_id, text=f"{task} añadido como tarea pendiente")
    
    else:
       await context.bot.send_message(chat_id=chat_id, text="Usa el comando /start primero")


async def show_pending_tasks(update:Update, context):

    chat_id = update.effective_chat.id

    if chat_id in persistence.TASKLIST:
        await context.bot.send_message(chat_id=chat_id, text=f"Tienes las siguientes tareas pendientes: ")
        
        for task in persistence.TASKLIST[chat_id]["pending_tasks"]:
            await context.bot.send_message(chat_id=chat_id, text=f"{task}")
    
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"Usa el comando /start primero")




OPTION = range(1)

async def delete_task(update:Update, context:CallbackContext):

    chat_id = update.effective_chat.id

    if chat_id not in persistence.TASKLIST or not persistence.TASKLIST[chat_id].get("pending_tasks"):
        await update.message.reply_text("¡No tienes tareas pendientes para borrar!")
        return ConversationHandler.END 

    else:
        user_tasklist = persistence.TASKLIST[chat_id]["pending_tasks"]
        keyboard = []
        
        #Create a row for each task
        for index,task in enumerate(user_tasklist):
                keyboard.append([InlineKeyboardButton(f"{task}", callback_data=task)])

        
        keyboard.append([InlineKeyboardButton("Cancelar", callback_data="CANCEL_DELETE")])
        reply_markup = InlineKeyboardMarkup(keyboard)
                
        await update.message.reply_text(text=f"Tienes las siguientes tareas pendientes, ¿Cual quieres borrar?:", reply_markup=reply_markup)
        return OPTION

    

async def delete_button(update:Update, context:CallbackContext):
    chat_id = update.effective_chat.id
    query = update.callback_query
    await query.answer()

    data = query.data

    user_tasklist = persistence.TASKLIST[chat_id]["pending_tasks"]
    

    if chat_id in persistence.TASKLIST:

        if data == "CANCEL_DELETE":
            await query.edit_message_text("Operación de eliminación de tareas cancelada.")
            return ConversationHandler.END

        if data in user_tasklist:
            user_tasklist.remove(data)

        if not user_tasklist:
        # No quedan tareas: Finalizar la conversación
            await query.edit_message_text("✅ ¡Todas las tareas han sido eliminadas! Conversación finalizada.")
            return ConversationHandler.END

        keyboard = []
        for task in user_tasklist:
            keyboard.append([InlineKeyboardButton(f"{task}", callback_data=task)])
        
    keyboard.append([InlineKeyboardButton("Terminar Eliminación", callback_data="CANCEL_DELETE")])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Tarea eliminada. Toca otra para seguir borrando:",
        reply_markup=reply_markup
    )

    return OPTION


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operacion cancelada.")
    return ConversationHandler.END