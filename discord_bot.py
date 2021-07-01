import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions
import config
from googleapiclient.discovery import build
import random
import youtube_dl
from music_cog import music_cog

client = commands.Bot(command_prefix = ":")
client.remove_command('help')

api_key = '<YOUR_API_KEY>' #google custom search api key

@client.event
async def on_ready():

    status = discord.Status.dnd
    activity = discord.Game('zxc') #you can just remove that silly joke

    await client.change_presence(status = status, activity = activity)

    print("Bot is online")


client.add_cog(music_cog(client))


@client.event
async def on_command_error(ctx, error):

    if isinstance(error, commands.MissingRequiredArgument):

        await ctx.send(config.err_missing_argument)

    if isinstance(error, commands.CommandNotFound):

        content = ctx.message.content

        await ctx.send(f'`{content}`' + f'{config.err_not_found}')

    if isinstance(error, commands.MissingPermissions):

        await ctx.send(f'{config.err_missing_permissions}' + f'{ctx.command}')

    if isinstance(error, commands.BadArgument):

        await ctx.send(f'{config.err_bad_argument}' + f'`{ctx.command}`')


@client.command(pass_context = True)
async def join(ctx):
    
   if (ctx.author.voice):
        
       channel = ctx.author.voice.channel

       vocie = await channel.connect()
    
   else:
        
       await ctx.send('You are not in voice channel')

@client.command(pass_context = True)
async def leave(ctx):
    
    if (ctx.voice_client):

        voice = ctx.guild.voice_client
        
        await voice.disconnect()

    else:
        
        await ctx.send('I am not in a voice channel')


#@client.command(pass_context = True)
#async def pause(ctx):


#@client.command(pass_context = True)
#async def resume(ctx):


@client.command(aliases = ['r'])
async def roll(ctx, limit : int = 100):

    if (limit > 0):

        rand = random.randint(0, limit)
        await ctx.send(rand)

    else:
        await ctx.send('what are you trying to do? argument value must be larger than 0')


@client.command()
async def coinflip(ctx):
    coin = ['Yes', 'No']
    result = random.choice(coin)
    await ctx.send(result)


@client.command()
async def ping(ctx):

    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(pass_context = True)
async def help(ctx, page : int = 1):

    if (page == 1):

        embed = discord.Embed(
        colour = discord.Colour.red()
    )
        embed.set_author(name = 'Help page 1')
        embed.add_field(name = ':ping', value=f'{config.help_ping}',
        inline = False)
        embed.add_field(name = ':image | :search | :i <query>', value=f'{config.help_search}',
        inline = False)
        embed.add_field(name = ':gif | :g <query>', value=f'{config.help_gif}',
        inline = False)
        embed.add_field(name = ':clear <amount>', value=f'{config.help_clear}',
        inline = False)
        embed.add_field(name = ':help 2', value=f'{config.help_pages}',
        inline = False)
        await ctx.send(embed = embed)

    elif (page == 2):

        embed = discord.Embed(
        colour = discord.Colour.red()
        )
        embed.set_author(name = 'Help page 2')
        embed.add_field(name = ':avatar | :av <user>', value = f'{config.help_avatar}',
        inline = False)
        embed.add_field(name = ':roll | :r <limit>', value = f'{config.help_roll}',
        inline = False)
        embed.add_field(name = ':coinflip', value = f'{config.help_coinflip}')
        await ctx.send(embed = embed)
    
    else:
        
        await ctx.send('there is no more pages yet')


@client.command(aliases = ['av'])
async def avatar(ctx, member : discord.User):

    avatar_url = member.avatar_url_as(static_format = 'png')
    embed = discord.Embed()
    embed.set_author(name = f'{member.display_name}' + "'" + 's' +  ' avatar')
    embed.set_image(url = avatar_url)
#    embed.description = f'download as [PNG] {avatar_url}'
    await ctx.send(embed = embed)


@client.command()
@has_permissions(manage_messages = True)
async def clear(ctx, amount : int):

    await ctx.channel.purge(limit = amount + 1)
    await ctx.send(f'{amount} Messages have been deleted', delete_after = 5)


@client.command()
@has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member, *, reason = None):

    await member.kick(reason = reason)
    await ctx.send(f'{member} has been kicked')


@client.command(aliases=['image', 'search', 'i'])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey = api_key).cse()
    result = resource.list(
        q=f"{search}", cx="2f7a458793894e534", searchType="image"  #cx is your custom search engine public id
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(
        colour = discord.Colour.red()
    )
    embed1.set_image(url = url)
    
    await ctx.send(embed = embed1)


@client.command(aliases=['gif', 'g'])
async def showgif(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey = api_key).cse()
    result = resource.list(
        q=f"{search}", cx="2f7a458793894e534", searchType="image", imgType="animated" #cx is your custom search engine public id
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(
        colour = discord.Colour.red()
    )
    embed1.set_image(url = url)
    
    await ctx.send(embed = embed1)


client.run('<YOUR_BOT_TOKEN>')
