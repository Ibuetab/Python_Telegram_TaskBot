import datetime
import pytz

#TIME ZONE
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
ZONE = pytz.timezone("Europe/Madrid")
time = datetime.time(hour=0, minute= 0, second=0, tzinfo=ZONE)


DIAS = {
    "LU": 1, 
    "MA": 2, 
    "MI": 3, 
    "JU": 4, 
    "VI": 5, 
    "SA": 6, 
    "DO": 0
}