import motor.motor_asyncio
from info import AUTH_CHANNELS, DATABASE_URI

class JoinReqs:

    def __init__(self):
        if DATABASE_URI:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
            self.db = self.client["JoinReqs"]
            self.collections = {str(channel): self.db[str(channel)] for channel in AUTH_CHANNELS}
        else:
            self.client = None
            self.db = None
            self.collections = None

    def isActive(self):
        return self.client is not None

    async def add_user(self, channel_id, user_id, first_name, username, date):
        try:
            if str(channel_id) in self.collections:
                await self.collections[str(channel_id)].insert_one({
                    "_id": int(user_id),
                    "user_id": int(user_id),
                    "first_name": first_name,
                    "username": username,
                    "date": date
                })
        except Exception as e:
            print(f"Error adding user to channel {channel_id}: {e}")

    async def get_user(self, channel_id, user_id):
        if str(channel_id) in self.collections:
            return await self.collections[str(channel_id)].find_one({"user_id": int(user_id)})

    async def get_all_users(self, channel_id):
        if str(channel_id) in self.collections:
            return await self.collections[str(channel_id)].find().to_list(None)

    async def delete_user(self, channel_id, user_id):
        if str(channel_id) in self.collections:
            await self.collections[str(channel_id)].delete_one({"user_id": int(user_id)})

    async def delete_all_users(self, channel_id):
        if str(channel_id) in self.collections:
            await self.collections[str(channel_id)].delete_many({})

    async def get_all_users_count(self, channel_id):
        if str(channel_id) in self.collections:
            return await self.collections[str(channel_id)].count_documents({})
