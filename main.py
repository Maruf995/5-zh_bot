import discord
import os
import sys
import asyncio
import time
import json
from discord.utils import get
from config import settings
from list import BADWORDS, idy_spat, knigi, spat_spisok, LINKS, spat_emoje, emoje
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
        await message.channel.send(f"{choice(spat_spisok)} {choice(spat_emoje)}")
    if msg in knigi:
        await message.channel.send('Напиши команду: ?book')
    if message.author == bot.user:
        return
    if message.content.startswith('!'):
        if message.content == '!refresh':
            refresh()
        else:
            response = get_city(message.content)
            await message.channel.send(response)

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

            await get(message.guild.text_channels, id=978151285545111622).send(embed=emb)

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

            await get(message.guild.text_channels, id=978151285545111622).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason='Вы привысили допустимое кол-во нарушений!')


#######################################################################################################################################################


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(978559623055429663)

    role = discord.utils.get(member.guild.roles, id=883259920982605834)

    await member.add_roles(role)
    welcome = ['Добро Пожаловать! \n'
               f'``{member.name}``, Зашел в нашу беседу\n'
               'Чувствуй себя как дома и соблюдай правила!\n'
               'И пропиши команду: ?info',
               'Здравствуй!\n'
               f'``{member.name}``, Теперь ты в нашей беседе\n'
               'Соблюдай правила и не говори ничего лишнего\n'
               f'Не забудь прописать команду: ?info',
               'Добрый День!\n'
               f'``{member.name}``, Теперь ты один из нас\n'
               'Не забывай соблюдать правила, и не матерись!\n'
               'не забудь прописать: ?info']
    await channel.send(embed=discord.Embed(description=f'{choice(welcome)} {choice(emoje)}',
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

        await get(ctx.guild.text_channels, id=978151285545111622).send(embed=emb)

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

        await get(ctx.guild.text_channels, id=978151285545111622).send(embed=emb)

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

# Остальные команды
@bot.command()
async def table(ctx):
    await ctx.send(f'`Расписание Уроков На Завтра`', file=discord.File('media/raspisan.jpeg'))


@bot.command()
async def zvonok(ctx):
    await ctx.send(f'`Расписание Звонков`', file=discord.File('media/zvonkov.jpeg'))


@bot.command()
async def hw(ctx):
    await ctx.send('`Д/З По Всем Урокам`', )

    await ctx.send('                                                                                           \n`'
                   '                                                                                            \n'
                   ' Русский: Ничего                                                                            \n'
                   ' Литература: Ничего                                                                         \n'
                   ' Англисский(С.И): Стр 295 номер 3                                                           \n'
                   ' Англиский(А.А): Учить неправильные глаголы, следующие 20 штук                              \n'
                   ' Человек и Общество: параграф 5 написать потребности людей, таблица.                        \n'
                   ' Естествознание: параграф 31 учить                                                          \n'
                   ' Кыргызский(Ж.К): Учить стих музыка каждый берет себе по куплету. СТР 168-169               \n'
                   ' Кыргызский(С.Т): Учить стих уч энем                                                        \n'
                   ' ИЗО: Альбом, А3, краски                                                                    \n'
                   ' Истроия: Подготовится к зачёту.                                                            \n'
                   ' Адабият: Знать биографию Мукай Элебаева                                                    \n'
                   ' Музыка: Подготовится к тесту                                                               \n'
                   ' Матем:  номер 468, 469. Кадыралиев.                                                        \n'
                   '                                                                                            \n`'
                   )


# Игра города
def parse_city_json(json_file='russia.json'):
    content = {}
    p_obj = None
    try:
        js_obj = open(json_file, "r", encoding="utf-8")
        p_obj = json.load(js_obj)
    except Exception as err:
        print(err)
        return None
    finally:
        js_obj.close()
    return [city['city'].lower() for city in p_obj]


def get_city(city):
    normilize_city = city.strip().lower()[1:]
    if is_correct_city_name(normilize_city):
        if get_city.previous_city != "" and normilize_city[0] != get_city.previous_city[-1]:
            return 'Город должен начинаться на "{0}"!'.format(get_city.previous_city[-1])

        if normilize_city not in cities_already_named:
            cities_already_named.add(normilize_city)
            last_latter_city = normilize_city[-1]
            proposed_names = list(filter(lambda x: x[0] == last_latter_city, cities))
            if proposed_names:
                for city in proposed_names:
                    if city not in cities_already_named:
                        cities_already_named.add(city)
                        get_city.previous_city = city
                        return city.capitalize()
            return 'Я не знаю города на эту букву. Ты выиграл'
        else:
            return 'Город уже был. Повторите попытку'
    else:
        return 'Некорректное название города. Повторите попытку'


get_city.previous_city = ""


def is_correct_city_name(city):
    return city[-1].isalpha() and city[-1] not in ('ь', 'ъ')


def refresh():
    cities = parse_city_json()[:1000]
    cities_already_named = set()


cities = parse_city_json()[:1000]  # города которые знает бот
cities_already_named = set()  # города, которые уже называли


#####################################################################

# Book
@bot.command()
async def book(ctx):
    await ctx.send(f'`Все Учебники, в электроном виде`')
    await ctx.send(file=discord.File('book/chelovekiobchestvo.pdf'))
    await ctx.send(file=discord.File('book/english.pdf'))
    await ctx.send(file=discord.File('book/kirgiz.pdf'))
    await ctx.send(file=discord.File('book/adabiat.pdf'))
    await ctx.send(file=discord.File('book/estestvo.pdf'))
    await ctx.send(file=discord.File('book/litra.pdf'))
    await ctx.send(file=discord.File('book/istoria.pdf'))
    await ctx.send(file=discord.File('book/matem.pdf'))
    await ctx.send(file=discord.File('book/vilenkin.pdf'))


@bot.command()
async def chio(ctx):
    await ctx.send(file=discord.File('book/chelovekiobchestvo.pdf'))


@bot.command()
async def english(ctx):
    await ctx.send(file=discord.File('book/english.pdf'))


@bot.command()
async def kirgiz(ctx):
    await ctx.send(file=discord.File('book/kirgiz.pdf'))


@bot.command()
async def adabiat(ctx):
    await ctx.send(file=discord.File('book/adabiat.pdf'))


@bot.command()
async def estestvo(ctx):
    await ctx.send(file=discord.File('book/estestvo.pdf'))


@bot.command()
async def litra(ctx):
    await ctx.send(file=discord.File('book/litra.pdf'))


@bot.command()
async def istoria(ctx):
    await ctx.send(file=discord.File('book/istoria.pdf'))


@bot.command()
async def matem(ctx):
    await ctx.send(file=discord.File('book/matem.pdf'))


@bot.command()
async def vilenkin(ctx):
    await ctx.send(file=discord.File('book/vilenkin.pdf'))


###################################################################


# Команды help, info
@bot.command()
async def info(ctx):  # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.

    await ctx.send(f'Приветствую, {author.mention}!\n'
                   'Я так понял ты хочешь узнать инфу о нашей беседе?\n'
                   'Эта беседа была создана для 5-Ж Класса, 12-Гимназии, Города Бишкек\n'
                   'Тут Вы сможете общаться на разные темы\n'
                   'Тут есть отдельный канал, где вы можете друг другу скидывать ДЗ или ГДЗ\n'
                   'Также можете общаться по голосовому аккаунту\n'
                   'Сервер работает 24/7, Можете общаться целый день\n'
                   'Также Бот, который работает без перерыва\n'
                   'Если хотите узнать что делает бот, то напишите команду ?help\n')


@bot.command(pass_context=True)
async def help(ctx):
    emb = discord.Embed(title='Навигация по командам бота')

    emb.add_field(name='{}info'.format(PREFIX), value='Узнать о Беседе')
    emb.add_field(name='{}book'.format(PREFIX), value='Получить все книги в pdf')
    emb.add_field(name='{}vilenkin'.format(PREFIX), value='Книга Виленкин')
    emb.add_field(name='{}matem'.format(PREFIX), value='Книга Кадыралиева')
    emb.add_field(name='{}adabiat'.format(PREFIX), value='Книга Адабият')
    emb.add_field(name='{}kirgiz'.format(PREFIX), value='Книга Кыргыз Тили')
    emb.add_field(name='{}chio'.format(PREFIX), value='Книга ЧИО')
    emb.add_field(name='{}estestvo'.format(PREFIX), value='Книга Естествознание')
    emb.add_field(name='{}istoria'.format(PREFIX), value='Книга История')
    emb.add_field(name='{}litra'.format(PREFIX), value='Книга Литература')
    emb.add_field(name='{}english'.format(PREFIX), value='Книга Англисский Язык')
    emb.add_field(name='{}hw'.format(PREFIX), value='Домашние Задание по всем урокам')
    emb.add_field(name='{}zvonok'.format(PREFIX), value='Расписание Звонков')
    emb.add_field(name='{}table'.format(PREFIX), value='Расписание Уроков')
    emb.add_field(name='!Название города'.format(PREFIX), value='Игра Города (Играть только в "игровой-чат")')

    await ctx.send(embed=emb)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def admin(ctx):
    emb = discord.Embed(title='Навигация по командам бота Для Админов')

    emb.add_field(name='{}info'.format(PREFIX), value='Узнать о Беседе')
    emb.add_field(name='{}clear'.format(PREFIX), value='Очистка Сообщений в чате')
    emb.add_field(name='{}kick'.format(PREFIX), value='Удаление Пользователя с беседы')
    emb.add_field(name='{}ban'.format(PREFIX), value='Выдает Бан')
    emb.add_field(name='{}mute'.format(PREFIX), value='Выдает Мут')
    emb.add_field(name='{}warn'.format(PREFIX), value='Выдает Предупреждение')
    emb.add_field(name='{}unwarn'.format(PREFIX), value='Убрать 1 Предупреждение')
    emb.add_field(name='{}clear_warns'.format(PREFIX), value='Убрать Все Предупреждение')
    emb.add_field(name='{}book'.format(PREFIX), value='Получить все книги в pdf')
    emb.add_field(name='{}vilenkin'.format(PREFIX), value='Книга Виленкин')
    emb.add_field(name='{}matem'.format(PREFIX), value='Книга Кадыралиева')
    emb.add_field(name='{}adabiat'.format(PREFIX), value='Книга Адабият')
    emb.add_field(name='{}kirgiz'.format(PREFIX), value='Книга Кыргыз Тили')
    emb.add_field(name='{}chio'.format(PREFIX), value='Книга ЧИО')
    emb.add_field(name='{}estestvo'.format(PREFIX), value='Книга Естествознание')
    emb.add_field(name='{}istoria'.format(PREFIX), value='Книга История')
    emb.add_field(name='{}litra'.format(PREFIX), value='Книга Литература')
    emb.add_field(name='{}english'.format(PREFIX), value='Книга Англисский Язык')
    emb.add_field(name='{}hw'.format(PREFIX), value='Домашние Задание по всем урокам')
    emb.add_field(name='{}zvonok'.format(PREFIX), value='Расписание Звонков')
    emb.add_field(name='{}table'.format(PREFIX), value='Расписание Уроков')
    emb.add_field(name='!Название города'.format(PREFIX), value='Игра Города (Играть только в "игровой-чат")')

    await ctx.send(embed=emb)


########################################################################################################

# ERROR


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

@admin.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))

@clear_warns.error
async def clear_warns_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description='*У вас недостаточно прав!*',
            timestamp=ctx.message.created_at,
        ))

#############################################################################################################

bot.run(settings['token'])
