from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doc_id = self.scope['url_route']['kwargs']['doc_id']
        self.group_name = f"editor_{self.doc_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content", "")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_update",
                "content": content,
            }
        )

    async def send_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "update",
            "content": event["content"]
        }))
