# Python Telegram TaskBot

## Spanish
La idea de este bot surge de la necesidad de mejorar la productividad mediante tareas y recordatorios, usando al mismo como herramienta para dicho fin.
Su funcionamiento es sencillo, se crean los usuarios que interactúan con el bot y se almacenan en el mismo, de forma que en caso de avería o reinicio se recurre a la persistencia de datos. 
El usuario dispondrá de los siguientes comandos para el uso del bot.

### Comandos del bot
/start -> Inicializa el bot y almacena al usuario y sus datos en un archivo JSON  
/help -> Muestra la lista de comandos del bot  
/addtask (nombre de la tarea) -> Añade una tarea como argumento tras el comando a la lista de tareas. Ej: /addtask Hacer la compra  
/showtasks -> Muestra la lista de tareas pendientes del usuario  
/comtask -> Muestra la lista de tareas pendientes y permite marcar las tareas realizadas como completadas  
/deltask -> Permite eliminar una tarea de la lista de tareas pendientes  
/reminder -> Establece un recordatorio los días seleccionados  
/deluser -> Elimina completamente al usuario del bot, con sus tareas y recordatorios  

