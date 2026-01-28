from telegram import BotCommand

async def menu(application):
    commands = [
        BotCommand("start", "Registrarse en el sistema"),
        BotCommand("deluser", "Elimina tu usuario del sistema"),
        BotCommand("addtask", "Añade una nueva tarea"),
        BotCommand("showtasks", "Lista de tareas pendientes"),
        BotCommand("comtask", "Muestra la lista de tareas pendientes y permite marcar las tareas realizadas como completadas"),        
    ]

    await application.bot.set_my_commands(commands)

