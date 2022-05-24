import discord
import os
import sys
import asyncio
import time
import json
from discord.utils import get
from config import settings
import random
from random import choice
from discord.ext import tasks, commands

PREFIX = '?'
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
bot.remove_command('help')


# Система предупреждений

@bot.event
async def on_ready():
    print('Ехало')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('?info'))

    if not os.path.exists('users.json'):
        with open('users.json', 'w') as file:
            file.write('{}')
            file.close()

        for guild in bot.guilds:
            for member in guild.members:
                with open('users.json', 'r') as file:
                    data = json.load(file)
                    file.close()
                with open('users.json', 'w') as file:
                    data[str(member.id)] = {
                        "WARNS": 0,
                        "CAPS": 0
                    }
                    json.dump(data, file, indent=4)
                    file.close()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    WARN = BADWORDS + LINKS
    msg = message.content.lower()
    if msg in idy_spat:
        await message.channel.send(f"{choice(spat_spisok)}")
    if msg in knigi:
        await message.channel.send('Напиши команду: ?book')

    for i in range(0, len(WARN)):
        if WARN[i] in message.content.lower():
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()

            with open('users.json', 'w') as file:
                data[str(message.author.id)]['WARNS'] += 1
                json.dump(data, file, indent=4)
                file.close()

                emb = discord.Embed(
                    title='Нарушение',
                    description=f"*Ранее, у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1} нарушение, после 7 он будет забанен!*",
                    timestamp=message.created_at
                )

            emb.add_field(name='Канал:', value=message.channel.mention, inline=True)
            emb.add_field(name='Нарушитель:', value=message.author.mention, inline=True)
            emb.add_field(name=' Тип нарушения:', value='Ругательство/ссылки', inline=True)

            await get(message.guild.text_channels, id=977977348169297923).send(embed=emb)

    if message.content.isupper():
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()
        with open('users.json', 'w') as file:
            data[str(message.author.id)]["CAPS"] += 1
            json.dump(data, file, indent=4)

        if data[str(message.author.id)]["CAPS"] >= 3:
            await message.delete()
            with open('users.json', 'w') as file:
                data[str(message.author.id)]["CAPS"] >= 0
                data[str(message.author.id)]["WARNS"] >= 1

                json.dump(data, file, indent=4)
                file.close()

            emb = discord.Embed(
                title='Нарушение',
                description=f"*Ранее, у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1} нарушение, после 7 он будет забанен!*",
                timestamp=message.created_at
            )

            emb.add_field(name='Канал:', value=message.channel.mention, inline=True)
            emb.add_field(name='Нарушитель:', value=message.author.mention, inline=True)
            emb.add_field(name=' Тип нарушения:', value='КАПС', inline=True)

            await get(message.guild.text_channels, id=977977348169297923).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason='Вы привысили допустимое кол-во нарушений!')


#######################################################################################################################################################

# Все Списки

idy_spat = ['я спать', 'я пошел спать', 'иду спать', 'хочу спать', 'блин, пора спать', 'пора спать', 'я пошла спать',
            'я ложусь спать', 'мне рано вставать, я спать', 'надо спать идти', 'пойду спать', 'уже спать надо',
            'я хочу спать', 'я иду спать', 'мне рано вставать я спать']

knigi = ['скинь книгу']

spat_spisok = ['Спокойно Ночи😴', 'До Завтра👋', 'Сладких Снов💤', 'Доброй Ночи!', 'Спи Спокойно🙏', 'Приятных Снов🙌']

BADWORDS = ['блять', 'сука', 'далбаящер', 'конченный ', 'пидараз', 'еблан', 'даун', 'анус', 'анал', 'хуесос', 'пиздеж',
            'нахуй', 'хуйло', 'пизданах''похуй', ]

LINKS = ['https', 'http', '://', '.com', '.ru', '.net', '.org', '.shop']


#####################################################################################################################################


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(977977348169297923)

    role = discord.utils.get(member.guild.roles, id=978540076755722270)

    await member.add_roles(role)
    await channel.send(embed=discord.Embed(description=f'Пользователь ``{member.name}``, пришел к нам',
                                           color=0x0c0c0))

    # Clear, Kick, Ban, Mute, Warn, Unwarn, Clear_wans


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(colour=discord.Color.red())
    author = ctx.message.author
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Кик', value='Админ кикнул юзера : {}'.format(member.mention))

    await ctx.send(embed=emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(colour=discord.Color.red())
    await ctx.channel.purge(limit=1)
    author = ctx.message.author

    await member.ban(reason=reason)

    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Бан', value='Админ забанил юзера : {}'.format(member.mention))

    await ctx.send(embed=emb)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='Мут')
    await member.add_roles(mute_role)
    await ctx.send(f'У {member.mention}, Ограничение чата, за нарушение прав беседы!')


@bot.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, reason: str):
    if reason.lower() == "badwords" or reason.lower() == "links":
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json', 'w') as file:
            data[str(member.id)]['WARNS'] += 1
            json.dump(data, file, indent=4)
            file.close()

            emb = discord.Embed(
                title='Нарушение',
                description=f"*Ранее, у нарушителя было уже {data[str(member.id)]['WARNS'] - 1} нарушение, после 7 он будет забанен!*",
                timestamp=ctx.message.created_at
            )

        emb.add_field(name='Канал:', value='Не определён', inline=True)
        emb.add_field(name='Нарушитель:', value='Не определён', inline=True)
        emb.add_field(name=' Тип нарушения:', value='Ругательство/ссылки', inline=True)

        await get(ctx.guild.text_channels, id=977977348169297923).send(embed=emb)

        if data[str(member.id)]['WARNS'] >= 7:
            await member.ban(reason='Вы привысили допустимое кол-во нарушений!')

        await ctx.message.reply(embed=discord.Embed(
            title='Успешно',
            description='*Предупреждение выдано!*',
            timestamp=ctx.message.created_at
        ))

    elif reason.lower() == "caps":
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()

        with open('users.json', 'w') as file:
            data[str(member.id)]["CAPS"] >= 0
            data[str(member.id)]["WARNS"] >= 1

            json.dump(data, file, indent=4)
            file.close()

        emb = discord.Embed(
            title='Нарушение',
            description=f"*Ранее, у нарушителя было уже {data[str(member.id)]['WARNS'] - 1} нарушение, после 7 он будет забанен!*",
            timestamp=ctx.message.created_at
        )

        emb.add_field(name='Канал:', value='Не определён', inline=True)
        emb.add_field(name='Нарушитель:', value='Не определён', inline=True)
        emb.add_field(name=' Тип нарушения:', value='КАПС', inline=True)

        await get(ctx.guild.text_channels, id=977977348169297923).send(embed=emb)

        if data[str(member.id)]['WARNS'] >= 7:
            await member.ban(reason='Вы привысили допустимое кол-во нарушений!')

        await ctx.message.reply(embed=discord.Embed(
            title='Успешно',
            description='*Предупреждение выдано!*',
            timestamp=ctx.message.created_at
        ))
    else:
        await ctx.message.reply(embed=discord.Embed(
            title="Ошибка",
            description='Не правильная причина! ',
            timestamp=ctx.message.created_at,
        ))


@warn.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*Использование: ?warn (@участник) (Причина)*',
            timestamp=ctx.message.created_at,
        ))
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))


@bot.command()
@commands.has_permissions(administrator=True)
async def unwarn(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] -= 1
        json.dump(data, file, indent=4)

        file.close()


@bot.command()
@commands.has_permissions(administrator=True)
async def clear_warns(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] = 0
        json.dump(data, file, indent=4)

        file.close()


#######################################################################################

# ERROR
@bot.event
async def on_comman_error(ctx, error):
    pass


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обязательно укажите аргумент!')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))


#############################################################################################################

# Команды help, info
@bot.command()
async def info(ctx):  # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Приветствую, {author.mention}!\n'
                   'Я Так Понял Ты Хочешь Узнать Инфу о Нашей Беседе?\n'
                   'Эта беседа была создана для 5-Ж Класса, 12-Гимназии, Города Бишкек\n'
                   'Тут Вы сможете общаться на разные темы\n'
                   'Тут есть отдельный канал, где вы можете друг другу скидывать ДЗ или ГДЗ\n'
                   'Также можете общаться по голосовому аккаунту\n'
                   'Сервер работает 24/7, Можете общаться целый день\n'
                   'Также Бот, который работает без перерыва\n'
                   'Если хотите узнать что делает бот, то напишите команду /help\n')


@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам бота')

    emb.add_field(name='{}info'.format(PREFIX), value='Узнать о Беседе')
    emb.add_field(name='{}clear'.format(PREFIX), value='Очистка Сообщений в чате')
    emb.add_field(name='{}kick'.format(PREFIX), value='Удаление Пользователя с беседы')
    emb.add_field(name='{}ban'.format(PREFIX), value='Выдает Бан')

    await ctx.send(embed=emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def admin(ctx):
    emb = discord.Embed(title='Навигация по командам бота Для Админов')

    emb.add_field(name='{}info'.format(PREFIX), value='Узнать о Беседе')
    emb.add_field(name='{}clear'.format(PREFIX), value='Очистка Сообщений в чате')
    emb.add_field(name='{}kick'.format(PREFIX), value='Удаление Пользователя с беседы')
    emb.add_field(name='{}ban'.format(PREFIX), value='Выдает Бан')

    await ctx.send(embed=emb)


########################################################################################################

bot.run(settings['token'])
