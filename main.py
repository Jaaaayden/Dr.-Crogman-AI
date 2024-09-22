from typing import Final
import os 
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# load token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN') # key
# print(TOKEN)

# bot setup
intents: Intents = Intents.default()
intents.message_content = True #NOQA

discordClient: Client = Client(intents=intents)

# message func
async def send_message(message: Message, user_message: str, username: str, channel: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled)')
        return
    
    try:
        response: str = get_response(user_message, username, channel)
        await message.channel.send(response)
    except Exception as e: # bad practice but it works
        print(e) # use logging later
        
@discordClient.event
async def on_ready() -> None:
    print(f'{discordClient.user} is now running!')
    
@discordClient.event
async def on_message(message: Message) -> None:
    if message.author == discordClient.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)
    
    print(f'[{channel}] {username}: "{user_message}"')
    await send_message(message, user_message, username, channel)
    
def main() -> None:
    discordClient.run(token = TOKEN)
    
if __name__ == '__main__': # useful when calling
    main()