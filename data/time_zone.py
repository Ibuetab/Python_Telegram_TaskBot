import datetime
import pytz

#TIME ZONE
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
ZONE = pytz.timezone("Europe/Madrid")
time = datetime.time(hour=0, minute= 0, second=0, tzinfo=ZONE)


DIAS = {
    "LU": 0, "MA": 1, "MI": 2, "JU": 3, 
    "VI": 4, "SA": 5, "DO": 6
}