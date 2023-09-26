import websocket
import _thread
import time
import rel
import json
from Tool import ts_check,bar_checker,convert_date
from twilio.rest import Client
from os import environ


print(str(environ.get("Web_socket_Api")))
# SMS Configuration 
account_sid = str(environ.get('account_sid'))
auth_token = str(environ.get('auth_token'))
client = Client(account_sid, auth_token)

def send_message(alert_time):
    message = client.messages.create(
    from_='+18338220538',
    body='NASDAQ ALert at '+ str(alert_time),
    to='+18507608802')
    print(message.sid)
# End of  SMS Configuration

def on_message(ws, message):
    #print(message)
    ms_json = json.loads(message)
    # Make sure the Event is V - To avoid Status Message
    if ms_json[0]['ev'] == "AM" :
        
        #Get timestamp 
        ts = int(ms_json[0]['e'])
        if ts_check(ts) == True :
            # get closing price and H 
            op = ms_json[0]['o']
            cp = ms_json[0]['c']
            hp = ms_json[0]['h']
            lp = ms_json[0]['l']
            if bar_checker(op,cp,hp,lp) == True :
                alert_time = convert_date(ms_json[0]['e'])
                print ("Found One")
                send_message(alert_time)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
    #Authenticate 
    auth_data = {"action":"auth","params":str(environ.get("Web_socket_Api"))}
    ws.send(json.dumps(auth_data))
    indice_data = {"action":"subscribe", "params":"AM.I:NDX"}
    ws.send(json.dumps(indice_data))
if __name__ == "__main__":
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://socket.polygon.io/indices",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel,suppress_origin=True, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()