import json

from channels.generic.websocket import AsyncWebsocketConsumer

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'stock_updates'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print("entrou")
    async def disconnect(self,close_code):
        # Remove o consumer do grupo ao desconectar
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("disconnect")

    # Método que recebe as mensagens do Channel Layer
    async def stock_update(self, event):
        message = event['message']
        # Envia a mensagem para o cliente via WebSocket
        await self.send(text_data=json.dumps({
            'type': 'stock_update',
            'data': message
        }))
        print(event)

