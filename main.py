import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler


#LOCAL IMPORTS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
import persistence
from basic_functions import start, help
from task_functions import add_task, delete_task, show_pending_tasks


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
    app = ApplicationBuilder().token(BOT_TOKEN).build()


    #Handlers
    #---------------------------------------------------------------------------------------------------
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("addtask", add_task))
    app.add_handler(CommandHandler("deltask", delete_task))
    app.add_handler(CommandHandler("showtasks", show_pending_tasks))
   
   #---------------------------------------------------------------------------------------------------
    app.run_polling()



#BOT RUNNING
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
#If scripts's name match with 'main', bot starts
if __name__ == "__main__":
    main()