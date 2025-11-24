import os
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes

#---------------------------------------------------------------------------------------------------

from persistence import TASKLIST, REGISTERED_USERS, load_data
from basic_functions import start, help

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("El token de Telegram no se encontró. Asegúrate de que BOT_TOKEN esté definido en el archivo .env.")



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