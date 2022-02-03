import discord
from discord_slash import SlashCommand
from discord.ext import commands
from PIL import ImageColor
from discord.utils import get
import pymongo

apiURI = 'mongodb://ALEX:rtXreOIhLVzGWIqz@cluster0-shard-00-00.mb4wu.mongodb.net:27017,cluster0-shard-00-01.mb4wu.mongodb.net:27017,cluster0-shard-00-02.mb4wu.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-y3m5i3-shard-0&authSource=admin&retryWrites=true&w=majority'
client = pymongo.MongoClient(apiURI)
dbname = "LDHBot"
db = client[dbname]
collection = db["Roles"]

# Subjects = ["Math", "English", "Science", "History", "Civics and Careers", "Computer Tech", "Computer Science", "Business", "Design Tech", "Communication Tech", "Arts", "Law", "Cooking", "French", "Biology", "Physics", "Chemistry", "Earth and Space Science", "Health Science"]
# color = [0x1A5BD1, 0xD11A1A, 0x40A53B, 0xDEAB1A, 0x4D2B2B, 0x4BA8DE, 0x104F0C, 0x5D29A7, 0x9A29A7, 0x53CA8F, 0xC4ED56, 0x8B8B8B, 0xA08BC5, 0xAB3131, 0x45573F, 0x2D2D2D, 0xE1C15B, 0x004CFF, 0xFFFFFF]
subjects = ["Math", "English", "Science", "History", "Civics and Careers", "Computer Tech", "Computer Science",
            "Business", "Design Tech", "Communication Tech", "Arts", "Law", "Cooking", "French", "Biology", "Physics",
            "Chemistry", "Earth and Space Science", "Health Science"]
subjectsEMOJI = ["Math", "English", "Science", "History", "CivicsandCareers", "ComputerTech", "ComputerScience",
                 "Business", "DesignTech", "CommunicationTech", "Arts", "Law", "Cooking", "French", "Biology",
                 "Physics",
                 "Chemistry", "EarthandSpaceScience", "HealthScience"]
colors = [0x1A5BD1, 0xD11A1A, 0x40A53B, 0xDEAB1A, 0x4D2B2B, 0x4BA8DE, 0x104F0C, 0x5D29A7, 0x9A29A7, 0x53CA8F, 0xC4ED56,
          0x8B8B8B, 0xA08BC5, 0xAB3131, 0x45573F, 0x2D2D2D, 0xE1C15B, 0x004CFF, 0xFFFFFF]
print(list(map(lambda x: str(x), colors)))
res = dict(zip(subjectsEMOJI, subjects))


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def delete_role(self, role_name, message):
        role_object = discord.utils.get(message.guild.roles, name=role_name)
        await role_object.delete()

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.channel.id == 936131045374459936 and message.author.id == 420417488283500576:
            # add reaction to message
            collection.update_one({"id": collection.find_one()["id"]}, {"$set": {"id": message.id}})
            print(collection.find_one())
            for i in subjectsEMOJI:
                emoji = discord.utils.get(message.guild.emojis, name=i)
                await message.add_reaction(emoji)
            if message.content == "create roles":
                guild = message.guild
                for i, j in enumerate(colors):
                    # await self.delete_role(j, message)
                    await guild.create_role(name=subjects[i], colour=discord.Colour(j))
                await message.channel.send("Roles Created")

    async def on_raw_reaction_add(self, payload):
        guild = await client.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        if user != client.user:
            if payload.message_id == collection.find_one()["id"]:
                try:
                    name = (str(payload.emoji).split(":")[1])
                    print(name)
                    role = get(guild.roles, name=res[name])
                    await user.add_roles(role)
                except (KeyError, IndexError) as e:
                    pass

    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == collection.find_one()["id"]:
            try:
                name = (str(payload.emoji).split(":")[1])
                print(name)
                guild = await client.fetch_guild(payload.guild_id)
                role = get(guild.roles, name=res[name])
                user = await guild.fetch_member(payload.user_id)
                await user.remove_roles(role)
            except (KeyError, IndexError) as e:
                pass


client = MyClient()

client.run("OTM4NDY2MzYyNzY0OTUxNTYy.Yfqs6A.QX2ToY6_YUKaekzsT8GeMw5kRVg")
