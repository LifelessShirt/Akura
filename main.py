# This example requires the 'members' privileged intents

import asyncio
import glob
from site import PREFIXES
import discord # type: ignore
import discordToken # type: ignore
import openaiToken # type: ignore
import addons as a  # type: ignore
from openai import OpenAI # type: ignore

from discord.ext import commands # type: ignore

ai_client = OpenAI(
  api_key=openaiToken.getToken()
)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist':'True'}


# --------------------------------
# Bot
# --------------------------------
class AkuraBot(discord.Client):
    # --------------------------------
    # Bot init
    # --------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Role on reaction def
        self.role_message_id = 1096225412373291068  # ID of the message that can be reacted to to add/remove a role.
        self.emoji_to_role = {
            discord.PartialEmoji(name='ic3o', id=1237421525217448066): 268472494250393606,
            discord.PartialEmoji(name='minecraft', id=1099074248213016757): 1388152894242685018,
        }

    # --------------------------------
    # Bot starts
    # --------------------------------
    async def on_ready(self):
        print(f'{a.colors.HEADER}Logged in as {self.user} (ID: {self.user.id}){a.colors.END}')
        print(f'{a.colors.HEADER}--------------------{a.colors.END}')

        await client.change_presence(activity=discord.CustomActivity(name='🌸 Being cute' ,emoji='🌸'))

        # Uncomment this to allow bot join music channel on bot start:
        #
        #ch = await client.fetch_channel("1388134429100216351")
        #await a.playMusic(ch, glob, discord, asyncio)

    # --------------------------------
    # Add role on reaction
    # --------------------------------
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.\
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally, add the role.
            print(f'{a.colors.GREEN}❇️ Give to user {payload.member.name} role {role}.{a.colors.END}')
            await payload.member.add_roles(role)
        except:
            # If we want to do something in case of errors we'd do it here.
            return
        
    # --------------------------------
    # Remove role on reaction
    # --------------------------------
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about.
        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            return

        try:
            # Finally, remove the role.
            await member.remove_roles(role)
        except discord.HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    # --------------------------------
    # Answer on messages
    # --------------------------------
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.channel.id == 1280075114003566602 or message.channel.id == 903533058135818281:
            if str(message.content.startswith('akura')).lower():
                await a.chatgpt("Your name is Akura. You are cute anime girl. Answer as sweetly as possible. Use 'Senpai' when addressing the user. Don't greet the user, the conversation has been going on for some time.", message, ai_client)
            elif str(message.content.startswith('акура')).lower():
                await a.chatgpt("Тебя зовут Акура. Ты милая аниме девочка. Отвечай максимально мило. Используй обращение семпай к пользователю. Не здоровайся с пользователем, беседа уже продолжается какое-то время.", message, ai_client)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

client = AkuraBot(intents=intents)
# --------------------------------
# Bot event (on voice channels update)
# --------------------------------
@client.event
async def on_voice_state_update(member, before, after):
    # Join "lofi music 🎧" when users connects
    #
    if after.channel is not None and member.id != 924376479289212998:
        channel = await client.fetch_channel("1388134429100216351")
        if after.channel == channel:
            try:
                print(f"{a.colors.GRAY}Connecting to {a.colors.CYAN}{channel}{a.colors.END}{a.colors.GRAY} voice channel...{a.colors.END}")
                await a.playMusic(channel, glob, discord, asyncio)
            except:
                print(f"{a.colors.GRAY}There is an Error while connecting to {a.colors.CYAN}{channel}{a.colors.END}{a.colors.GRAY} voice channel.\nMaybe I already has been connected?{a.colors.END}")
    # Leave "lofi music 🎧" if no users left
    #
    if before.channel is not None:
        channel = await client.fetch_channel("1388134429100216351")
        if before.channel == channel:
            if len(channel.members) == 1 and channel.members[0].id == 924376479289212998:
                await channel.members[0].guild.voice_client.disconnect()
                print(f"{a.colors.RED}Disconnected from {a.colors.CYAN}{channel}{a.colors.END}{a.colors.RED} voice channel{a.colors.END}")
client.run(discordToken.getToken())