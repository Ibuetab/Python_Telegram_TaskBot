from telegram import Update


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


    
async def delete_task(update:Update, context):

    chat_id = update.effective_chat.id

    task = " ".join(context.args)

    if chat_id in persistence.TASKLIST:
        user_tasklist = persistence.TASKLIST[chat_id]
        if task not in user_tasklist:
            await context.bot.send_message(chat_id=chat_id, text=f"{task} no existe en la lista de tareas")
        
        else:
            persistence.TASKLIST[chat_id].remove(task)
            await context.bot.send_message(chat_id=chat_id, text=f"La tarea {task} ha sido eliminada")

    else:
    
        await context.bot.send_message(chat_id=chat_id, text=f"Usa el comando /start primero")


async def show_pending_tasks(update:Update, context):

    chat_id = update.effective_chat.id

    if chat_id in persistence.TASKLIST:
        await context.bot.send_message(chat_id=chat_id, text=f"Tienes las siguientes tareas pendientes: ")
        
        for task in persistence.TASKLIST[chat_id]["pending_tasks"]:
            await context.bot.send_message(chat_id=chat_id, text=f"{task}")
    
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"Usa el comando /start primero")