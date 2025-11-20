import json
import os
import atexit
import datetime
import pytz
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("El token de Telegram no se encontró. Asegúrate de que BOT_TOKEN esté definido en el archivo .env.")


#REGISTER USERS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

USERS_DATA_FILE = "users_data.json"
REGISTERED_USERS = {} #User data store on a dictionary


def load_data():
    global REGISTERED_USERS
    if os.path.exists(USERS_DATA_FILE):
        try:
            with open(USERS_DATA_FILE, "r") as f:
                data_from_json = json.load(f)
                REGISTERED_USERS = {int(k): v for k, v in data_from_json.items()}
                print(f" Datos cargados: {len(REGISTERED_USERS)} usuarios en memoria.")

        except json.JSONDecodeError:
            print(" Error al leer el archivo JSON. Iniciando con diccionario vacío.")


def save_data():
    global REGISTERED_USERS
    try:
        with open(USERS_DATA_FILE, 'w') as f:
            json.dump(REGISTERED_USERS, f, indent=4)
        print(f"Datos guardados: {len(REGISTERED_USERS)} usuarios escritos en disco.")
    except Exception as e:
        print(f" Error al guardar datos: {e}")


#REGISTER USERS' TASK
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

USERS_TASK_LIST = "task_list.json"
TASKLIST = {} #users tasklist stored on a dictionary

def load_tasklist():
    global TASKLIST
    if os.path.exists(USERS_TASK_LIST):
        try:
            with open(USERS_TASK_LIST, "r") as f:
                data_from_json = json.load(f)
                TASKLIST = {int(k): v for k, v in data_from_json.items()}
                print(f"Tareas cargadas de {len(TASKLIST)} usuarios")

        except json.JSONDecodeError:
            print(f"Error al cargar las tareas")

def save_tasklist():
    global TASKLIST
    try:
        with open(USERS_TASK_LIST, "w") as f:
            json.dump(TASKLIST,f,indent=4)
            print(f"Tareas guardadas de {len(TASKLIST)} usuarios")

    except Exception as e:
        print(f"Error al guardar las tareas {e}")


#TIME ZONE
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------


ZONE = pytz.timezone("Europe/Madrid")
time = datetime.time(hour=12, minute= 24, second=0, tzinfo=ZONE)



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

    if chat_id not in REGISTERED_USERS:

        REGISTERED_USERS[chat_id] = {
            'user_id': user_id,
            'username': username,
            'fecha_registro': str(datetime.datetime.now(ZONE))
        }

        TASKLIST[chat_id] = []
   
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
    await context.bot.send_message(chat_id=chat_id, text=f"Aqui tienes una lista de comandos disponibles: \n /start -> Inicializa el bot \n /help -> Muestra una lista de comandos del bot \n /addtask (nombre de tarea)-> añade una tarea a la lista de tareas")


#TASK FUNCTIONS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

async def add_task(update:Update, context):

    chat_id = update.effective_chat.id

    if not context.args:
        await context.bot.send_message(chat_id=chat_id, text=f"Debes escribir el comando y el nombre de la tarea")
        return

    task = " ".join(context.args)

    if chat_id in TASKLIST:

        user_tasklist = TASKLIST[chat_id]
        if task in user_tasklist:
            await context.bot.send_message(chat_id=chat_id, text=f"{task} ya existe como tarea")

        else:
            TASKLIST[chat_id].append(task)
            await context.bot.send_message(chat_id=chat_id, text=f"{task} añadido como tarea")
    
    else:
       await context.bot.send_message(chat_id=chat_id, text="Usa el comando /start primero")


    
async def delete_task(update:Update, context):

    chat_id = update.effective_chat.id

    task = " ".join(context.args)

    if chat_id in TASKLIST:
        user_tasklist = TASKLIST[chat_id]
        if task not in user_tasklist:
            await context.bot.send_message(chat_id=chat_id, text=f"{task} no existe en la lista de tareas")
        
        else:
            TASKLIST[chat_id].remove(task)
            await context.bot.send_message(chat_id=chat_id, text=f"La tarea {task} ha sido eliminada")

    else:
    
        await context.bot.send_message(chat_id=chat_id, text=f"Usa el comando /start primero")


async def show_tasks(update:Update, context):

    chat_id = update.effective_chat.id

    if chat_id in TASKLIST:
        await context.bot.send_message(chat_id=chat_id, text=f"Tienes las siguientes tareas: ")
        
        for task in TASKLIST[chat_id]:
            await context.bot.send_message(chat_id=chat_id, text=f"{task}")
    
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"Usa el comando /start primero")


#BOT RUNNING
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#Main function. Build the bot and store handlers
def main():

    #---------------------------------------------------------------------------------------------------

    load_data()
    load_tasklist()

    atexit.register(save_data)
    atexit.register(save_tasklist)

    #---------------------------------------------------------------------------------------------------

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    #---------------------------------------------------------------------------------------------------

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("deltask", delete_task))
    app.add_handler(CommandHandler("showtasks", show_tasks))
   
   #---------------------------------------------------------------------------------------------------


    app.run_polling()



#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

#If scripts's name match with 'main', bot starts
if __name__ == "__main__":
    main()