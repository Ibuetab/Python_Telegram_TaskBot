import datetime
from telegram import Update


#LOCAL IMPORTS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
import data.persistence as persistence
from data.time_zone import ZONE



#BASIC FUNCTIONS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

""" Due to Privacy Policy of Telegram, users must initialize the communication with the bot. 
So, I tried to make a function which bot initialize the comunication with the user, but it is not possible.  

"""

async def start(update:Update, context):

    chat_id = update.effective_chat.id #get the chat_id
    user_id = update.effective_user.id #get the user id
    username = update.effective_user.username #get the username

    if chat_id not in persistence.REGISTERED_USERS:

        persistence.REGISTERED_USERS[chat_id] = {
            'user_id': user_id,
            'username': username,
            'fecha_registro': str(datetime.datetime.now(ZONE))
        }

        persistence.TASKLIST[chat_id] = {
            "pending_tasks": [],
            "completed_tasks": []
        }

   
        if username:
            await context.bot.send_message(chat_id = chat_id, text=f"Hola, usuario @{username}, utiliza el comando /help para ver una lista de comandos disponibles")
            print(f"DEBUG: Nuevo usuario registrado: @{username}")
        else:
            await context.bot.send_message(chat_id = chat_id, text=f"Hola, usuario {chat_id}, utiliza el comando /help para ver una lista de comandos disponibles")
            print(f"DEBUG: Nuevo usuario registrado: @{username}")


    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Ya estás registrado. Usa el comando /help para ver las opciones disponibles"
        )


async def help(update:Update, context):
    chat_id= update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id,
    text=f"<b>Aquí tienes una lista de comandos disponibles:</b>\n\n"
        f"• <b>/start</b> ➡️ Inicializa el bot\n\n" 
        f"• <b>/help</b> ➡️ Muestra una lista de comandos del bot\n\n"
        f"• <b>/addtask (nombre de tarea)</b> ➡️ añade una tarea a la lista de tareas\n\n"
        f"• <b>/showtasks</b> ➡️ Muestra la lista de tareas pendientes\n\n"
        f"• <b>/comtasks</b> ➡️ Muestra la lista de tareas pendientes y permite marcar las tareas realizadas como completadas\n\n"
        f"• <b>/deltask</b> ➡️ Permite seleccionar una tarea a eliminar de la lista de tareas pendientes\n\n"
        f"• <b>/reminder</b> ➡️ Establece un recordatorio diario\n\n"
        f"• <b>/deluser</b> ➡️ Elimina un usuario del bot\n\n",
    parse_mode = "HTML")




async def delete_user(update:Update, context):
    chat_id = update.effective_chat.id

    if chat_id in persistence.REGISTERED_USERS:
        
        persistence.REGISTERED_USERS.pop(chat_id)
        persistence.TASKLIST.pop(chat_id)

        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in current_jobs:
            job.schedule_removal()
    
        await update.message.reply_text(f"Usuario borrado con éxito")

    else:
        await update.message.reply_text(f"No eres un usuario registrado")