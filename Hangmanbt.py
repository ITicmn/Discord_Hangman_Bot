import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Select
import random

bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is up and ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="hangman_info",description="Info for hangman")
async def hinfo(interaction:discord.Interaction):
    hembed=discord.Embed(title="Hangman Information",color=discord.Colour.random())
    hembed.set_author(name=f"ITicbt")
    hembed.set_thumbnail(url="https://play-lh.googleusercontent.com/Eg8Swxv4VMMs-l8r0yzCDVX-Mr6RZiztBFieLfdjH9c5Apn4BoOJT4sMC5Vx5gNnfg")
    hembed.add_field(name="How to play",value="One player thinks of a word and the other tries to guess it by guessing letters. Each incorrect guess brings you closer to being hanged.",inline=False)
    hembed.add_field(name="Commands:",value="",inline=False)
    hembed.add_field(name="/hangman_game_start:",value="Start the game",inline=False)
    hembed.add_field(name="/hangman_game_start:",value="Set the word",inline=False)
    hembed.add_field(name="/hangman_guess_letter:",value="Guess the letter",inline=False)
    hembed.add_field(name="/hangman_quit:",value="Quit game",inline=False)
    hembed.add_field(name="/hangman_restart:",value="Restart game",inline=False)
    hembed.set_footer(text=f"Made by Hangbt")

    await interaction.response.send_message(f"Here's the information!",embed=hembed)

@bot.tree.command(name="hangman_set_word",description="Set a word and duel someone")
@app_commands.describe(word="The word you want to set")
async def hset(interaction:discord.Interaction,word:str,member:discord.Member = None):
    global qword,aword,hngs
    if (hngs==False):
        aword=word
        qword=''
        qword+='-' * len(word)
        if (member==None):
            await interaction.response.send_message(f"Word has been set to {qword}")
        elif (member!=None):
            await interaction.response.send_message(f"<@{member.id}> word has been set to {qword}")
    elif (hngs==True):
        await interaction.response.send_message(f"Game already started")

@bot.tree.command(name="hangman_game_start",description="Start a hangman game")
async def hgame(interaction:discord.Interaction):
    global qword,hngs,hsteps,hlose,hwin
    if (hngs==False and qword!=None):
        hngs=True
        hlose=False
        hwin=False
        hsteps=1 
        await interaction.response.send_message(f"Game Start!")
    elif (hngs==True):
        await interaction.response.send_message(f"Game already started")

@bot.tree.command(name="hangman_guess_letter",description="Guess the letter of hangman")
@app_commands.describe(letter="Letter you guess")
async def gletter(interaction:discord.Interaction,letter:str):
    global qword,aword,gembed,hngs,hsteps,hfile,qlist,qsame,hlose,hwin
    if (hngs==True):
        qsame=False
        qlist=list(qword)
        if (len(letter)==1):
            for i in range(0,len(aword)):
                if (aword[i]==letter):
                    qsame=True
                    qlist[i]=letter
                    qword="".join(qlist)
        gembed=discord.Embed(title="Hangman",color=discord.Colour.blue())
        gembed.add_field(name="Word:",value=f"{qword}")
        if (qword==aword):
            hwin=True
            hngs=False
        if (qsame==False):
            hsteps=hsteps+1
        if (hsteps==1):
            hfile = discord.File("hangman\hangman0.jpg",filename="image.jpg")
        elif (hsteps==2):
            hfile = discord.File("hangman\hangman1.jpg",filename="image.jpg")
        elif (hsteps==3):
            hfile = discord.File("hangman\hangman2.jpg",filename="image.jpg")
        elif (hsteps==4):
            hfile = discord.File("hangman\hangman3.png",filename="image.png")
        elif (hsteps==5):
            hfile = discord.File("hangman\hangman4.png",filename="image.png")
        elif (hsteps==6):
            hfile = discord.File("hangman\hangman5.png",filename="image.png")
        elif (hsteps==7):
            hfile = discord.File("hangman\hangman6.png",filename="image.png")
        elif (hsteps==8):
            hfile = discord.File("hangman\hangman7.png",filename="image.png")
        elif (hsteps==9):
            hfile = discord.File("hangman\hangman8.png",filename="image.png")
        elif (hsteps==10):
            hfile = discord.File("hangman\hangman9.png",filename="image.png")
        elif (hsteps==11):
            hfile = discord.File("hangman\hangman10.png",filename="image.png")
            hngs=False
            hlose=True
        if (hsteps<=3):
            gembed.set_image(url="attachment://image.jpg")
        elif (hsteps>=4):
            gembed.set_image(url="attachment://image.png")
        if (hlose==True):
            await interaction.response.send_message(f"You lost!",file=hfile,embed=gembed)
        elif (hwin==True):
            await interaction.response.send_message(f"You win!",file=hfile,embed=gembed)
        elif (hlose==False and hwin==False):
            await interaction.response.send_message(file=hfile,embed=gembed)
    elif (hngs==False and hlose==False):
        await interaction.response.send_message(f"Game not started")
    elif (hngs==False and hlose==True):
        await interaction.response.send_message(f"You lost")
    elif (hngs==False and hwin==True):
        await interaction.response.send_message(f"You won")

@bot.tree.command(name="hangman_quit",description="Quit game")
async def hq(interaction:discord.Interaction):
    global hngs,hquit
    if (hngs==True):
        hquit=True
        hngs=False
        await interaction.response.send_message(f"Game stopped")

@bot.tree.command(name="hangman_restart",description="Restart game")
async def hrestart(interaction:discord.Interaction):
    global hngs,hlose,hwin,hquit
    if (hngs==False and hwin==True or hngs==False and hlose==True or hngs==False and hquit==True):
        hngs=True
        hsteps=1
        await interaction.response.send_message(f"Game restarted")
    if (hngs==True or hngs==False and hwin==False and hlose==False and hquit==False):
        await interaction.response.send_message(f"Game can't be restarted")

bot.run("TOKEN")
