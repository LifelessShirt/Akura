######################################
###################################### Color schema
######################################
class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    LIGHTGRAY = '\033[90m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

######################################
###################################### Playing music in the voice channels
######################################
async def playMusic(channel, glob, discord, asyncio):
    voice = await channel.connect()
    playlist = glob.glob("./music/*.mp3")
    while True:     
        for song in playlist: 
            # For testing on Windows:  
            # voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=f"{song}"))
            voice.play(discord.FFmpegPCMAudio(source=f"{song}"))
            print(f"{colors.CYAN}🎧 Playing :: {song}{colors.END}")
            while voice.is_playing():
                await asyncio.sleep(1)
            else:
                playMusic(channel, glob, discord, asyncio)

######################################
###################################### OpenAI
###################################### ChatGPT
######################################
async def chatgpt(temper, message, client):
    print(f"{colors.GRAY}ChatGPT generation starts here{colors.END}")
    try:
        completion = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                    {"role": "system", "content": temper},
                    {"role": "user", "content": message.content}
                ]
        )

        reply = completion.choices[0].message.content
        await message.reply(reply, mention_author=True)
        print("--------------------------------------")
        print(f" >> User {str(message.author)} speaks with Akurha.")
        print(f"{colors.CYAN}{str(message.author)}: {message.content} {colors.END}")
        print(f"{colors.BLUE}Akurha: {reply} {colors.END}")
        print("--------------------------------------")
    except:
        await message.reply("❌ Whoops!.\n There's an error, Senpai.\n\n Try again a little bit later.", mention_author=True)
        print(f"User {str(message.author)} tried to speak with Akurha, but there is an error.")