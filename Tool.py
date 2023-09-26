from datetime import datetime
import pytz 
from datetime import datetime

def convert_date(ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
    # Filter By time to Avoid sending Alerts at bad time of the day 
    # From 8:00 AM to 16:00 PM
    if date_obj.hour < 15 and date_obj.hour >= 8 : 
        formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
        return str(date_obj.hour) + ":"+ str(date_obj.minute)
    return 0 
def ts_check(ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
    # Filter By time to Avoid sending Alerts at bad time of the day 
    # From 8:00 AM to 16:00 PM
    if date_obj.hour < 15 and date_obj.hour >= 8 :
        #Only take mns that are divisible by 4  
        formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
        if date_obj.minute % 5 == 0 :
            return True 
        else: 
            return False 
    #     # return str(formated_date)
    #     match date_obj.minute:
    #         case 4 :
    #             if date_obj.second == 59:
    #                 return True
    #         case 9 : 
    #             if date_obj.second == 59:
    #                 return True
    #         case 14:
    #             if date_obj.second == 59:
    #                 return True
    #         case 19 :
    #             if date_obj.second == 59:
    #                 return True
    #         case 24 : 
    #             if date_obj.second == 59:
    #                 return True
    #         case 29 :
    #             if date_obj.second == 59:
    #                 return True
    #         case 34 :
    #              if date_obj.second == 59:
    #                 return True
    #         case 39 : 
    #             if date_obj.second == 59:
    #                 return True
    #         case 44 : 
    #             if date_obj.second == 59:
    #                 return True
    #         case 49 :
    #             if date_obj.second == 59:
    #                 return True
    #         case 54 :
    #             if date_obj.second == 59:
    #                 return True
    #         case 59 : 
    #             if date_obj.second == 59:
    #                 return True
    # else :
    #     return False
def bar_checker (op,cp,hp,lp):
     if hp == cp  or lp == cp:
         return True
