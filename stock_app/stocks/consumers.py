import json
import websocket
from channels.generic.websocket import AsyncWebsocketConsumer
from finnhub import Client
import asyncio

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.finnhub_client = Client(api_key ='d31dnfpr01qsprr0g9d0d31dnfpr01qsprr0g9dg')
        self.symbol = 'AAPL'
        self.ws = websocket.WebSocketApp(
            f'wss://ws.finnhub.io?token={self.finnhub_client.api_key}'
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close
        )
        self.ws.on_open = lambda ws: ws.send(json.dumps({'type': 'subscribe', 'symbol': self.symbol}))
        await asyncio.get_event_loop().run_in_executor(None, self.ws.run_forever)

    def on_message(self, ws, message):
        data = json.loads(message)
        if data.get('type') == 'trade':
            for trade in data['data']:
                price = trade['p']
                asyncio.run(self.send(text_data=json.dumps({
                    'symbol': self.symbol,
                    'price': price,
                    'timestamp': trade['t']
                })))
            # Salvar no banco (opcional)
                from .models import StockPrice
                StockPrice.objects.create(symbol=self.symbol, price=price)

    def on_error(self, ws, error):
        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket Closed")

    async def disconnect(self, close_code):
        self.ws.close()