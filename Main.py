import ApiConfig
from datetime import datetime
import pytz
from twilio.rest import Client

# SMS Configuration 
account_sid = 'AC4769a5c2b9176a0419ed2c27f96d5e39'
auth_token = 'ef484f8fff592f160144c1b93c8bd949'
client = Client(account_sid, auth_token)
# Api Config 
indice = ApiConfig.ApiAccess()
data = indice.get_5mn_data("I:NDX",5)

# Trading Account Structure

initial_amount     = 100000    # 100k Account Size 
currently_in_trade = False     # 0 No trade in place 1 Trade placed 
long_position      = False     # 
short_position     = False     #
borrow_price       = 0         # Short Selling
buy_price          = 0         # Long Position 
bar_counter        = 0         # 0 by default - Max Exit bar is 5 - or 55 Pts
entry_time         = 0         # Timestamp  

def send_message(ticker_data):
    message = client.messages.create(
    from_='+18338220538',
    body='Yoo Test',
    to='+18507608802')
    print(message.sid)
def convert_date(ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
    # Filter By time to Avoid sending Alerts at bad time of the day 
    # From 8:00 AM to 16:00 PM
    if date_obj.hour < 15 and date_obj.hour >= 8 : 
        formated_date = date_obj.strftime('%Y-%m-%d %H:%M:%S  %Z %z')
        return str(formated_date)
    return 0 
def print_trade_result(ticker,WL,pnl,ts):
    timestamp = ts/1000.0
    date_obj = datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('America/Chicago'))
    print(str(ticker)+"!"+str(WL)+"!"+ str(pnl)+"!"+str(date_obj.year)
          +"!"+str(date_obj.month)+"!"+ str(date_obj.day) + "!"+
          str(date_obj.hour)+"!"+ str(date_obj.minute))

def go_short():
    global initial_amount,currently_in_trade,long_position,short_position,borrow_price,bar_counter
    for x in data:
            if x.low == x.close and not currently_in_trade : 
                temp_date = convert_date(x.timestamp)
                if temp_date != 0 :
                    #send_message(x)
                    # Open Short Position - SELL
                    currently_in_trade = True
                    short_position     = True
                    borrow_price       = x.close
                    
            elif currently_in_trade:
                # Check if we have reached the max bar length
                if bar_counter < 5 :
                    if short_position is True: 
                        # Check for a 50pts difference for 1st Exit 
                        pnl = borrow_price - x.close 
                        # Stop Loss is 50 pts, if lower than -50pts exit the trade  
                        if pnl <= -50 :
                            initial_amount += pnl
                            print_trade_result("NDX","L",pnl,x.timestamp) 
                            #print ("Trade Exited L : Loss of "+ str(pnl) + "pts")
                            # Set everything back to default
                            currently_in_trade = False 
                            bar_counter        = 0 
                            short_position     = False 
                            borrow_price       = 0
                        # First Target 50 pts     
                        elif pnl >= 50:
                            initial_amount += pnl
                            print_trade_result("NDX","W",pnl,x.timestamp) 
                            #print ("Trade Exited Win : Profit of "+ str(pnl) + "pts")
                            currently_in_trade = False
                            bar_counter        = 0
                            short_position     = False
                            borrow_price       = 0
                        # Move to the next bar          
                        bar_counter+=1 
                elif bar_counter == 5:
                    # Exit trade after 5 Bars 
                    pnl = borrow_price - x.close
                    initial_amount += pnl 
                    # If trade is Positive - W 
                    if pnl > 0 :
                        print_trade_result("NDX","W",pnl,x.timestamp) 
                        #print ("Trade Exited Win : Profit of "+ str(pnl) + "pts")
                    else:
                        print_trade_result("NDX","L",pnl,x.timestamp)  
                        #print ("Trade Exited L : Loss of  "+ str(pnl) + "pts")
                    borrow_price = 0    
                    bar_counter = 0
                    currently_in_trade = False
                    short_position     = False 

    print("Account Summary after trades: "+ str(initial_amount))
def go_long():
    global initial_amount,currently_in_trade,long_position,short_position,buy_price,bar_counter,entry_time
    for x in data:
            if x.high == x.close  and not currently_in_trade : 
                temp_date = convert_date(x.timestamp)
                if temp_date != 0 :
                    #send_message(x)
                    # Open LONG Position - BUY
                    currently_in_trade = True
                    entry_time         = x.timestamp
                    long_position      = True
                    buy_price          = x.close
                    
            elif currently_in_trade:
                # Check if we have reached the max bar length
                if bar_counter < 5 :
                    if long_position is True: 
                        # Check for a 50pts difference for 1st Exit 
                        pnl = x.close - buy_price
                        # Stop Loss is 50 pts, if lower than -50pts exit the trade  
                        if pnl <= -50 :
                            initial_amount += pnl
                            print_trade_result("NDX","L",pnl,entry_time) 
                            #print ("Trade Exited L : Loss of "+ str(pnl) + "pts")
                            # Set everything back to default
                            currently_in_trade = False
                            entry_time         = 0 
                            bar_counter        = 0 
                            long_position      = False 
                            buy_price          = 0

                        # First Target 50 pts     
                        elif pnl >= 50:
                            initial_amount += pnl
                            print_trade_result("NDX","W",pnl,entry_time) 
                            #print ("Trade Exited Win : Profit of "+ str(pnl) + "pts")
                            currently_in_trade = False
                            entry_time         = 0
                            bar_counter        = 0
                            long_position      = False
                            buy_price          = 0
                        # Move to the next bar          
                        bar_counter+=1 
                elif bar_counter == 5:
                    # Exit trade after 5 Bars 
                    pnl = x.close - buy_price
                    initial_amount += pnl 
                    # If trade is Positive - W 
                    if pnl > 0 :
                        print_trade_result("NDX","W",pnl,entry_time) 
                        #print ("Trade Exited Win : Profit of "+ str(pnl) + "pts")
                    else:
                        print_trade_result("NDX","L",pnl,entry_time)  
                        #print ("Trade Exited L : Loss of  "+ str(pnl) + "pts")
                    buy_price          = 0    
                    bar_counter        = 0
                    currently_in_trade = False
                    entry_time         = 0
                    long_position      = False 

    print("Account Summary after trades: "+ str(initial_amount))

go_short()
#go_long()
