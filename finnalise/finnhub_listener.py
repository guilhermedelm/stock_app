import os 
import json 
import asyncio
from websocket import create_connection
import websocket
print('inciando')
#Acesso ao projeto Django para trocar dados
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finnalise.settings')
import django
django.setup()
print('django')

from channels.layers import get_channel_layer
# Configura o Channel Layer para ser usado neste script
channel_layer = get_channel_layer()
# Define o nome do grupo para o qual o processo enviará mensagens
group_name = 'stock_updates' 
print('stock_layer')

async def send_to_channel_layer(message_data):
    await channel_layer.group_send(
        group_name,
        {
            'type': 'stock.update',
            'message': message_data
        }
    
    )

def on_message(ws, message):
    data = json.loads(message)
    if 'type' in data and data['type'] == 'ping':
        return

    if 'data' in data:
        for item in data['data']:
            asyncio.run(send_to_channel_layer(item))
            print(f"Enviando para o Channel Layer: {item}")


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    print('conectado')

def on_error(ws,error):
    print(error)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=d31dnfpr01qsprr0g9d0d31dnfpr01qsprr0g9dg",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
    
    '''ws = create_connection("wss://ws.finnhub.io?token=d31dnfpr01qsprr0g9d0d31dnfpr01qsprr0g9dg")
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_close = on_close'''
    
    # Loop de escuta que fica rodando para receber dados
    while True:
        try:
            message = ws.recv()
            on_message(ws, message)
        except Exception as e:
            print(f"Erro: {e}")
            break