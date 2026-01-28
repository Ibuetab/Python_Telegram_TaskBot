import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters


#LOCAL IMPORTS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
import data.persistence as persistence
from data.time_zone import ZONE, DIAS
from functions.basic_functions import start, help, delete_user
from functions.task_functions import TASK_NAME, DELETE, COMPLETE
from functions.task_functions import new_task, add_task, show_pending_tasks, delete_task, delete_button, cancel, complete_task, complete_button
from functions.reminders_functions import NAME,DAY,HOUR,MINUTE
from functions.reminders_functions import reminder_name, get_reminder_name, get_day_frequency_buttons, get_hour, get_minute, save_and_finish
from functions.menu import menu

#BOT TOKEN
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("El token de Telegram no se encontró. Asegúrate de que BOT_TOKEN esté definido en el archivo .env.")


#MAIN FUNCTION
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#Main function. Build the bot and store handlers
def main():
    #---------------------------------------------------------------------------------------------------
    persistence.load_data() #load user´s data
  
    #---------------------------------------------------------------------------------------------------
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(menu).build()


    #Handlers
    #---------------------------------------------------------------------------------------------------
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("showtasks", show_pending_tasks))
    app.add_handler(CommandHandler("deluser", delete_user))



    #Conversation Handlers
    #---------------------------------------------------------------------------------------------------
    add_task_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("addtask", new_task)],
        states = {
            TASK_NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), add_task)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False)
    
    
    del_task_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("deltask", delete_task)],
        states = {
            DELETE: [CallbackQueryHandler(delete_button)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False)
    
    complete_task_handler = ConversationHandler(
        entry_points=[CommandHandler("comtask", complete_task)],
        states = {
            COMPLETE: [CallbackQueryHandler(complete_button)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False)
    
      
    reminder_handler = ConversationHandler(
        entry_points=[CommandHandler("reminder", reminder_name)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_reminder_name)],
            DAY: [CallbackQueryHandler(get_day_frequency_buttons)],
            HOUR: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_hour)],
            MINUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_minute)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False)
    
    
    app.add_handler(add_task_conv_handler)
    app.add_handler(del_task_conv_handler)
    app.add_handler(complete_task_handler)
    app.add_handler(reminder_handler)

   
   #---------------------------------------------------------------------------------------------------
    app.run_polling()



#BOT RUNNING
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#If scripts's name match with 'main', bot starts
if __name__ == "__main__":
    main()