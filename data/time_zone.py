import datetime
import pytz

#TIME ZONE
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
ZONE = pytz.timezone("Europe/Madrid")
time = datetime.time(hour=0, minute= 0, second=0, tzinfo=ZONE)