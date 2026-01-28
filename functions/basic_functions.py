import datetime
import os
import hashlib
from telegram import Update

#LOCAL IMPORTS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
import data.persistence as persistence
from data.time_zone import ZONE
from dotenv import load_dotenv


#BASIC FUNCTIONS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

"""
Por seguridad, se encriptan los datos de los usuarios. De esta forma, se refuerza la seguridad del bot
"""

load_dotenv()
SECRET_WORD = os.getenv("SECRET_WORD") #Palabra secreta para encriptar el id del usuario, guardada en .env

#Función que genera un id único para cada usuario partiendo del chat id
def generate_id(chat_id):
    bin_id = f"{chat_id}{SECRET_WORD}".encode()
    id = hashlib.sha256(bin_id).hexdigest()

    return id[:12]

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


async def start(update:Update, context):

    chat_id = update.effective_chat.id #Obtiene el id del chat
    user = update.effective_user.first_name #Obtiene el nombre del usuario
    

    user_id = generate_id(chat_id) #Id del usuario que va a ser almacenada
   

    if user_id not in persistence.REGISTERED_USERS:

        persistence.REGISTERED_USERS[user_id] = {
            'user_id': user_id,
            'user': user,
            'fecha_registro': str(datetime.datetime.now(ZONE))
        }

        persistence.TASKLIST[user_id] = {
            "pending_tasks": [],
            "completed_tasks": []
        }

        
        await context.bot.send_message(chat_id = chat_id, text=f"Hola, {user}, utiliza el comando /help para ver una lista de comandos disponibles")
        print(f"DEBUG: Nuevo usuario registrado: {user}")


    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Ya estás registrado. Usa el comando /help para ver las opciones disponibles"
        )
    
    for key in persistence.REGISTERED_USERS:
            print(f"{key}")


#---------------------------------------------------------------------------------------------------

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
        f"• <b>/deluser</b> ➡️ Elimina tu usuario del bot\n\n",
    parse_mode = "HTML")


#---------------------------------------------------------------------------------------------------

#Función que borra al usuario del bot
async def delete_user(update:Update, context):

    chat_id = update.effective_chat.id

    user_id = generate_id(chat_id) #Se calcula el id del usuario

    #Si el usuario está en nuestra base de datos, se borran todos sus datos, tareas y recordatorios
    if user_id in persistence.REGISTERED_USERS:
        
        persistence.REGISTERED_USERS.pop(user_id)
        persistence.TASKLIST.pop(user_id)

        current_jobs = context.job_queue.get_jobs_by_name(str(user_id))
        for job in current_jobs:
            job.schedule_removal()
    
        await update.message.reply_text(f"Usuario borrado con éxito")

    
    #Si no está en el sistema, se le dice que no está registrado
    else:
        await update.message.reply_text(f"No eres un usuario registrado")