import discord
from discord.channel import VoiceChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from youtube_dl import YoutubeDL
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time
from selenium.webdriver.chrome.service import Service
service=Service(r"C:\Users\jaemi\OneDrive\문서\재민\깃헙\zzzzz\zzzzz")

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connect was successful')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command()
async def 들어와(ctx):   
    try: 
        global vc 
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await VoiceChannel.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속하여 있지 않습니다.")  

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("이미 그 채널에 접속하여 있지 않습니다.") 

@bot.command()
async def URL재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")


@bot.command()
async def 일시정지(ctx):
    if not bot.voice_clients[0].is_paused():
        bot.voice_clients[0].pause()
    else:
        await ctx.send("이미 중지되었습니다.")    

@bot.command()
async def 다시재생(ctx):
    if bot.voice_clients[0].is_paused():
        bot.voice_clients[0].resume()
    else:
        await ctx.send("이미 재생 중입니다.")

@bot.command()
async def 정지(ctx):
    if bot.voice_clients[0].is_playing():
        bot.voice_clients[0].stop()
    else:
        await ctx.send("재생 중이지 않습니다.")   

@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        driver = webdriver.Chrome(executable_path=r'C:\Users\jaemi\OneDrive\문서\재민\깃헙\zzzzz\zzzzz')    
        chromedriver_dir = r"C:\Users\jaemi\OneDrive\문서\재민\깃헙\zzzzz\zzzzz"
        driver = webdriver.Chrome(chromedriver_dir)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없습니다.")


                   
bot.run('ODk4ODgzMzA1NDAxODk2OTgx.YWqsUA.vKqoRuPLaccH7V9h87KzSVkKDGU')