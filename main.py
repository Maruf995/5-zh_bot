import discord
from discord.ext import commands
from config import settings
import random
from random import choice
from discord.ext import tasks, commands

bot = commands.Bot(command_prefix=settings['prefix'])


@bot.event
async def on_ready():
    print('Ехало')


idy_spat = ['я спать', 'я пошел спать', 'иду спать', 'хочу спать', 'блин, пора спать', 'пора спать', 'я пошла спать',
            'я ложусь спать', 'мне рано вставать, я спать', 'надо спать идти', 'пойду спать', 'уже спать надо',
            'я хочу спать']
spat_spisok = ['Спокойно Ночи😴', 'До Завтра👋', 'Сладких Снов💤', 'Доброй Ночи!', 'Спи Спокойно🙏', 'Приятных Снов🙌']


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    msg = message.content.lower()

    if msg in idy_spat:
        await message.channel.send(f"{choice(spat_spisok)}")


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=100):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    author = ctx.message.author
    await ctx.channel.purge(limit=1)
    await member.kick(reason=reason)
    await ctx.send(f'Админ {author.mention} кикнул юзера {member.mention}')

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    await member.ban(reason=reason)
    await ctx.send(f'Админ {author.mention} забанил юзера {member.mention}')



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


bot.run(settings['token'])
