import json
import os
import atexit

#REGISTER USERS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

USERS_DATA_FILE = "json/users_data.json"
REGISTERED_USERS = {} #User data store on a dictionary

USERS_TASK_LIST = "json/task_list.json"
TASKLIST = {} #users tasklist stored on a dictionary

USERS_REMINDERS_FILE = "json/reminders.json"
REMINDERS = {}

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def load_users():
    global REGISTERED_USERS
    if os.path.exists(USERS_DATA_FILE):
        try:
            with open(USERS_DATA_FILE, "r") as f:

                content = f.read().strip()
                if not content:
                    print(f"DEBUG: {USERS_DATA_FILE} está vacío.")
                    return

                data_from_json = json.loads(content)
                REGISTERED_USERS = {int(k): v for k, v in data_from_json.items()}
                print(f" Datos cargados: {len(REGISTERED_USERS)} usuarios en memoria.")

        except json.JSONDecodeError:
            print(" Error al leer el archivo JSON. Iniciando con diccionario vacío.")



def save_users():
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

def load_tasklist():
    global TASKLIST
    if os.path.exists(USERS_TASK_LIST):
        try:
            with open(USERS_TASK_LIST, "r") as f:

                content = f.read().strip()
                if not content:
                    print(f"DEBUG: {USERS_TASK_LIST} está vacío.")
                    return


                data_from_json = json.loads(content)
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

#REGISTERES USERS' REMINDERS
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def load_reminders():
    global REMINDERS

    if os.path.exists:
        try:
            with open(USERS_REMINDERS_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    print(f"DEBUG: {USERS_REMINDERS_FILE} está vacío.")
                    return
                
                data_from_json = json.loads(content)
                REMINDERS= {int(k): v for k, v in data_from_json.items()}
                print(f"Recordatorios cargados de {len(REMINDERS)} usuarios")
        except json.JSONDecodeError:
            print(f"Error al cargar los recordatorios")

def save_reminders():
    global REMINDERS
    
    try:
        with open(USERS_REMINDERS_FILE, "w") as f:
            json.dump(REMINDERS,f, indent=4)
            print(f"Recordarios guardados de len({REMINDERS} usuarios)")

    except Exception as e:
        print(f"Error al guardar los recordatorios {e}")
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------

def load_data():
    load_users()
    load_tasklist()
    load_reminders()

atexit.register(save_users)
atexit.register(save_tasklist)
atexit.register(save_reminders)