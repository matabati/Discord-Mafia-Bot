from asyncio.windows_events import NULL
import random
from re import I
from typing import Counter
from urllib import response
import hikari
import lightbulb


import requests


## function that gets the random quote
def get_random_quote():
	try:
		## making the get request
		response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
		if response.status_code == 200:
			## extracting the core data
			json_data = response.json()
			data = json_data['data']

			## getting the quote from the data
			return data[0]['quoteText']
		else:
			print("Error while getting quote")
	except:
		print("Something went wrong! Try Again!")

#global dictZ

GameState = {'Mode': [],
            'Timer':[],
            'Players': { }
}


Players = {'PlayerNumber' : [],
            'PlayerUserID' : [],
            'PlayerName' : [],
            'PlayerState' : { }
}

PlayerState = {'Role': [],
                'isDead' : [],
                'hasGun' : [],
                'detectiveRole' : [],
                'detectiveJob' : [],
                'isHealed' : [],
                'isHostage' : [],
                'isGuarded': [],
                'isShot' : []
}


Rolez = {'Name' : ["GodFather","Doctor","Karagah","MafiaSimple","ShahrvandSimple","Tofangdar","Nato","Takavar","GroganGir","Negahban"],
        'Count' : []
}
RolezBa = {'Name' : ["GodFather","Doctor","Karagah","MafiaSimple","ShahrvandSimple","Tofangdar","Nato","Takavar","GroganGir","Negahban"],
        'Count' : []
}

mylist = []

j = 0
is_night = 0

#bot token
bot = lightbulb.BotApp(token='MTAwMzY3MTIwMjc0Njg2MzY2Ng.GzDqa6.l3R_1dKb9flXHwq9vwSk2c-jBHav44gnv28p3E')


#bot setting
@bot.listen(hikari.GuildMessageCreateEvent)
async def print_message(event):
    print(event.content)

#bot setting for dm messages
@bot.listen(hikari.DMMessageCreateEvent)
async def print_message(event):
    print("night state is : ",is_night)
    if (is_night==1):
        print(event.author_id)
        i = Players['PlayerUserID'].index(event.author_id)
        res = (event.content).split()
        if(PlayerState['Role'][i]=="GroganGir"):
            PlayerState['isHostage'][int(res[0])-1] = 1
        if(PlayerState['Role'][i]=="Negahban"  and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            PlayerState['isGuarded'][int(res[0])-1] = 1
            PlayerState['isHostage'][int(res[0])-1] = 0
        if(PlayerState['Role'][i]=="Doctor" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            PlayerState['isHealed'][int(res[0])-1] = 1
            PlayerState['isDead'][int(res[0])-1] = 0
        if(PlayerState['Role'][i]=="Karagah" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            PlayerState['detectiveJob'][int(res[0])-1] = 1
            global j
            j = int(res[0])-1
            print("hi")
            print(j)
        if(PlayerState['Role'][i]=="GodFather"):
            if not PlayerState['isHealed'][int(res[0])-1]:
                PlayerState['isDead'][int(res[0])-1] = 1
        if(PlayerState['Role'][i]=="Tofangdar" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            PlayerState['hasGun'][int(res[0])-1] = res[1]
            mylist.append(int(res[0])-1)
        if(PlayerState['Role'][i]=="Nato"):
            if (PlayerState['Role'][int(res[0])-1] == res[1]):
                PlayerState['isDead'][int(res[0])-1] = 1
        if(PlayerState['Role'][i]=="Takavar"):
            if (PlayerState['Role'][int(res[0])-1]=="GodFather"):
                PlayerState['isDead'][i] = 0
            if (PlayerState['detectiveRole'][int(res[0])-1]==1 ):
                PlayerState['isDead'][i] = 0
                PlayerState['isDead'][int(res[0])-1] = 1
    
    Players['PlayerState'].update(PlayerState)
    GameState['Players'].update(Players)
    print(GameState)

#bot starting event
@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print("bot has started")

#hi DONE
@bot.command
@lightbulb.command('astart','welcome to new game!')
@lightbulb.implements(lightbulb.SlashCommand)
async def mode(ctx):
    await ctx.respond('Which mode do u wanna play?\n1- Normal ( boo! boring! )\n2- Reza mode ( Pro B) )\nYou have to choose "gamemode" command.\nThen join to game.\nYou can see players name by "player" command.\nThen type roles and Initialize and at the end!\nType "firstnight" when you want mafias to know each other.\nnight begin by "night" and nightactions by "day"!')

#game mode DONE
@bot.command
@lightbulb.option('num','modenumber',type=int)
@lightbulb.option('time','time of nights',type=int)
@lightbulb.command('gamemode','result')
@lightbulb.implements(lightbulb.SlashCommand)
async def res(ctx):
    number = ctx.options.num
    timer = ctx.options.time
    if (number < 3 and number > 0):
        GameState['Mode'].append(number)
        GameState['Timer'].append(timer)
        await ctx.respond('Now its time to join!')
    else:
        await ctx.respond('Are u OSKOL or something?')
        

#join the game DONE
@bot.command
@lightbulb.command('join','join the game!')
@lightbulb.implements(lightbulb.SlashCommand)
async def join(ctx):
    if ctx.author.id not in Players['PlayerUserID']:
        Players['PlayerNumber'].append(len(Players['PlayerNumber'])+1)
        Players['PlayerName'].append(ctx.author.username)
        Players['PlayerUserID'].append(ctx.author.id)
        Players['PlayerState'].update(PlayerState)
        GameState['Players'].update(Players)
        await ctx.respond('u have been joined!')
    else:
        await ctx.respond('u have already joined! Dont spam me. Dont u have KAR O ZENDEGI?!')


#roles DONE
@bot.command
@lightbulb.option('negahban','negahban',type=int)
@lightbulb.option('grogan_gir','grogan gir',type=int)
@lightbulb.option('takavar','takavar',type=int)
@lightbulb.option('nato','nato',type=int)
@lightbulb.option('mafia_simple','mafia simple',type=int)
@lightbulb.option('shahrvand_simple','shahrvand simple',type=int)
@lightbulb.option('tofangdar','tofangdar',type=int)
@lightbulb.option('karagah','karagah',type=int)
@lightbulb.option('doctor','doctor',type=int)
@lightbulb.option('god_father','god father',type=int)
@lightbulb.command('roles','see list of roles:')
@lightbulb.implements(lightbulb.SlashCommand)
async def roles(ctx):
    Rolez['Count'] = [ctx.options.god_father,ctx.options.doctor,ctx.options.karagah,ctx.options.mafia_simple,ctx.options.shahrvand_simple,ctx.options.tofangdar,ctx.options.nato,ctx.options.takavar,ctx.options.grogan_gir,ctx.options.negahban]
    RolezBa['Count'] = [ctx.options.god_father,ctx.options.doctor,ctx.options.karagah,ctx.options.mafia_simple,ctx.options.shahrvand_simple,ctx.options.tofangdar,ctx.options.nato,ctx.options.takavar,ctx.options.grogan_gir,ctx.options.negahban]
    print(Rolez)
    await ctx.respond('Got it!')
    

#players DONE
@bot.command
@lightbulb.command('players','players name and number list')
@lightbulb.implements(lightbulb.SlashCommand)
async def players(ctx):
    text = ""
    if len(Players['PlayerNumber'])>0:
        for i in range(len(Players['PlayerNumber'])):
            text = text + str(Players['PlayerNumber'][i]) + ' : ' + str(Players['PlayerName'][i]) +'\n'
        await ctx.respond(text)
    else:
        await ctx.respond("AMAT")

#playersstate DONE
@bot.command
@lightbulb.command('playerstate','players name and there state')
@lightbulb.implements(lightbulb.SlashCommand)
async def players(ctx):
    text = ""
    if len(Players['PlayerNumber'])>0:
        for i in range(len(Players['PlayerNumber'])):
            text = text + str(Players['PlayerNumber'][i]) + ' : ' + str(Players['PlayerName'][i]) + ' : '
            if (PlayerState['isDead'][i]==0):
                text = text +  'Alive' + '\n'
            else:
                text = text +  'Dead' + '\n'
        await ctx.respond(text)
    else:
        await ctx.respond("AMAT")

#Initialize DONE
@bot.command
@lightbulb.command('initialize','give roles to players')
@lightbulb.implements(lightbulb.SlashCommand)
async def init(ctx):
    i = 0
    while i < len(Players['PlayerNumber']):
        ran = random.randint(0,9)
        if(Rolez['Count'][ran]>0):
            print("hi")
            print(Rolez['Count'][ran])
            PlayerState['Role'].append(Rolez['Name'][ran])
            PlayerState['hasGun'].append('No')
            PlayerState['isGuarded'].append(0)
            PlayerState['isHealed'].append(0)
            PlayerState['isHostage'].append(0)
            PlayerState['isShot'].append(0)
            PlayerState['isDead'].append(0)
            PlayerState['detectiveJob'].append(0)
            if(Rolez['Name'][ran]=="MafiaSimple" or Rolez['Name'][ran]=="Nato" or Rolez['Name'][ran]=="GroganGir"):
                PlayerState['detectiveRole'].append(1)
            else:
                PlayerState['detectiveRole'].append(0)
            Players['PlayerState'].update(PlayerState)
            GameState['Players'].update(Players)
            print(PlayerState)
            print(Players)
            print(GameState)
            Rolez['Count'][ran] = Rolez['Count'][ran] - 1
            i = i + 1
    i = 0
    while i < len(Players['PlayerNumber']):
        print(i)
        print(Players['PlayerUserID'][i])
        print(PlayerState['Role'][i])
        await bot.cache.get_user(Players['PlayerUserID'][i]).send(PlayerState['Role'][i])
        i = i + 1

#roles state DONE
@bot.command
@lightbulb.command('rolestate','which roles are in the game?')  
@lightbulb.implements(lightbulb.SlashCommand)
async def rs(ctx):
    text = ""
    for i in range(10):
        print(RolezBa['Count'][i])
        if RolezBa['Count'][i]>0:
            text = text + str(RolezBa['Count'][i]) + ' ' + str(RolezBa['Name'][i]) + '\n'
    text = text + "are in the game"
    await ctx.respond(text)
    

#is_night DONE
@bot.command
@lightbulb.command('night','night has began')
@lightbulb.implements(lightbulb.SlashCommand)
async def isnight(ctx):
    global is_night
    is_night = 1
    await ctx.respond("The night is coming!")
    for i in range(len(Players['PlayerNumber'])):
        PlayerState['hasGun'][i] = 'No'
        PlayerState['detectiveJob'][i] = 0
        PlayerState['isGuarded'][i] = 0
        PlayerState['isHostage'][i] = 0
        PlayerState['isHealed'][i] = 0

    Players['PlayerState'].update(PlayerState)
    GameState['Players'].update(Players)
    mylist.clear()
    j = 0

# firstnight DONE
@bot.command
@lightbulb.command('firstnight','tell mafia their alliances')
@lightbulb.implements(lightbulb.SlashCommand)
async def fn(ctx):
    mafias = []
    for i in range(len(Players['PlayerNumber'])):
        if (PlayerState['detectiveRole'][i]==1 or PlayerState['Role'][i]=="GodFather"):
            mafias.append(i)
    text = ""
    for i in range(len(mafias)):
        text = text + str(PlayerState['Role'][mafias[i]]) + " : " + str(Players['PlayerName'][mafias[i]]) + '\n'
    for i in range(len(mafias)):
        await bot.cache.get_user(int(Players['PlayerUserID'][mafias[i]])).send(text)

#kill DONE
@bot.command
@lightbulb.option('gunkill','if no one is dead enter 0',type=int)
@lightbulb.option('execution','execution kill',type=int)
@lightbulb.command('kill','Days kill')
@lightbulb.implements(lightbulb.SlashCommand)
async def kill(ctx):
    gk = ctx.options.gunkill
    ex = ctx.options.execution
    if(gk>0):
        if (PlayerState['isDead'][gk-1]==0):
            text = ""
            text = 'Okay.' + '\n' + 'RIP ' + str(Players['PlayerName'][gk-1])
            await ctx.respond(text)
            PlayerState['isDead'][gk-1]=1
            Players['PlayerState'].update(PlayerState)
            GameState['Players'].update(Players)
        else :
            await ctx.respond("The player is already dead OSKOL!")
    if(ex>0):
        
        if (PlayerState['isDead'][ex-1]==0):
            text = ""
            text = 'Okay.' + '\n' + 'RIP ' + str(Players['PlayerName'][ex-1])
            await ctx.respond(text)
            PlayerState['isDead'][ex-1]=1
            Players['PlayerState'].update(PlayerState)
            GameState['Players'].update(Players)
        else:
            await ctx.respond("The player is already dead OSKOL!")
    print(PlayerState)

#revive DONE
@bot.command
@lightbulb.option('number','who you killed wrongly?!',type=int)
@lightbulb.command('revive','you killed someone wrongly because i am a OSKOL')
@lightbulb.implements(lightbulb.SlashCommand)
async def re(ctx):
    if(ctx.options.number > 0 and ctx.options.number <= len(Players['PlayerNumber'])):
        if (PlayerState['isDead'][ctx.options.number-1]==1):
            await ctx.respond("Yes u are OSKOL and sucked and i have to fix it.\nAnyway, done!")
            PlayerState['isDead'][ctx.options.number-1]=0
            Players['PlayerState'].update(PlayerState)
            GameState['Players'].update(Players)
        else:
            await ctx.respond("OSKOL")
    else:
        await ctx.respond("OSKOL")
    print(PlayerState)

#NightActions
@bot.command
@lightbulb.command('day','day is here!')
@lightbulb.implements(lightbulb.SlashCommand)
async def na(ctx):
    for i in range(len(Players['PlayerNumber'])):
        print("whats up?")
        if(PlayerState['Role'][i]=="GroganGir"):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
        if(PlayerState['Role'][i]=="Negahban"  and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
        elif(PlayerState['Role'][i]=="Negahban" and PlayerState['isHostage'][i]==1):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("You are OSKOL emshab")
        if(PlayerState['Role'][i]=="Doctor" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
        elif(PlayerState['Role'][i]=="Doctor" and PlayerState['isHostage'][i]==1):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("You are OSKOL emshab")
        if(PlayerState['Role'][i]=="Karagah" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send(PlayerState['detectiveRole'][j])
        elif(PlayerState['Role'][i]=="Karagah" and PlayerState['isHostage'][i]==1):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("You are OSKOL emshab")
        if(PlayerState['Role'][i]=="GodFather"):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
        if(PlayerState['Role'][i]=="Tofangdar" and (PlayerState['isHostage'][i]==0 or (PlayerState['isGuarded'][i]==1 and PlayerState['isHostage']==1))):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
            if mylist:
                for m in range(len(mylist)):
                    await bot.cache.get_user(Players['PlayerUserID'][mylist[m]]).send("You have gun")
        elif(PlayerState['Role'][i]=="Tofangdar" and PlayerState['isHostage'][i]==1):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("You are OSKOL emshab")
        if(PlayerState['Role'][i]=="Nato"):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("Done")
        if(PlayerState['Role'][i]=="Takavar" and PlayerState['isDead'][i]==1):
            await bot.cache.get_user(Players['PlayerUserID'][i]).send("You have been shot. you can shot someone.")
            print("hi")
    
#who is dead? DONE
@bot.command
@lightbulb.command('dead','who is dead in night?')
@lightbulb.implements(lightbulb.SlashCommand)
async def dead(ctx):
    m = 0
    text = ""
    for i in range(len(Players['PlayerNumber'])):
        if(PlayerState['isDead'][i]==1 and PlayerState['isHealed'][i]==0):
            text = text + 'Player '+ str(Players['PlayerName'][i])+ ' is Dead' + '\n'
            m = 1
    if(m==0):
        text = "no one is dead"

    await ctx.respond(text)
    
    is_night = 0

#mygun DONE
@bot.command
@lightbulb.command('mygun','do i have a gun? which type?')
@lightbulb.implements(lightbulb.SlashCommand)
async def mg(ctx):
    i = Players['PlayerUserID'].index(ctx.author.id)
    await ctx.respond(PlayerState['hasGun'][i])
	
	
#mygun DONE
@bot.command
@lightbulb.command('quote','random shitty quote')
@lightbulb.implements(lightbulb.SlashCommand)
async def mg(ctx):
    q = get_random_quote()
    await ctx.respond(q)

#gamestate DONE
@bot.command
@lightbulb.command('gamestate','how many mafia remains?')
@lightbulb.implements(lightbulb.SlashCommand)
async def gs(ctx):
    shahrvand = 0
    mafia = 0
    alive = 0
    for i in range(len(Players['PlayerNumber'])):
        if PlayerState['isDead'][i]==0:
            alive = alive + 1
            if PlayerState['detectiveRole'][i] == 0 and PlayerState['Role'][i] != "GodFather" :
                shahrvand = shahrvand + 1
            else:
                mafia = mafia + 1
    text = str(alive) + " players are alive.\n" + str(shahrvand) + " white\n" + str(mafia) + " black"
    await ctx.respond(text)

        


bot.run()