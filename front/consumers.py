import json
import aiohttp
from channels.generic.websocket import AsyncWebsocketConsumer
from config.settings import CURRENT_HOST


class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "comments"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "fetch_comments":
            comments = await self.get_comments_from_api()
            await self.send(text_data=json.dumps({"comments": comments}))

    async def get_comments_from_api(self):
        async with aiohttp.ClientSession() as session:
            headers = {"Host": CURRENT_HOST}
            async with session.get(
                    f"http://web:8000/api/v1/comments/comments/?ordering=-rating",
                    headers=headers) as response:
                return await response.json()

    async def notify_clients(self):
        comments = await self.get_comments_from_api()
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_update",
                "comments": comments
            }
        )

    async def send_update(self, event):
        await self.send(text_data=json.dumps({"comments": event["comments"]}))
