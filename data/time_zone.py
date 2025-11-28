import datetime
import pytz

#TIME ZONE
#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
ZONE = pytz.timezone("Europe/Madrid")
time = datetime.time(hour=12, minute= 24, second=0, tzinfo=ZONE)