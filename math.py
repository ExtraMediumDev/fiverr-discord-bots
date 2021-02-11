import sys
import discord
import random
import json
from discord.ext import commands

data = open('low_self_esteem/users.json')
raw = data.read()
users = json.loads(raw)


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$',intents=intents)

seeks = {}
problems = {}
no_delete = []
bot_id = None

#ready message
@bot.event
async def on_ready():
    global bot_id
    bot_id = bot.user.id
    print("Bot is online!")

@bot.event
async def on_member_join(member):
    print(member.name + ' has joined')



def gen_question():
    constants = random.randint(2, 8)
    msg = ''
    answer = 0
    for n in range(constants):
        digits = random.choice([0,1,2,3,4,5,6,7,8,9])
        if digits < 7: new = str(random.randint(0,9))
        else: new = str(random.randint(0,50))
        num = int(new)
        if n == 0: answer = num
        msg = msg + new
        if n > 0:
            if operator == ' - ':
                answer -= num
            if operator == ' + ':
                answer += num
        if n < constants - 1:
            operator = random.choice([' - ',' + '])
            msg = msg + operator

    return msg, answer
            

#when a reaction is added to a message
@bot.event
async def on_raw_reaction_add(payload):
    global bot_id
    channel = bot.get_channel(payload.channel_id)
    seek = await channel.fetch_message(payload.message_id)
    if payload.message_id in seeks and not payload.user_id == seeks[payload.message_id] and not payload.user_id == bot_id:
        await seek.delete()
        del seeks[payload.message_id]
        a,b = gen_question()
        msg = await channel.send('`'+a+'`')
        problems[msg.id] = b
        no_delete.append(msg.id)
    elif seek.author.id == bot_id and not payload.message_id in no_delete:
        await seek.delete()

#when a message is sent, runs the code below
@bot.event
async def on_message(message):
    raw = message.content
    content = raw[1:]
    if '$' in raw:
        if raw[0] == '$':
            if content == "problem":
                embed=discord.Embed(title="NEW PROBLEM", description="Waiting for at least one more person to react...\n\n**remember to type your answer with the prefix \'$\'*", color=0x00ff00)
                msg = await message.channel.send(embed=embed)
                await msg.add_reaction('👍')
                seeks[msg.id] = message.author.id
                no_delete.append(msg.id)
                await message.delete()
            elif content == 'rankings':
                ranked = sorted(users,key=users.get, reverse=True)
                i = 0
                leaderboard = '```'
                for rank in ranked:
                    person = await bot.fetch_user(rank)
                    score = users[rank]
                    leaderboard = leaderboard + str(i+1) + ". {}: {}\n".format(person.name,score)
                    i += 1
                    if i == 9:
                        break
                leaderboard = leaderboard + '```'
                await message.channel.send(leaderboard)
            else:
                for key in problems:
                    answer = problems[key]
                    if int(content) == answer:
                        await message.channel.send('Pog! {} has solved a question!'.format(message.author.name))

                        if message.author.id not in users:
                            users[message.author.id] = 1
                        else:
                            a = users[message.author.id]
                            users[message.author.id] = a + 1

                        print(users)

                        file_write = open('low_self_esteem/users.json','w')
                        write = json.dumps(sorted(users,key=users.get))
                        file_write.write(write)
                        file_write.close()

                        old_problem = await message.channel.fetch_message(key)
                        await old_problem.delete()
                        no_delete.remove(key)
                        del problems[key]
                        await message.delete()
                        break



#runs the bot
bot.run('Nzk5NzEzMTU2ODA0MTE2NTEx.YAHk6g.CYjseoezXMpGy-FkAyBDJ-ZUS8w')
