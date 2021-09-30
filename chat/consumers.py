import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'test_message',
                'tester':'This is the test'
            }
        )
    

    async def test_message(self, event):
        tester = event['tester']

        await self.send(text_data=json.dumps({
            'tester': tester
        }))

    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # async receive()
    
