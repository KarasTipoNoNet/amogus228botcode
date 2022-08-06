# coding=utf-8
import discord
from discord.ext import commands
import time
import datetime
import random
import asyncio
from discord.utils import get
import os
import requests
import io
import sqlite3
import json
import aiohttp
import smtplib as root
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#import alive




intents = discord.Intents.default()
intents.members = True

bot_token = open('token.txt', 'r').readline()
prefix = '!'

database = sqlite3.connect('amogus228db.db')
cursor = database.cursor()




client = commands.Bot(command_prefix = prefix, intents = intents)
client.remove_command('help')

@client.event
async def on_ready():
	print('conneted!\n')

	# channel = await client.fetch_channel(959111892364820500)

	# time = datetime.datetime.now()

	# embed = discord.Embed(title = 'Бот запущен!', description = 'Вы можете использовать бота!', color = 0x00ff00)
	# embed.set_footer(text = f'Запустился: {time}')	

	# await channel.send(embed=embed)

	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
			name TEXT,
			id INT,
			cash BIGINT,
			rep INT,
			lvl INT,
			server_id INT,
			warns INT,
			exp INT,
			level INT,
			vipstatus INT,
			safecode INT,
			safe INT
		)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS shop(
			role_id INT,
			id INT,
			cost BIGINT
		)""")

	cursor.execute("""CREATE TABLE IF NOT EXISTS snusoed(
			role_id INT,
			id INT,
			cost BIGINT
		)""") # Буржуй: Снюсоед

	cursor.execute("""CREATE TABLE IF NOT EXISTS fermer(
		role_id INT,
		id INT,
		cost BIGINT
	)""") # Буржуй: Фермер

	cursor.execute("""CREATE TABLE IF NOT EXISTS pekar(
		role_id INT,
		id INT,
		cost BIGINT
	)""") # Буржуй: Пекарь

	cursor.execute("""CREATE TABLE IF NOT EXISTS shahter(
		role_id INT,
		id INT,
		cost BIGINT
	)""") # Буржуй: Шахтёр


	cursor.execute("""CREATE TABLE IF NOT EXISTS nsfw(
		url TEXT,
		serverid BIGINT,
		id INTEGER PRIMARY KEY AUTOINCREMENT
		)""")





	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, {guild.id}, 0, 0, 1, 0, 0, 0)")
			else:
				pass
	database.commit()

	await client.change_presence(status = discord.Status.idle, activity = discord.Game(name = 'loading...'))
	await asyncio.sleep(1)
	while True:
		await client.change_presence(status = discord.Status.online, activity = discord.Game(name = 'Бот создан для сервера "Море с рыбами | Карарасёнок =)"'))
		await asyncio.sleep(7)
		await client.change_presence(status = discord.Status.online, activity = discord.Game(name = f'{prefix}help - для списка команд'))
		await asyncio.sleep(7)
		await client.change_presence(status = discord.Status.online, activity = discord.Game(name = f'{prefix}changelog - для списка изменений'))
		await asyncio.sleep(7)




		





@client.command()
@commands.has_permissions(manage_messages = True)
async def echo(ctx, *, message = 'None'):
	if message == 'None':
		await ctx.send('Вы не указали что отправить!')

		print('''ОШИБКА:
Команда: echo
ошибка: Не указано что отправить!
''')
	else:
		author_name = ctx.message.author

		await ctx.channel.purge(limit = 1)
		await ctx.send(f'{message}')

		print(f'{author_name} отправил сообщение от имени бота! \nТекст {message}\n')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, clear = 0):
	if clear == 0:
		await ctx.send('Укажите сколько надо очистить!')
		print('''ОШИБКА:
Команда: clear
ошибка: Не указано сколько нужно очистить
''')
	else:
		author_name = ctx.message.author

		await ctx.channel.purge(limit = 1 + clear)
		await ctx.send(f'Очищено {clear} сообщений!')



		print(f'Модератор {author_name} сделал очистку! \nКол-во сообщений: {clear}\n')



@client.command()
async def verify(ctx, code = 'None'):
	verify_role = discord.utils.get(ctx.message.guild.roles, name='Рыбка')
	author_id = ctx.message.author.id
	author_name = ctx.message.author

	if code == 'None':
		await ctx.message.delete()
		message = await ctx.send(f'<@{author_id}> я отправил тебе в личку код для верификации!')
		await ctx.author.send('Код для верификации: **amogusbesus228**. ||Команда с кодом: !verify amogusbesus228||')
		await asyncio.sleep(10)
		await message.delete()
	elif code == 'amogusbesus228':
		await ctx.message.delete()
		await ctx.message.author.add_roles(verify_role)
		message = await ctx.send(f'<@{author_id}> вы успешно верефицировались!')
		await asyncio.sleep(10)
		await message.delete()

		if cursor.execute(f"SELECT id FROM users WHERE id = {ctx.author.id}").fetchone() is None:
			cursor.execute(f"INSERT INTO users VALUES ('{ctx.author}', {ctx.author.id}, 0, 0, 0, 0, {ctx.author.guild.id}, 0)")
			database.commit()
		else:
			pass
	else:
		await ctx.message.delete()
		message = await ctx.send(f'<@{author_id}> вы ввели неправельный код!')
		await asyncio.sleep(10)
		await message.delete()

	print(f'{author_name} успешно верефицировался!\n')


@client.command()
async def suggest(ctx, *, suggest = 'None'):
	author_id = ctx.message.author.id
	author_name = ctx.message.author

	if suggest == 'None':
		await ctx.send(f'<@{author_id}> вы забыли написать что вы хотите предложить!')
		print('''ОШИБКА:
Команда: suggest
ошибка: Не указана идея
''')
	else:
		suggests_channel = await client.fetch_channel(954642706007728149)

		embed=discord.Embed(title=f"{author_name} отправил идею!", description=f"Идея: {suggest}", color=0x00ff00)
		suggest_send = await suggests_channel.send(embed=embed)
		await ctx.send('ваша идея отправлена в <#954642706007728149>!')

		print(f'{author_name} отправил идею!\nТекст идеи: {suggest}\n')


@client.command()
async def sos(ctx, member = 'None', *, reason = 'None'):
	author_name = ctx.message.author
	author_id = ctx.message.author.id

	if member == 'None':
		await ctx.send(f'<@{author_id}> вы забыли указать нарушителя!')
		print('''ОШИБКА:
Команда: sos
ошибка: Не указан нарушитель
''')
	else:
		embed=discord.Embed(title="Вызов модерации!", description=f"{author_name} заметил что {member} нарушает правила! Причина вызова модерации: {reason}", color=0x0000ff)
		await ctx.send('<@&954649913063510026>')
		await ctx.send(embed=embed)

		print(f'{author_name} вызвал модерацию!\n')






@client.command()
async def help(ctx, *, cotegory = 'None'):
	if cotegory == 'None':
		embed=discord.Embed(title="Выберите котегорию:", description="!help mod\n!help fun\n!help other\n!help info\n!help economy\n!help buyer\n!help crafting\n!help safes\n!help rank\n!help vip\n!help support\n!help nsfw", color=0x0000ff)
	elif cotegory == 'mod':
		embed=discord.Embed(title="Команды бота - Модерация", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name="!clear [кол-во сообщений для уборки]", value="Очистить сообщения", inline=True)
		embed.add_field(name="!mute [участник] [время] {причина}", value="выдать мут", inline=True)
		embed.add_field(name="!unmute [участник]", value="Размутить участника", inline=True)
		embed.add_field(name="!kick [участник] {причина}", value="кикнуть участника", inline=True)
		embed.add_field(name="!ban [участник] {причина}", value="забанить участника", inline=True)
		embed.add_field(name="!addrole [роль] [участник]", value="выдать роль участнику", inline=True)
		embed.add_field(name="!remrole", value="убрать роль у участника", inline=True)
		embed.add_field(name="!create_channel [voice / text] [название]", value="создать голосовой / текстовый канал", inline=True)
		embed.add_field(name="!create_role [permissions integer] {название}", value="Создать роль | Название по умолчанию: No name", inline=True)
		embed.add_field(name="!delete_role [роль]", value="удалить роль", inline=True)
		embed.add_field(name="!survey [тема опроса] {вариант 1} {эмодзи для варианта 1} {вариант 2} {эмодзи для варианта 2}", value="Создать опрос (вариант 1 по умолчанию: Да | эмодзи для варианта 1 по умолчанию: ✅ | вариант 2 по умолчанию: Нет | эмодзи для варианта 2 по умолчанию: ❌)", inline=True)
		embed.add_field(name='!close', value='закрывает канал (уберает право отправлять сообщения)', inline=True)
		embed.add_field(name='!open', value='открыть канал', inline=True)
		embed.add_field(name='!setup', value='установить стандартные права на канал', inline=True)
		embed.add_field(name='!setupnosend', value='установить стандартные права на канал без возможности отправлять сообщения', inline=True)
		embed.add_field(name='!echo_embed {название эмбеда} {описание}', value='Отправить эмбед от имени бота')
		embed.add_field(name='!echo {сообщение}', value='Отправить сообщение от имени бота')
		embed.add_field(name='!warn [@участник] {причина}', value='Выдать предупреждение участнику')
		embed.add_field(name='!remwarn [@участник]', value='Удалить пред у участника')
		embed.add_field(name='!mute_setup', value = 'Настроить сервер под мут роль')
	elif cotegory == 'fun':
		embed=discord.Embed(title="Команды бота - Весёлое / рп", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент", color=0x0000ff)
		embed.add_field(name="!8ball [вопрос]", value="МэДжИк ШаРиК", inline=True)
		embed.add_field(name='!rpbuy "[придмет]" {кол-во}', value='Купить что то (пример: !buy "хлеб" 2)', inline=True)
		embed.add_field(name='!calc [пример]', value='калькулятор (пример команды: !calc 2+2)', inline=True)
		embed.add_field(name='!strcount {что нужно найти в сообщении} {сообщение}', value='Поиск слова/буквы/слога в сообщении')
		embed.add_field(name='!coin <Орёл | Решка>', value = 'Орёл или Решка')
		embed.add_field(name='!rps <Камень | Ножницы | Бумага>', value = 'Камень, Ножницы, Бумага')
		embed.add_field(name='!randnum {минимум} {максимум}', value = 'Выбросить Рандомное число')
		embed.add_field(name='!mine', value = 'Пойти в шахту')
		embed.add_field(name='!hunt', value = 'Пойти на охоту')
		embed.add_field(name='!case', value = 'Открыть кейс')
		embed.add_field(name='!box', value = 'Открыть ящик')
	elif cotegory == 'other':
		embed=discord.Embed(title="Команды бота - Прочее", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name="!suggest [идея]", value="отправить идею", inline=True)
		embed.add_field(name="!sos [нарушитель] {причина}", value="Оповестить модерацию о нарушителе", inline=True)
		embed.add_field(name='!send_email [e-mail получателя] [сообщение]', value = 'Отправить писмо на почту')
		embed.add_field(name='!gd_lvl_req [ID] {видео на YouTube}', value = 'Просто отправить уровень на оценку (Geometry Dash)')
	elif cotegory == 'info':
		embed=discord.Embed(title="Команды бота - Информация", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!changelog', value='Список Изменений бота', inline=True)
		embed.add_field(name='!about', value='мини информация о боте', inline=True)
		embed.add_field(name='!server', value='Показывает информацию о сервере', inline=True)
		embed.add_field(name='!ping', value='Узнать пинг бота', inline=True)
	elif cotegory == 'economy':
		embed=discord.Embed(title="Команды бота - Экономика", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!balance {юзер}', value = 'Посмотреть баланс пользователя')
		embed.add_field(name='!addmoney [юзер] [сколько передать]', value = 'Добавить печеньки к пользователю')
		embed.add_field(name='!remmoney [юзер] [сколько отнять]', value = 'Отнимает печеньки у пользователя')
		embed.add_field(name='!resetmoney {юзер}', value = 'Сбросить печеньки')
		embed.add_field(name='!work', value = 'подзароботать печенек')
		embed.add_field(name='!givemoney [юзер] [сколько передать]', value = 'Передать печеньки пользователю')
		embed.add_field(name='!rate [юзер] [сколько звёзд]', value = 'Поставить оценку (репутацию) юзеру')
		embed.add_field(name='!lb', value = 'Лидерборд по печенькам')
		embed.add_field(name='!promo {промокод}', value = 'Активировать промокод или узнать о них')
		embed.add_field(name='!duo {ставка}', value = 'Типо казино')
		embed.add_field(name='!shop', value = 'Магазин')
		embed.add_field(name='!buy [роль]', value = 'Купить предмет из магазина')
		embed.add_field(name='!add_item [роль] [стоимость]', value = 'Добавить роль в магазин')
		embed.add_field(name='!delete_item [роль]', value = 'Удалить роль из магазина')
		embed.add_field(name='!daily', value = 'Ежедневный бонус')
		embed.add_field(name='!crime', value = 'Подзароботать печенек')
		embed.add_field(name='!rob [участник] {код от сейфа}', value = 'Украсть пиченьки участника')
	elif cotegory == 'buyer':
		embed=discord.Embed(title="Команды бота - Буржуи", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!buyer [Буржуй]', value = 'Буржуи')
		embed.add_field(name='!add_item_to_buyer [буржуй] [роль] [цена]', value = 'Добавить продоваймый предмет к буржую')
		embed.add_field(name='!delete_item_from_buyer [буржуй] [роль]', value = 'Удалить продоваймый предмет у буржуя')
		embed.add_field(name='!sell [буржуй] [роль]', value = 'Продать предмет буржую')
	elif cotegory == 'crafting':
		embed=discord.Embed(title="Команды бота - Крафты", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!craft [предмет 1] [предмет 2]', value = 'Скрафтить что то, все крафты можно получить командой !case')
		embed.add_field(name='!open_craft', value='Открыть все доступные крафты')
	elif cotegory == 'vip':
		embed=discord.Embed(title="Команды бота - Випка", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!vip <info|add|delete>', value = 'Випка =3')
	elif cotegory == 'rank':
		embed=discord.Embed(title="Команды бота - Ранк", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!rank {участник}', value = 'Узнать какой у тебя уровень и опыт')
		embed.add_field(name='!setexp [участник] [опыт]', value = 'Устанавливает опыт у участника 👑')
	elif cotegory == 'support':
		embed=discord.Embed(title="Команды бота - Поддержка", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name = '!support [вопрос]', value = 'Создать тикет')
		embed.add_field(name = '!close_ticket [роль для тикета]', value = 'Закрыть и удалить тикет')
	elif cotegory == 'safes':
		embed=discord.Embed(title="Команды бота - Сейфы", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!safe pass <create|delete> [пароль] [пароль ещё раз (если add)]', value = 'Создать/удалить пароль на сейф')
		embed.add_field(name='!safe <add|take> <пиченьки|all> [пароль]', value = 'Положить/взять пиченьки в сейф')
		embed.add_field(name='!safe_hack [участник]', value = 'Взломать сейф участника')
		embed.add_field(name='!all_codes', value = 'получить все коды от сейфов')
	elif cotegory == 'nsfw':
		embed=discord.Embed(title="Команды бота - NSFW", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент\n \n👑 - вип-команда, доступна админам и тем, кто с випкой", color=0x0000ff)
		embed.add_field(name='!nsfw {id}', value = 'Просто рандомное NSFW видео/гифка/изображение')
		embed.add_field(name='!nsfw_send {url}', value = 'Отправить NSFW видео/гифку/изображение на модерацию')
		embed.add_field(name='!nsfw_add {url}', value = 'Добавить NSFW видео/гифку/изображение в бота')
		embed.add_field(name='!nsfw_delete {id}', value = 'Удалить NSFW видео/гифку/изображение с бота')
	else:
		await ctx.send('Неизвестная котегория!')



	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, mute_time = '0', *, reason = 'None'):
	mute_role = get(ctx.message.guild.roles, name='《😶》Impostor')
	default_role = get(ctx.message.guild.roles, name='《🐟》Рыбка')
	mod = ctx.message.author
	time = datetime.datetime.now()

	

	if mute_time == '0':
    	
		await user.add_roles(mute_role)
		await user.remove_roles(default_role)
		embed=discord.Embed(title = 'Участник получил мут!', description=f"Участник {user} получил мут по причине {reason}", color=0xff0000)
		embed.set_footer(text=f"Выдано: {time}")
		await ctx.send(embed=embed)
		
		

	elif 's' in mute_time:

		embed=discord.Embed(title = 'Ошибка!', description=f"Участник не может быть замьючен меньше чем на 1 минуту!", color=0xff0000)
		await ctx.send(embed=embed)


	elif 'm' in mute_time:

		await user.add_roles(mute_role)
		await user.remove_roles(default_role)
		embed=discord.Embed(title = 'Участник получил мут!', description=f"Участник {user} получил мут на {mute_time} по причине {reason}", color=0xff0000)
		embed.set_footer(text=f"Выдано: {time}")
		await ctx.send(embed=embed)
		
		


		mute_time1 = mute_time[:1]

		await asyncio.sleep(int(mute_time1) * 60)

		await user.remove_roles(mute_role)
		await user.add_roles(default_role)

	elif 'h' in mute_time:

		await user.add_roles(mute_role)
		await user.remove_roles(default_role)
		embed=discord.Embed(title = 'Участник получил мут!', description=f"Участник {user} получил мут на {mute_time} по причине {reason}", color=0xff0000)
		embed.set_footer(text=f"Выдано: {time}")
		await ctx.send(embed=embed)
		
		


		mute_time1 = mute_time[:1]

		await asyncio.sleep(int(mute_time1) * 3600)

		await user.remove_roles(mute_role)
		await user.add_roles(default_role)

	elif 'd' in mute_time:

		await user.add_roles(mute_role)
		await user.remove_roles(default_role)
		embed=discord.Embed(title = 'Участник получил мут!', description=f"Участник {user} получил мут на {mute_time} по причине {reason}", color=0xff0000)
		embed.set_footer(text=f"Выдано: {time}")
		await ctx.send(embed=embed)
		
		


		mute_time1 = mute_time[:1]

		await asyncio.sleep(int(mute_time1) * 864000)

		await user.remove_roles(mute_role)
		await user.add_roles(default_role)



	else:

		embed = discord.Embed(title = 'Ошибка!', description = 'Неизвестное единица времени! Доступные еденицы времени:\nm - минута\nh - час\nd - день')
		
		await ctx.send(embed=embed)








	print(f'Модератор {mod} замутил {user} по причине: {reason}\n')


@client.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, user: discord.Member):
	mute_role = discord.utils.get(ctx.message.guild.roles, name='《😶》Impostor')
	mod = ctx.message.author

	await user.remove_roles(mute_role)
	embed=discord.Embed(title="Человек успешно размутен!", description=f"Участник {user} размучен!", color=0x00ff00)
	await ctx.send(embed=embed)
	

	print(f'{mod} размутил {user}\n')


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = 'None'):
	mod = ctx.message.author
	member_id = member.id
	memebir_id = await client.fetch_user(member_id)

	await memebir_id.send(f'Вы были кикнуты с сервера **Море с рыбами | Карарасёнок =)**\nМодератор: {mod}\nПричина: {reason}\nВы всё ещё можете вернуться по этой ссылке: https://discord.gg/K64GdYwBfT')

	await member.kick(reason=reason)

	embed=discord.Embed(title="Участник кикнут!", description=f"Пользователь {member} был кикнут по причине: `{reason}`", color=0x00ff00)
	await ctx.send(embed=embed)
	

	print(f'{mod} кикнул {member} по причине: {reason}\n')




@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = 'None'):
	banntype = ['default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'default', 'rare']
	bantype = random.choice(banntype)
	mod = ctx.message.author
	member_id = member.id
	memebir_id = await client.fetch_user(member_id)

	await memebir_id.send(f'Вы были забанены на сервере **Море с рыбами | Карарасёнок =)**\nМодератор: {mod}\nПричина: {reason}')

	await member.ban(reason=reason)

	if bantype == 'default':

		embed=discord.Embed(title="Участник забанен!", description=f"Пользователь {member} был забанен по причине: {reason}", color=0x00ff00)
		await ctx.send(embed=embed)
	else:
		await ctx.send(f'Вы забанили {member} по причине {reason} и открыли секретное сообщение о бане! https://cdn.discordapp.com/attachments/962373169660973086/993616809628549292/VID_20220704_222629_918.mp4')
	

	print(f'{mod} забанил {member} по причине: {reason}\n')


@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, role: discord.Role, member: discord.Member):
	mod = ctx.message.author

	await member.add_roles(role)

	await ctx.send(f'Выдал роль **{role}** для пользователя **{member}**')

	print(f'{mod} выдал роль {role} для участника {member}\n')


@client.command()
@commands.has_permissions(manage_roles=True)
async def remrole(ctx, role: discord.Role, member: discord.Member):
	mod = ctx.message.author

	await member.remove_roles(role)

	await ctx.send(f'Убрал роль **{role}** у пользователя **{member}**')

	print(f'{mod} убрал роль {role} у участника {member}\n')



@client.command()
@commands.has_permissions(manage_channels = True)
async def create_channel(ctx, type = 'None', *, name = 'None'):
	mod = ctx.message.author

	if type == 'None':
		await ctx.send('Укажите тип канала:\ntext\nvoice')
	else:
		if name == 'None':
			await ctx.send('Вы забыли указать имя канала!')
		else:
			if type == 'voice':
				channel = await ctx.guild.create_voice_channel(name, reason = 'create channel command')
				channel_id = channel.id

				await ctx.send(f'канал <#{channel_id}> создан!')

				print(f'{mod} создал голосовой канал {name}\n')
			elif type == 'text':
				channel = await ctx.guild.create_text_channel(name, reason = 'create channel command')
				channel_id = channel.id

				await ctx.send(f'канал <#{channel_id}> создан!')

				print(f'{mod} создал текстовый канал {name}\n')

			else:
				await ctx.send('Указан неизвесный тип! Типы каналов:\ntext\nvoice')


@client.command()
@commands.has_permissions(manage_roles = True)
async def create_role(ctx, permissionsid = 1071698660929, *, name = 'No Name'):
	mod = ctx.message.author

	if permissionsid == 0:
		await ctx.send('Вы забыли указать ID прав! Подсказка: используйте https://discordapi.com/permissions.html (сайт на англ. языке) или одного из своих ботов на https://discord.com/developers для более быстрого подсчёта id прав (или же permissions integer)')
	else:

		role = await ctx.guild.create_role(name=name, permissions=discord.Permissions(permissions=permissionsid))

		role_id = role.id

		await ctx.send(f'создал роль <@&{role_id}>')

		print(f'{mod} создал роль {role} с правами {permissionsid}\n')


@client.command(aliases = ['del_role', 'delrole', 'deleterole'])
@commands.has_permissions(manage_roles = True)
async def delete_role(ctx, role: discord.Role = 'None'):
	mod = ctx.message.author

	if role == 'None':
		await ctx.send('Не указана роль')
	else:
		await role.delete()
		await ctx.send(f'удалил роль **{role}**')

		print(f'{mod} удалил роль {role}\n')




@client.command(aliases = ['шар', '8ball'])
async def magic_ball(ctx, *, q):
	author = ctx.message.author

	answers = ['да', 'нет', 'маловероятно', '100%', 'возможно', 'не знаю...']
	answer = random.choice(answers)

	embed=discord.Embed(title="Шарик =)", color=0x00ff00)
	embed.add_field(name=f"Вопрос: {q}", value=f"Ответ: ||{answer}||", inline=False)

	await ctx.send(embed=embed)

	print(f'{author} использовал шарик с вопросом {q}. Ему выпало {answer}')


@client.command()
@commands.has_permissions(manage_messages = True)
async def survey(ctx, name = 'None', option1 = 'Да', emoji = '✅', option2 = 'Нет', emoji2 = '❌'):
	author_name = ctx.message.author
	if name == 'None':
		await ctx.send('Вы забыли указать тему опроса! Пример команды: !survey "крутой ли этот сервер?" "Да, крутой!" "✅" "Нет, отстой!" "❌"')
	else:
		embed=discord.Embed(title=f"Опрос по теме {name}", description="Варианты ответа:")
		embed.add_field(name=f"{option1}", value=f"{emoji}", inline=True)
		embed.add_field(name=f"{option2}", value=f"{emoji2}", inline=True)
		await ctx.channel.purge(limit = 1)
		msg = await ctx.send(embed=embed)

		await msg.add_reaction(emoji)
		await msg.add_reaction(emoji2)

		print(f'''{author_name} запустил опрос на тему {name}
Варианты ответа:
{option1}
{option2}
''')


@client.command()
async def rpbuy(ctx, item = 'None', count = 1):
	if item == 'None':
		await ctx.send('Вы забыли сказать что вы хотите купить!')
	else:
		author_id = ctx.message.author.id

		await ctx.send(f'<@{author_id}> купил {item} в количестве {count} штук(-а / -и)!')



@client.command()
async def about(ctx):
	embed=discord.Embed(title="Немного о нас", description="Привет! Это бот Амогус 228! Он создан для сервера Море с рыбами | Карарасёнок =)\nСоздал <@640926869948203030>\n**Соц Сети создателя**\n[YouTube](https://www.youtube.com/channel/UCnPdFplgMbo5pNPoBJf0kIQ)\n[Telegram](https://t.me/prime_eight_team)\n \n[Донаты (DonationAlerts)](https://www.donationalerts.com/r/kararasenok)\n[Донаты + контент которого нет на ютуб канале (Boosty)](https://boosty.to/kararasenochek)", color=0x1100ff)
	await ctx.send(embed=embed)


#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog
#changelog


@client.command(aliases = ['changelog'])
async def change_log(ctx):
	embed=discord.Embed(title="Последние изменения", description="Версия 0.4 (<t:1648155600:D>(<t:1648155600:R>)):\n- Добавлена команда !about и !changelog\n - Бот работает теперь круглосуточно с небольшими перебоями!\n \nВерсия 0.5 (<t:1648155600:D>(<t:1648155600:R>))\n- Добавлен новый текст в Rich Presence\n \nВерсия 0.6 (<t:1648242000:D>(<t:1648242000:R>))\n- Добавлена команда !calc\n \nВерсия 0.7 (<t:1648760400:D>(<t:1648760400:R>))\n- Немного изменена команда !mute\n- Добавлено уведомление на сервере о включении бота\n- Добавлено сообщение если команды нет (к примеру: команды !test2373465736 нет и бот скажет что команда не существует)\n- Немного изменена команда !verify\n \nВерисия 0.8 (<t:1648846800:D>(<t:1648846800:R>))\n- Добавлена команда !server\n- Добавлены команды !close и !open\n- Добавлены команды !setup и !setupnosend\n- Добавлена команда !card\n- Добавлено сообщение если недостаточно прав на выполнение команды\n \nВерсия 0.9 (<t:1648933200:D>(<t:1648933200:R>))\n- Добавлено 2 новых сообщения об ошибке (неизвестная ошибка / пропушен обязательный аргумент)\n- Была изменена команда !mute\n- Добавлена команда !echo_embed\n \nВерсия 1.0 (<t:1649538000:D>(<t:1649538000:R>))\n- Добавлена команда !strcount\n- Была изменена команда !help\n \nВерсия 1.1 CodeName: Global (<t:1649710800:D> - <t:1649797200:D>(<t:1649797200:R>))\n- Добавлена экономика (!help economy)\n- Добавлена команда !profile\n \nВерсия 1.2 (<t:1649883600:D>(<t:1649883600:R>))\n- Добавлена команда !leaderboard\n- Добавлен коулдаун на команду !work\n \nВерсия 1.3 (<t:1650747600:D>(<t:1650747600:R>))\n- Добавлена команда !warn и !remwarn\n- Добавлен пункт 'Предупреждения' в команду !profile\n- Исправлено парочка багов\n \nВерсия 1.4 (<t:1651501776:f>(<t:1651501776:R>))\n- Исправлен баг с кодировкой\n- Добавлена команда !rps и !coin\n- Добавлены промокоды (!promo)\n \nВерсия 1.5 (<t:1651595343:f>(<t:1651595343:R>))\n- Добавлена команда !mute_setup\n- Была изменена команда !mute\n- Исправлены баги\n \nВерсия 1.6 (<t:1651857184:f>(<t:1651857184:R>))\n- Добавлена команда !duo\n \nВерсия 1.7 CodeName: Global (<t:1651940160:f> - <t:1652026659:f>(<t:1652026659:R>))\n- Добавлен магазин\n- Добавлены команды !shop, !add_item, !delete_item, !buy, !daily, !send_email и !crime\n- Была переименована команда !buy на !rpbuy\n \nВерсия 1.8 CodeName: MegaGlobal (<t:1652093854:f> - <t:1652196709:f>(<t:1652196709:R>))\n- Добавлена команда !ping\n- исправлено парочка багов\n- Удалено сообщение о неизвестной ошибке\n- Добавлена команда !randnum\n- Добавлены буржуи (!help buyer)\n- Добавлен крафтинг (!help crafting)\n- Добавлена команда !mine\n \nВерсия 1.9 (<t:1652459227:f>(<t:1652459227:R>))\n-Добавлена команда !hunt\n- Добавлена команда !case\n- Добавлены новые крафты\n- Изменён способ получения крафтов\n- Добавлены новые руды\n \nВерсия 2.0 CodeName: UltraGlobal (<t:1656255600:D> - <t:1656340909:D>(<t:1656340909:R>))\n- Добавлены сейфы (!help safes)\n- Добавлена ранг система (!help rank)\n- Добавлена поддержка (!help support)\n- Добавлена випка (!help vip)\n- Добавлена команда !rob и !all_codes\n \nВерсия 2.1 (<t:1656426420:f>(<t:1656426420:R>))\n- Исправлены некоторые баги\n \nВерсия 2.2 (<t:1656775980:D>(<t:1656775980:R>))\n- Добавлен NSFW (!help nsfw)\n- Исправлено парочка багов\n- Добавлена команда !gd_lvl_req\n \nВерсия 2.3 (<t:1656967500:D>(<t:1656967500:R>))\n- Добавлена команда !box\n- Добавлено секретное сообщение о бане", color = 0x0000ff)
	embed.set_footer(text='Версия бота: 2.3')

	await ctx.send(embed=embed)
	


@client.command(aliases = ['calculator', 'math', 'калькулятор'])
async def calc(ctx, example):
	if '/0' in example:
		await ctx.send('На ноль делить нельзя!')
	else:
		answer = eval(example)
		embed=discord.Embed(title="Калькулятор", description=f"Пример: {example}={answer}", color=0x00ff00)
		await ctx.send(embed=embed)
	# await ctx.send(eval(example))




# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors
# errors



@client.event
async def on_command_error(ctx, error):
	author_id = ctx.message.author.id
	if isinstance(error, commands.CommandNotFound):
		embed=discord.Embed(title="Команды нет!", description=f"<@{author_id}>, такой команды нет! Пропишите !help для списка команд или предложите команду командой !suggest [идея для команды]", color=0xff0000)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingPermissions):
		embed=discord.Embed(title="Недостаточно прав!", description=f"<@{author_id}>, у вас не хватает прав для выполнения команды!", color=0xff0000)
		await ctx.send(embed=embed)
	elif isinstance(error, commands.MissingRequiredArgument):
		embed=discord.Embed(title="Пропуск нужного аргумента!", description=f"<@{author_id}>, вы забыли указать один из аргуметов, который является нужным в команде!", color=0xff0000)
		await ctx.send(embed=embed)
	# elif isinstance(error, commands.CommandOnCooldown):
	# 	embed=discord.Embed(title="Не так быстро!", description=f"<@{ctx.author.id}>, на команду стоит ограничение по времени использования!", color=0xff0000)
	# 	await ctx.send(embed=embed)
	# else:
	# 	embed=discord.Embed(title="Неизвестная ошибка!", description=f"<@{author_id}>, произошла неизвестная ошибка! Пожалуйста, сообщите о ней создателю!", color=0xff0000)
	# 	await ctx.send(embed=embed)





@client.command()
async def server(ctx):
	# await ctx.send('идёт сбор информации... Пожалуйста подождите...')

	server_members = ctx.guild.members

	server_name = ctx.guild.name
	server_owner = ctx.guild.owner

	member_all = 0

	on = 0
	i = 0
	dnd = 0
	of = 0
	
	channel_text = 0
	channel_voice = 0


	for text in ctx.guild.text_channels:
		channel_text += 1

	for voice in ctx.guild.voice_channels:
		channel_voice += 1

	channel_all = channel_voice + channel_text

	for member in server_members:
		member_all += 1

	# for discord.Status.online in server_members:
	# 	o += 1
	# for discord.Status.idle in server_members:
	# 	i += 1
	# for discord.Status.dnd in server_members:
	# 	dnd += 1
	# for discord.Status.offline in server_members:
	# 	of += 1


	embed=discord.Embed(title="Статистика сервера 📊", description=f"**Сервер:**\nНазвание: {server_name}\nСоздатель: {server_owner}\n \n**Участники:**\nВсего: {member_all}\n \n**Каналы:**\nВсего: {channel_all}\nТекстовых: {channel_text}\nГолосовых: {channel_voice}", color=0x0000ff)
	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels = True)
async def close(ctx):

	channel = ctx.message.channel

	await channel.set_permissions(get(ctx.guild.roles, id=954405241430880306), send_messages = False)

	await ctx.send('**Чат закрыт**')

@client.command()
@commands.has_permissions(manage_channels = True)
async def open(ctx):

	channel = ctx.message.channel

	await channel.set_permissions(get(ctx.guild.roles, id=954405241430880306), send_messages = True)

	await ctx.send('**Чат открыт**')

@client.command(aliases = ['setup'])
@commands.has_permissions(administrator = True)
async def setupchannel(ctx):
	channel = ctx.message.channel

	await channel.set_permissions(get(ctx.guild.roles, id=954405241430880306), view_channel = False)
	await channel.set_permissions(get(ctx.guild.roles, id=954406906162724964), view_channel = True)

	await ctx.send('Канал настроен!')


@client.command(aliases = ['setupnosend', 'setup_no_send'])
@commands.has_permissions(administrator = True)
async def setupchannelnosend(ctx):
	channel = ctx.message.channel

	await channel.set_permissions(get(ctx.guild.roles, id=954405241430880306), view_channel = False, send_messages = False)
	await channel.set_permissions(get(ctx.guild.roles, id=954406906162724964), view_channel = True)


	await ctx.send('Канал настроен!')





@client.command()
@commands.has_permissions(manage_messages = True)
async def echo_embed(ctx, title, *, description):
	await ctx.channel.purge(limit = 1)

	

	await ctx.send(embed = discord.Embed(title = title, description = description, colour = 0x00ff00))



@client.command(aliases = ['strcount', 'str', 'count'])
async def str_count(ctx, arg, *, message):
	argsinmessage = message.count(arg)
	await ctx.send(f'в сообщении **{message}**, __**{arg}**__ встречается **{argsinmessage}** раз(-а)')



# Economy commands


@client.command(aliases = ['bal'])
async def balance(ctx, member : discord.Member = None):
	if member is None:
		bal = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		safe_bal = cursor.execute("SELECT safe FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		total = int(bal) + int(safe_bal)
		await ctx.send(embed = discord.Embed(title = f'Баланс пользователя {ctx.author}', description = f'Баланс: {bal} :cookie:\nВ сейфе: {safe_bal} :cookie:\nВсего: {total} :cookie:'))
	else:
		bal = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		safe_bal = cursor.execute("SELECT safe FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		total = int(bal) + int(safe_bal)
		await ctx.send(embed = discord.Embed(title = f'Баланс пользователя {member}', description = f'Баланс: {bal} :cookie:\nВ сейфе: {safe_bal} :cookie:\nВсего: {total} :cookie:'))


@client.command(aliases = ['addmoney'])
@commands.has_permissions(manage_messages = True)
async def add_money(ctx, member : discord.Member = None, amount : int = None):
	if member is None:
		await ctx.send('Вы забыли указать пользователя!')
	else:
		if amount is None:
			await ctx.send('Вы не указали сколько передать!')
		elif amount < 1:
			await ctx.send('Укажите сумму больше 1 печеньки!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(amount, member.id))
			database.commit()

			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили {amount} :cookie: к балансу <@{member.id}>', color = 0x00ff00))


@client.command(aliases = ['removemoney', 'remmoney'])
@commands.has_permissions(manage_messages = True)
async def remove_money(ctx, member : discord.Member = None, amount = None):
	if member is None:
		await ctx.send('Вы забыли указать пользователя!')
	else:
		if amount is None:
			await ctx.send('Вы не указали сколько отнять!')
		elif int(amount) < 1:
			await ctx.send('Укажите сумму больше 1 печеньки!')
		else:
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
			database.commit()

			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно убрали {amount} :cookie: от баланса <@{member.id}>', color = 0x00ff00))


@client.command(aliases = ['resetmoney'])
@commands.has_permissions(manage_messages = True)
async def reset_money(ctx, member : discord.Member = None):
	if member is None:
		cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, ctx.author.id))
		cursor.execute("UPDATE safe SET cash = {} WHERE id = {}".format(0, ctx.author.id))
		database.commit()

		await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно сбросили печеньки!', color = 0x00ff00))

	else:
		cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
		cursor.execute("UPDATE safe SET cash = {} WHERE id = {}".format(0, member.id))
		database.commit()

		await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно сбросили печеньки у <@{member.id}>!', color = 0x00ff00))



@client.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def work(ctx):
	amount = int(random.uniform(1, 100))

	cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), ctx.author.id)).fetchone()
	database.commit()

	replies = [f'Вы поработали на складе и вы получили {amount} :cookie:', f'Вы построили дом и получили {amount} :cookie:', f'Вы взломали пинтагон и вам заплатили {amount} :cookie:']
	reply = random.choice(replies)

	await ctx.send(embed = discord.Embed(title = 'Вы подзаработали печенек!', description = reply))
	database.commit()

@work.error
async def work_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed = discord.Embed(title = 'Не так быстро!', description = 'Ты сможешь использовать команду !work через 5 минут!', color = 0xff0000))





@client.command(aliases = ['pay', 'give', 'givemoney'])
async def give_money(ctx, member : discord.Member = None, amount = None):
	if member is None:
		await ctx.send('Укажите кому передать!')
	else:
		if amount is None:
			await ctx.send('Укажите сколько передать!')
		elif int(amount) < 1:
			await ctx.send('Задайте значение больше 1!')
		elif cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < int(amount):
			await ctx.send('У вас не хватает денег!')
		else:
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), member.id)).fetchone()
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), ctx.author.id)).fetchone()
			database.commit()
			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'Вы успешно передали {amount} пользователю {member}', color = 0x00ff00))


@client.command()
async def rate(ctx, member : discord.Member = None, stars = None, *, comment = 'None'):
	if member is None:
		await ctx.send('Укажите кому поставить оценку!')
	elif ctx.author.id == member.id:
		await ctx.send('Вы не можете поставить оценку себе!')
	else:
		if stars is None:
			await ctx.send('Укажите сколько звёзд (макс. 5)')
		elif int(stars) > 5:
			await ctx.send('Укажите кол-во звёзд меньше 5-ти')
		else:
			cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {}".format(int(stars), member.id))
			database.commit()
			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'Вы поставили оценку {stars} звёзд для пользователя {member} с комантарием {comment}'))



@client.command()
async def profile(ctx, member : discord.Member = None):
	if member is None:
		money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		reputation = cursor.execute("SELECT rep FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		exp = cursor.execute("SELECT exp FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		level = cursor.execute("SELECT level FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		vipp = cursor.execute("SELECT vipstatus FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		vip = int(vipp)
		user_id = ctx.message.author.id
		user_name = ctx.author.name
		user_avatar = ctx.author.avatar_url

		if vip == 0:
			vpstatus = 'У данного пользователя нету випки'
			embed =	discord.Embed(title = f'Статистика пользователя {user_name}', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)
		else:
			vpstatus = 'У данного пользователя есть випка! Преобрести: !vip info'
			embed =	discord.Embed(title = f'Статистика пользователя {user_name} 👑', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)

		

		
		embed.set_footer(text = f'Запросил: {ctx.author.name}', icon_url = user_avatar)
		embed.set_thumbnail(url = user_avatar)
		embed.add_field(name = 'Ник', value = user_name)
		embed.add_field(name = 'АйДи', value = user_id)
		embed.add_field(name = 'Печеньки (деньги)', value = money)
		embed.add_field(name = 'Репутация', value = reputation)
		embed.add_field(name = 'Предупреждения', value = f'{warns}/5')
		embed.add_field(name = 'Опыт', value = f'{exp}')
		embed.add_field(name = 'Уровень', value = level)
		embed.add_field(name = 'Випка', value = vpstatus)


		await ctx.send(embed = embed)
	else:
		money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		reputation = cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		exp = cursor.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		level = cursor.execute("SELECT level FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		vipp = cursor.execute("SELECT vipstatus FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		vip = int(vipp)
		user_id = member.id
		user_name = member.name
		user_avatar = member.avatar_url

		if vip == 0:
			vpstatus = 'У данного пользователя нету випки'
			embed =	discord.Embed(title = f'Статистика пользователя {user_name}', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)
		else:
			vpstatus = 'У данного пользователя есть випка! Преобрести: !vip info'
			embed =	discord.Embed(title = f'Статистика пользователя {user_name} 👑', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)



		
		embed.set_footer(text = f'Запросил: {ctx.author.name}', icon_url = ctx.author.avatar_url)
		embed.set_thumbnail(url = user_avatar)
		embed.add_field(name = 'Ник', value = user_name)
		embed.add_field(name = 'АйДи', value = user_id)
		embed.add_field(name = 'Печеньки (деньги)', value = money)
		embed.add_field(name = 'Репутация', value = reputation)
		embed.add_field(name = 'Предупреждения', value = f'{warns}/5')
		embed.add_field(name = 'Опыт', value = exp)
		embed.add_field(name = 'Уровень', value = level)
		embed.add_field(name = 'Випка', value = vpstatus)

		await ctx.send(embed = embed)


@client.command(aliases = ['lb'])
async def leaderboard(ctx, limit = 10):
	embed = discord.Embed(title = f'Топ {limit} по печенькам')
	counter = 0

	for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {0} ORDER BY cash DESC LIMIT {1}".format(ctx.guild.id, int(limit))):
		if row[1] <= 0:
			pass
		else:
			counter += 1
			embed.add_field(
				name = f'# {counter} | {row[0]}',
				value = f'{row[1]} :cookie:',
				inline = False
			)

	await ctx.send(embed = embed)



@client.command()
@commands.has_permissions(kick_members = True, ban_members = True)
async def warn(ctx, member: discord.Member = None, *, reason = 'None'):
	user = await client.fetch_user(member.id)
	warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]

	if member is None:
		await ctx.send('Укажите пользователя!')
	else:
		if ctx.author.id == member.id:
			await ctx.send('Вы не можете выдать пред себе!')
		else:
			if warns > 3:
				cursor.execute("UPDATE users SET warns = 0 WHERE id = {}".format(member.id))
				database.commit()
				await user.send(f'Вы были кикнуты с сервера **Море с рыбами | Карарасёнок =)**\nПричина: Авто-кик: 5/5 предов\nВы всё ещё можете вернуться по этой ссылке: https://discord.gg/K64GdYwBfT')
				await member.kick(reason = 'Авто-кик: 5/5 предов')
				await ctx.send(embed = discord.Embed(title = 'Участник кикнут!', description = f'<@{member.id}> был кикнут из за многочисленых нарушений правил.'))
			else:
				cursor.execute("UPDATE users SET warns = warns + 1 WHERE id = {}".format(member.id))
				database.commit()
				await user.send(f'Вы получили предупреждение на сервере ** Море с рыбами | Карарасёнок =)**\nМодеротор: <@{ctx.author.id}>\nПричина: {reason}')
				warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]
				await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{member.id}> получил пред!\nПричина: {reason}\nМодератор: <@{ctx.author.id}>\nКол-во предов у <@{member.id}>: {warns}/5'))


@client.command()
async def remwarn(ctx, member: discord.Member = None):
	if member is None:
		await ctx.send('Укажите пользователя!')
	else:
		if ctx.author.id == member.id:
			await ctx.send('Вы не можете убрать пред у себя!')
		else:
			cursor.execute("UPDATE users SET warns = warns - 1 WHERE id = {}".format(member.id))
			database.commit()
			warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]
			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'Модератор <@{ctx.author.id}> убрал 1 пред у <@{member.id}>! Теперь у <@{member.id}> {warns}/5 предов!', color = 0x00ff00))


@client.command()
async def coin(ctx, orel_ili_reshka = None):
	orel_ili_reshka_random = ['Орёл', 'Решка']
	orel_ili_reshka_choice = random.choice(orel_ili_reshka_random)

	if orel_ili_reshka is None:
		await ctx.send('Укажите: **Орёл** или **Решка**?')
	else:
		if orel_ili_reshka == orel_ili_reshka_choice:
			await ctx.send(embed=discord.Embed(title='Орёл или Решка?', description=f'Воу <@{ctx.author.id}> тебе выпал(-а) {orel_ili_reshka_choice} поздравляю ты победил!', color = 0x00ff00))
		else:
			await ctx.send(embed=discord.Embed(title='Орёл или Решка?', description=f'К счастью или к сожелению, у <@{ctx.author.id}> выпал(-а) {orel_ili_reshka_choice}, ты проиграл =(', color = 0xff0000))


@client.command()
@commands.cooldown(1, 1800, commands.BucketType.user)
async def promo(ctx, code = None):
	if code is None:
		await ctx.send(embed=discord.Embed(title = '!promo - Что это?', description = 'Командой !promo можно получить мини бонус в экономике! Все коды можно узнать в [оффициальной группе сервера вк](https://vk.com/seawithfish)'))
	elif code == 'newoffvk':
		await ctx.message.delete()
		cursor.execute(f"UPDATE users SET cash = cash + 100 WHERE id = {ctx.author.id}")
		database.commit()
		ok = await ctx.send(f'<@{ctx.author.id}> вы успешно активировали промокод на сто печенек!')
		await asyncio.sleep(10)
		await ok.delete()
	else:
		await ctx.message.delete()
		ok = await ctx.send(f'<@{ctx.author.id}> такого промокода нет!')
		await asyncio.sleep(10)
		await ok.delete()


@promo.error
async def promo_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed = discord.Embed(title = 'Не так быстро!', description = 'Ты сможешь использовать команду !promo через 30 минут!', color = 0xff0000))





@client.command()
async def rps(ctx, selection = 'Камень'):
	bot_selection = random.choice(['Камень', 'Ножницы', 'Бумага'])

	if selection == 'Камень':
		if bot_selection == 'Камень':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ничья!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Ножницы':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты победил!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Бумага':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты проиграл!')
			await ctx.send(embed=embed)
	elif selection == 'Бумага':
		if bot_selection == 'Камень':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты победил!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Ножницы':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты проиграл!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Бумага':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ничья!')
			await ctx.send(embed=embed)
	elif selection == 'Ножницы':
		if bot_selection == 'Камень':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты проиграл!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Ножницы':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ничья!')
			await ctx.send(embed=embed)
		elif bot_selection == 'Бумага':
			embed = discord.Embed(title='Камень, Ножницы, Бумага', color = 0x0000ff)
			embed.add_field(name='Выбор бота:', value=bot_selection)
			embed.add_field(name='Твой выбор:', value=selection)
			embed.add_field(name='Результат:', value = 'Ты победил!')
			await ctx.send(embed=embed)
	else:
		await ctx.send('Такого предмета нету! Выберите предмет (с учётом регистра):\nКамень\nНожницы\nБумага')






@client.command()
@commands.has_permissions(administrator = True)
async def mute_setup(ctx):
	ignore = [971064016854208552, 954758300262621215]
	await ctx.send('Идёт настройка сервера! Пожалуйста подождите...')
	for channel in ctx.guild.text_channels:
		if channel.id in ignore:
			continue
		else:
			try:
				await channel.set_permissions(get(ctx.guild.roles, id = 954680311315324938), view_channel = False, send_messages = False)
			except:
				continue
	for channel in ctx.guild.voice_channels:
		try:
			await channel.set_permissions(get(ctx.guild.roles, id = 954680311315324938), connect = False)
		except:
			continue

	await ctx.send('Сервер настроен!')



@client.command()
async def duo(ctx, setn = 100):
	luckk = ['y', 'y', 'y', 'y', 'y', 'n', 'n', 'n']

	luck = random.choice(luckk)

	if cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0] < int(setn):
		await ctx.send('У вас не хватает денег!')
	elif setn < 0:
		await ctx.send('Укажите значение больше 0!')
	else:
		if luck == 'y':
			win = setn * 2
			await ctx.send(embed=discord.Embed(title = 'Умножение печенек', description = f'<@{ctx.author.id}>, вы выйграли и ваша ставка удваевается!', color = 0x00ff00))
			cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(win, ctx.author.id))
		else:
			await ctx.send(embed=discord.Embed(title = 'Умножение печенек', description = f'К сожелению <@{ctx.author.id}>, вы проиграли, и вы теряете {setn} :cookie:', color = 0xff0000))
			cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(setn, ctx.author.id))

		database.commit()



@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def crime(ctx):
	amountt = int(random.uniform(1, 1000))

	amount = f'{amountt} :cookie:'

	luckk = ['y', 'y', 'y', 'y', 'n', 'n', 'n', 'n']

	luck = random.choice(luckk)

	well_replies = [f'Вы решили ограбить банк и вас получилось! Вы смогли унести с собой {amount}', f'Вы нашли кошелёк и там было {amount} . Вы логично их забрали =)', f'Вы ограбили соседа на сумму {amount}']
	bad_replies = [f'Вы захотели ограбить соседа, но он позвонил в полицию и вам выписали штраф в размере {amount}', f'Вы нашли кошелёк. Вы логично захотели деньги забрать, но мимо проходил полицейский и он вас оштрафовал на сумму {amount}', f'Вы решили ограбить банк и вас не получилось! Вам пришлось платить штраф {amount}']
	bad_reply = random.choice(bad_replies)
	well_reply = random.choice(well_replies)

	if luck == 'y':
		await ctx.send(embed=discord.Embed(title = 'Воровка', description = well_reply, color = 0x00ff00))
		cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amountt), ctx.author.id))
	else:
		await ctx.send(embed=discord.Embed(title = 'Воровка', description = bad_reply, color = 0xff0000))
		cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amountt), ctx.author.id))

	database.commit()


@crime.error
async def crime_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed = discord.Embed(title = 'Не так быстро!', description = 'Ты сможешь использовать команду !crime через 1 час!', color = 0xff0000))



@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
	await ctx.send(embed=discord.Embed(title = 'Ежедневный бонус!', description = f'<@{ctx.author.id}>, вы забрали 50 :cookie: как бонус! Вызвращайтесь завтра что бы забрать ещё один бонус!', color = 0x00ff00))
	cursor.execute("UPDATE users SET cash = cash + 100 WHERE id = {}".format(ctx.author.id))
	database.commit()

@daily.error
async def daily_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed = discord.Embed(title = 'Не так быстро!', description = 'Ты сможешь использовать команду !daily через 1 день!', color = 0xff0000))



@client.command(aliases = ['sendmail', 'se'])
async def send_email(ctx, to = None, *, message = None):
	if to is None:
		await ctx.send('Укажите кому отправить сообщение!')
	elif to == 'amogus228.bot@mail.ru':
		await ctx.send('Извините, но я не могу отправить сообщение себе!')
	else:
		if message is None:
			await ctx.send('Укажите что отправить!')
		elif message == 'Пасхалка':
			login = 'amogus228.bot@mail.ru'
			password = 'kEdBSH1Z0gpEWZW4YSQW'
			topic = f'Отправлено пользователем {ctx.message.author} | Амогус 228 Дискорд бот'
			url = 'smtp.mail.ru'
			msg = MIMEMultipart()

			msg['Subject'] = topic
			msg['From'] = login

			server = root.SMTP_SSL(url, 465)

			server.login(login, password)
			body = 'Метоксихлордэтиламиномитилбутиламиноакридин'
			msg.attach(MIMEText(body, 'plain'))

			server.sendmail(login, to, msg.as_string())
			await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы нашли пасхалку, она была отправлена на почту, которую указали! Если сообщение нету, проверьте папку спам (это сообщение не является пасхалкой)', color = 0x00ff00))
		else:
			login = 'amogus228.bot@mail.ru'
			password = 'kEdBSH1Z0gpEWZW4YSQW'
			topic = f'Отправлено пользователем {ctx.message.author} | Амогус 228 Дискорд бот'
			url = 'smtp.mail.ru'
			msg = MIMEMultipart()

			msg['Subject'] = topic
			msg['From'] = login

			server = root.SMTP_SSL(url, 465)

			server.login(login, password)
			body = message
			msg.attach(MIMEText(body, 'plain'))

			server.sendmail(login, to, msg.as_string())

			await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно отправили письмо! Если его нету, проверьте папку спам!', color = 0x00ff00))


	

@client.command(aliases = ['additem', 'ai'])
@commands.has_permissions(manage_roles = True)
async def add_item(ctx, role : discord.Role = None, cost : int = None):
	if role is None:
		await ctx.send(f'<@{ctx.author.id}> укажите роль!')
	else:
		if cost is None:
			await ctx.send(f'<@{ctx.author.id}> укажите стоимость!')
		elif cost < 0:
			await ctx.send(f'<@{ctx.author.id}> укажите стоимость больше 0!')
		else:
			cursor.execute("INSERT INTO shop VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
			database.commit()

			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили роль <@&{role.id}> в магазин!', color = 0x00ff00))
			await ctx.send(embed = discord.Embed(title = 'Промотр товара', description = f'Роль: <@&{role.id}>\nЦена: {cost}', color = 0x0000ff))


@client.command()
@commands.has_permissions(manage_roles = True)
async def delete_item(ctx, role : discord.Role = None):
	if role is None:
		await ctx.send(f'<@{ctx.author.id}> укажите роль!')
	else:
		cursor.execute("DELETE FROM shop WHERE role_id = {}".format(role.id))
		database.commit()
		await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно удалили роль <@&{role.id}> из магазина!', color = 0x00ff00))


@client.command()
async def shop(ctx):
	embed = discord.Embed(title = 'Магазин')

	for row in cursor.execute("SELECT role_id, cost FROM shop WHERE id = {}".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			embed.add_field(
					name  = f'Стоимость: {row[1]}',
					value = f'Название: {ctx.guild.get_role(row[0]).mention}'
				)
		else:
			pass

	await ctx.send(embed=embed)


@client.command()
async def buy(ctx, role : discord.Role = None):
	if role is None:
		await ctx.send('Укажите роль которую надо купить!')
	else:
		if role in ctx.author.roles:
			await ctx.send('У вас уже есть эта роль!')
		elif cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0] > cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]:
			await ctx.send('У вас не хватает денег!')
		else:
			await ctx.author.add_roles(role)
			cursor.execute("UPDATE users SET cash = cash - {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shop WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
			database.commit()
			await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно купили предмет!'))




@client.command()
async def ping(ctx):
	calc = client.latency * 1000
	pong = round(calc)
	x = discord.Embed(title='Пинг бота - Слишком высокий!', description=f'{pong} ms', color=0xff0000) # bad
	y = discord.Embed(title='Пинг бота - Нормальный!', description=f'{pong} ms', color=0xffff00) # normal
	z = discord.Embed(title='Пинг бота - Идеальный!', description=f'{pong} ms', color=0x00ff00) # Nice
	if pong > 160:
		msg = await ctx.send(embed=x)
	elif 80 <= pong <= 160:
		msg = await ctx.send(embed=y)
	elif pong < 80:
		msg = await ctx.send(embed=z)




@client.command()
async def randnum(ctx, minimum : int = 0, maximum : int = 100):
	num = int(random.uniform(minimum, maximum))

	await ctx.send(embed=discord.Embed(title = 'Рандомное число', description = f'рандом показал число: {num}', color = 0x0000ff))




@client.command()
async def buyer(ctx, *, burzhuy = None):
	if burzhuy is None:
		await ctx.send('''Выберите Буржуя:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')
	else:

		if burzhuy == 'Снюсоед':


			embed = discord.Embed(title = 'Буржуй: Снюсоед')

			for row in cursor.execute("SELECT role_id, cost FROM snusoed WHERE id = {}".format(ctx.guild.id)):
				if ctx.guild.get_role(row[0]) != None:
					embed.add_field(
							name  = f'Получим: {row[1]}',
							value = f'После продажи: {ctx.guild.get_role(row[0]).mention}'
						)
				else:
					pass

			await ctx.send(embed=embed)

		elif burzhuy == 'Фермер':
			embed = discord.Embed(title = 'Буржуй: Фермер')

			for row in cursor.execute("SELECT role_id, cost FROM fermer WHERE id = {}".format(ctx.guild.id)):
				if ctx.guild.get_role(row[0]) != None:
					embed.add_field(
							name  = f'Получим: {row[1]}',
							value = f'После продажи: {ctx.guild.get_role(row[0]).mention}'
						)
				else:
					pass
			await ctx.send(embed=embed)

		elif burzhuy == 'Пекарь':
			embed = discord.Embed(title = 'Буржуй: Пекарь')

			for row in cursor.execute("SELECT role_id, cost FROM pekar WHERE id = {}".format(ctx.guild.id)):
				if ctx.guild.get_role(row[0]) != None:
					embed.add_field(
							name  = f'Получим: {row[1]}',
							value = f'После продажи: {ctx.guild.get_role(row[0]).mention}'
						)
				else:
					pass
			await ctx.send(embed=embed)

		elif burzhuy == 'Шахтёр':
			embed = discord.Embed(title = 'Буржуй: Шахтёр')

			for row in cursor.execute("SELECT role_id, cost FROM shahter WHERE id = {}".format(ctx.guild.id)):
				if ctx.guild.get_role(row[0]) != None:
					embed.add_field(
							name  = f'Получим: {row[1]}',
							value = f'После продажи: {ctx.guild.get_role(row[0]).mention}'
						)
				else:
					pass
			await ctx.send(embed=embed)

		else:
			await ctx.send('''Такого буржуя нету! Список буржуев:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')



@client.command(aliases = ['additemtoburzhuy'])
@commands.has_permissions(administrator = True)
async def add_item_to_buyer(ctx, burzhuy = None, role : discord.Role = None, cost : int = None):
	if burzhuy is None:
		await ctx.send('''Выберите Буржуя:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')
	else:
		if burzhuy == 'Снюсоед':

			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				if cost is None:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость!')
				elif cost < 0:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость больше 0!')
				else:
					cursor.execute("INSERT INTO snusoed VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
					database.commit()

					await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили роль <@&{role.id}> в список покупаемых предметов у буржуя Снюсоед!', color = 0x00ff00))
					await ctx.send(embed = discord.Embed(title = 'Промотр товара', description = f'Роль: <@&{role.id}>\nЦена: {cost}', color = 0x0000ff))
		elif burzhuy == 'Фермер':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				if cost is None:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость!')
				elif cost < 0:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость больше 0!')
				else:
					cursor.execute("INSERT INTO fermer VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
					database.commit()

					await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили роль <@&{role.id}> в список покупаемых предметов у буржуя Фермер!', color = 0x00ff00))
					await ctx.send(embed = discord.Embed(title = 'Промотр товара', description = f'Роль: <@&{role.id}>\nЦена: {cost}', color = 0x0000ff))
		elif burzhuy == 'Пекарь':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				if cost is None:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость!')
				elif cost < 0:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость больше 0!')
				else:
					cursor.execute("INSERT INTO pekar VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
					database.commit()

					await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили роль <@&{role.id}> в список покупаемых предметов у буржуя Пекарь!', color = 0x00ff00))
					await ctx.send(embed = discord.Embed(title = 'Промотр товара', description = f'Роль: <@&{role.id}>\nЦена: {cost}', color = 0x0000ff))
		elif burzhuy == 'Шахтёр':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				if cost is None:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость!')
				elif cost < 0:
					await ctx.send(f'<@{ctx.author.id}> укажите стоимость больше 0!')
				else:
					cursor.execute("INSERT INTO shahter VALUES ({}, {}, {})".format(role.id, ctx.guild.id, cost))
					database.commit()

					await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно добавили роль <@&{role.id}> в список покупаемых предметов у буржуя Шахтёр!', color = 0x00ff00))
					await ctx.send(embed = discord.Embed(title = 'Промотр товара', description = f'Роль: <@&{role.id}>\nЦена: {cost}', color = 0x0000ff))
		

		else:
			await ctx.send('''Такого буржуя нету! Список буржуев:
1. Снюсоед
2. Фермер
3. Пекарь
4. Буржуй''')



@client.command()
@commands.has_permissions(administrator = True)
async def delete_item_from_buyer(ctx, burzhuy = None, role : discord.Role = None):
	if burzhuy is None:
		await ctx.send('''Выберите Буржуя:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')
	else:	
		if burzhuy == 'Снюсоед':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				cursor.execute("DELETE FROM snusoed WHERE role_id = {}".format(role.id))
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно удалили роль <@&{role.id}> из списка покупаемых предметов у буржуя Снюсоед!', color = 0x00ff00))

		elif burzhuy == 'Фермер':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				cursor.execute("DELETE FROM fermer WHERE role_id = {}".format(role.id))
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно удалили роль <@&{role.id}> из списка покупаемых предметов у буржуя Фермер!', color = 0x00ff00))

		elif burzhuy == 'Пекарь':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				cursor.execute("DELETE FROM pekar WHERE role_id = {}".format(role.id))
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно удалили роль <@&{role.id}> из списка покупаемых предметов у буржуя Пекарь!', color = 0x00ff00))

		elif burzhuy == 'Шахтёр':
			if role is None:
				await ctx.send(f'<@{ctx.author.id}> укажите роль!')
			else:
				cursor.execute("DELETE FROM shahter WHERE role_id = {}".format(role.id))
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно удалили роль <@&{role.id}> из списка покупаемых предметов у буржуя Шахтёр!', color = 0x00ff00))

			
		else:
			await ctx.send('''Такого буржуя нету! Список буржуев:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')


@client.command()
async def sell(ctx, burzhuy = None, role : discord.Role = None):
	if burzhuy is None:
		await ctx.send('''Выберите Буржуя:
1. Снюсоед
2. Фермер
3. Пекарь
4. Шахтёр''')
	elif burzhuy == 'Снюсоед':
		if role is None:
			await ctx.send('Укажите предмет которых хотите продать!')
		else:
			if role not in ctx.author.roles:
				await ctx.send('У вас нету этого предмета!')
			else:
				await ctx.author.remove_roles(role)
				cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM snusoed WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				database.commit()
				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно продали предмет снюсоеду!'))
	elif burzhuy == 'Фермер':
		if role is None:
			await ctx.send('Укажите предмет которых хотите продать!')
		else:
			if role not in ctx.author.roles:
				await ctx.send('У вас нету этого предмета!')
			else:
				await ctx.author.remove_roles(role)
				cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM fermer WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				database.commit()
				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно продали предмет Фермеру!'))
	elif burzhuy == 'Пекарь':
		if role is None:
			await ctx.send('Укажите предмет которых хотите продать!')
		else:
			if role not in ctx.author.roles:
				await ctx.send('У вас нету этого предмета!')
			else:
				await ctx.author.remove_roles(role)
				cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM pekar WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				database.commit()
				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно продали предмет Пекарю!'))
	elif burzhuy == 'Шахтёр':
		if role is None:
			await ctx.send('Укажите предмет которых хотите продать!')
		else:
			if role not in ctx.author.roles:
				await ctx.send('У вас нету этого предмета!')
			else:
				await ctx.author.remove_roles(role)
				cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(cursor.execute("SELECT cost FROM shahter WHERE role_id = {}".format(role.id)).fetchone()[0], ctx.author.id))
				database.commit()
				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно продали предмет Шахтёру!'))




@client.command()
async def craft(ctx, item1 = 'None', item2 = 'None'):
	await ctx.message.delete()

	if item1 == 'Пшеница':
		if item2 == 'Молот':
			role1 = get(ctx.guild.roles, name = 'Молот')
			role2 = get(ctx.guild.roles, name = 'Пшеница')
			role3 = get(ctx.guild.roles, name = 'Мука')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Муку**!'))
				else:
					await ctx.send('У вас нехватает предмета: Пшиница')
			else:
				await ctx.send('У вас не хватает предмета: Молот')

	elif item1 == 'Железная руда':
		if item2 == 'Печь':
			role1 = get(ctx.guild.roles, name = 'Железная руда')
			role2 = get(ctx.guild.roles, name = 'Железо')

			if role1 in ctx.author.roles:
				await ctx.author.remove_roles(role1)
				await ctx.author.add_roles(role2)

				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Железо**!'))
			else:
				await ctx.send('У вас нехватает предмета: Железная руда')

	elif item1 == 'Железо':
		if item2 == 'Палка':
			role1 = get(ctx.guild.roles, name = 'Железо')
			role2 = get(ctx.guild.roles, name = 'Палка')
			role3 = get(ctx.guild.roles, name = 'Молот')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Молот**!'))
				else:
					await ctx.send('У вас нехватает предмета: Палка')
			else:
				await ctx.send('У вас нехватает предмета: Железо')
	elif item1 == 'Электролит':
		if item2 == 'Угольный стержень':
			role1 = get(ctx.guild.roles, name = 'Электролит')
			role2 = get(ctx.guild.roles, name = 'Угольный Стержень')
			role3 = get(ctx.guild.roles, name = 'Часть от батарейки')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Часть от батарейки**!'))
				else:
					await ctx.send('Не хватает предмета: Угольный Стержень')
			else:
				await ctx.send('Не хватает предмета: Электролит')

	elif item1 == 'Уголь':
		if item2 == 'Камень':
			role1 = get(ctx.guild.roles, name = 'Уголь')
			role2 = get(ctx.guild.roles, name = 'Камень')
			role3 = get(ctx.guild.roles, name = 'Угольный Стержень')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Угольный Стержень**!'))
				else:
					await ctx.send('Не хватает предмета: Камень')
			else:
				await ctx.send('Не хватает предмета: Уголь')

	elif item1 == 'Часть от батарейки':
		if item2 == 'Железо':
			role1 = get(ctx.guild.roles, name = 'Часть от батарейки')
			role2 = get(ctx.guild.roles, name = 'Железо')
			role3 = get(ctx.guild.roles, name = 'Батарейка')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Батарейку**!'))
				else:
					await ctx.send('Не хватает предмета: Железо')
			else:
				await ctx.send('Не хватает предмета: Часть от батарейки')

	elif item1 == 'Железо':
		if item2 == 'Точило':
			role1 = get(ctx.guild.roles, name = 'Железо')
			# role2 = get(ctx.guild.roles, name = '')
			role3 = get(ctx.guild.roles, name = 'Проволка')

			if role1 in ctx.author.roles:
				# if role2 in ctx.author.roles:
				await ctx.author.remove_roles(role1)
				# await ctx.author.remove_roles(role2)
				await ctx.author.add_roles(role3)

				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Проволку**!'))
			else:
				await ctx.send('Не хватает предмета: Железо')

	elif item1 == 'Медь':
		if item2 == 'Проволка':
			role1 = get(ctx.guild.roles, name = 'Медь')
			role2 = get(ctx.guild.roles, name = 'Проволка')
			role3 = get(ctx.guild.roles, name = 'Провода')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Провода**!'))
				else:
					await ctx.send('Не хватает предмета: Проволка')
			else:
				await ctx.send('Не хватает предмета: Медь')

	elif item1 == 'Порох':
		if item2 == 'Провода':
			role1 = get(ctx.guild.roles, name = 'Порох')
			role2 = get(ctx.guild.roles, name = 'Провода')
			role3 = get(ctx.guild.roles, name = 'Динамит')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Динамит**!'))
				else:
					await ctx.send('Не хватает предмета: Провода')
			else:
				await ctx.send('Не хватает предмета: Порох')

	elif item1 == 'Динамит':
		if item2 == 'Уран':
			role1 = get(ctx.guild.roles, name = 'Динамит')
			role2 = get(ctx.guild.roles, name = 'Уран')
			role3 = get(ctx.guild.roles, name = 'Ядерная Бомба')

			if role1 in ctx.author.roles:
				if role2 in ctx.author.roles:
					await ctx.author.remove_roles(role1)
					await ctx.author.remove_roles(role2)
					await ctx.author.add_roles(role3)

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = 'Вы успешно скрафтили **Ядерную Бомбу**!'))
				else:
					await ctx.send('Не хватает предмета: Динамит')
			else:
				await ctx.send('Не хватает предмета: Уран')







@client.command()
async def mine(ctx, *, booster = None):
	items = ['Палка', 'Железо', 'Дерево', 'Золото', 'Камень', 'Бедрок', 'Медь', 'Уран', 'Камень', 'Камень', 'Камень', 'Камень', 'Золото', 'Золото', 'Золото', 'Дерево', 'Дерево', 'Дерево', 'Дерево', 'Дерево', 'Дерево', 'Дерево', 'Дерево', 'Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка','Палка', 'Железо', 'Железо', 'Железо', 'Железо', 'Железо', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Медь', 'Уголь', 'Уголь', 'Уголь', 'Уголь', 'Уголь', 'Уголь', 'Уголь', 'Уголь']

	item1 = random.choice(items)
	item2 = random.choice(items)
	item3 = random.choice(items)

	stick = get(ctx.guild.roles, name = 'Палка')
	iron = get(ctx.guild.roles, name = 'Железная руда')
	wood = get(ctx.guild.roles, name = 'Дерево')
	gold = get(ctx.guild.roles, name = 'Золото')
	stone = get(ctx.guild.roles, name = 'Камень')
	Bedrock = get(ctx.guild.roles, name = 'Бедрок')
	copper = get(ctx.guild.roles, name = 'Медь')
	Uran = get(ctx.guild.roles, name = 'Уран')
	coal = get(ctx.guild.roles, name = 'Уголь')

	embed = discord.Embed(title = 'Вы сходили в шахту!', description = 'Вот что вы добыли:')

	if item1 == 'Палка':
		embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
		if stick not in ctx.author.roles:
			await ctx.author.add_roles(stick)
		else:
			pass
	elif item1 == 'Железо':
		embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
		if iron not in ctx.author.roles:
			await ctx.author.add_roles(iron)
		else:
			pass
	elif item1 == 'Дерево':
		embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
		if wood not in ctx.author.roles:
			await ctx.author.add_roles(wood)
		else:
			pass
	elif item1 == 'Золото':
		embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
		if gold not in ctx.author.roles:
			await ctx.author.add_roles(gold)
		else:
			pass
	elif item1 == 'Камень':
		embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
		if stone not in ctx.author.roles:
			await ctx.author.add_roles(stone)
		else:
			pass
	elif item1 == 'Бедрок':
		embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Bedrock)
		else:
			pass
	elif item1 == 'Медь':
		embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(copper)
		else:
			pass
	elif item1 == 'Уран':
		embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Uran)
		else:
			pass
	elif item1 == 'Уголь':
		embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(coal)
		else:
			pass


	if item2 == 'Палка':
		embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
		if stick not in ctx.author.roles:
			await ctx.author.add_roles(stick)
		else:
			pass
	elif item2 == 'Железо':
		embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
		if iron not in ctx.author.roles:
			await ctx.author.add_roles(iron)
		else:
			pass
	elif item2 == 'Дерево':
		embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
		if wood not in ctx.author.roles:
			await ctx.author.add_roles(wood)
		else:
			pass
	elif item2 == 'Золото':
		embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
		if gold not in ctx.author.roles:
			await ctx.author.add_roles(gold)
		else:
			pass
	elif item2 == 'Камень':
		embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
		if stone not in ctx.author.roles:
			await ctx.author.add_roles(stone)
		else:
			pass
	elif item2 == 'Бедрок':
		embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Bedrock)
		else:
			pass
	elif item2 == 'Медь':
		embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(copper)
		else:
			pass
	elif item2 == 'Уран':
		embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Uran)
		else:
			pass
	elif item2 == 'Уголь':
		embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(coal)
		else:
			pass

	if item3 == 'Палка':
		embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
		if stick not in ctx.author.roles:
			await ctx.author.add_roles(stick)
		else:
			pass
	elif item3 == 'Железо':
		embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
		if iron not in ctx.author.roles:
			await ctx.author.add_roles(iron)
		else:
			pass
	elif item3 == 'Дерево':
		embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
		if wood not in ctx.author.roles:
			await ctx.author.add_roles(wood)
		else:
			pass
	elif item3 == 'Золото':
		embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
		if gold not in ctx.author.roles:
			await ctx.author.add_roles(gold)
		else:
			pass
	elif item3 == 'Камень':
		embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
		if stone not in ctx.author.roles:
			await ctx.author.add_roles(stone)
		else:
			pass
	elif item3 == 'Бедрок':
		embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Bedrock)
		else:
			pass
	elif item3 == 'Медь':
		embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(copper)
		else:
			pass
	elif item3 == 'Уран':
		embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(Uran)
		else:
			pass
	elif item3 == 'Уголь':
		embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
		if Bedrock not in ctx.author.roles:
			await ctx.author.add_roles(coal)
		else:
			pass


	if booster == 'Ядерная Бомба':
		role = get(ctx.guild.roles, name = 'Ядерная Бомба')

		if role in ctx.author.roles:
			item4 = random.choice(items)
			item5 = random.choice(items)
			item6 = random.choice(items)

			await ctx.author.remove_roles(role)

			if item4 == 'Палка':
				embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
				if stick not in ctx.author.roles:
					await ctx.author.add_roles(stick)
				else:
					pass
			elif item4 == 'Железо':
				embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
				if iron not in ctx.author.roles:
					await ctx.author.add_roles(iron)
				else:
					pass
			elif item4 == 'Дерево':
				embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
				if wood not in ctx.author.roles:
					await ctx.author.add_roles(wood)
				else:
					pass
			elif item4 == 'Золото':
				embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
				if gold not in ctx.author.roles:
					await ctx.author.add_roles(gold)
				else:
					pass
			elif item4 == 'Камень':
				embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
				if stone not in ctx.author.roles:
					await ctx.author.add_roles(stone)
				else:
					pass
			elif item4 == 'Бедрок':
				embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
				if Bedrock not in ctx.author.roles:
					await ctx.author.add_roles(Bedrock)
				else:
					pass
			elif item4 == 'Медь':
				embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
				if copper not in ctx.author.roles:
					await ctx.author.add_roles(copper)
				else:
					pass
			elif item4 == 'Уран':
				embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
				if Uran not in ctx.author.roles:
					await ctx.author.add_roles(Uran)
				else:
					pass
			elif item4 == 'Уголь':
				embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
				if coal not in ctx.author.roles:
					await ctx.author.add_roles(coal)
				else:
					pass


			if item5 == 'Палка':
				embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
				if stick not in ctx.author.roles:
					await ctx.author.add_roles(stick)
				else:
					pass
			elif item5 == 'Железо':
				embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
				if iron not in ctx.author.roles:
					await ctx.author.add_roles(iron)
				else:
					pass
			elif item5 == 'Дерево':
				embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
				if wood not in ctx.author.roles:
					await ctx.author.add_roles(wood)
				else:
					pass
			elif item5 == 'Золото':
				embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
				if gold not in ctx.author.roles:
					await ctx.author.add_roles(gold)
				else:
					pass
			elif item5 == 'Камень':
				embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
				if stone not in ctx.author.roles:
					await ctx.author.add_roles(stone)
				else:
					pass
			elif item5 == 'Бедрок':
				embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
				if Bedrock not in ctx.author.roles:
					await ctx.author.add_roles(Bedrock)
				else:
					pass
			elif item5 == 'Медь':
				embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
				if copper not in ctx.author.roles:
					await ctx.author.add_roles(copper)
				else:
					pass
			elif item5 == 'Уран':
				embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
				if Uran not in ctx.author.roles:
					await ctx.author.add_roles(Uran)
				else:
					pass
			elif item5 == 'Уголь':
				embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
				if coal not in ctx.author.roles:
					await ctx.author.add_roles(coal)
				else:
					pass

			if item6 == 'Палка':
				embed.add_field(name = 'Палка', value = 'Шанс выпадения: 98%')
				if stick not in ctx.author.roles:
					await ctx.author.add_roles(stick)
				else:
					pass
			elif item6 == 'Железо':
				embed.add_field(name = 'Железо', value = 'Шанс выпадения: 87%')
				if iron not in ctx.author.roles:
					await ctx.author.add_roles(iron)
				else:
					pass
			elif item6 == 'Дерево':
				embed.add_field(name = 'Дерево', value = 'Шанс выпадения: 93%')
				if wood not in ctx.author.roles:
					await ctx.author.add_roles(wood)
				else:
					pass
			elif item6 == 'Золото':
				embed.add_field(name = 'Золото', value = 'Шанс выпадения: 57%')
				if gold not in ctx.author.roles:
					await ctx.author.add_roles(gold)
				else:
					pass
			elif item6 == 'Камень':
				embed.add_field(name = 'Камень', value = 'Шанс выпадения: 96%')
				if stone not in ctx.author.roles:
					await ctx.author.add_roles(stone)
				else:
					pass
			elif item6 == 'Бедрок':
				embed.add_field(name = 'Бедрок', value = 'Шанс выпадения: 8%')
				if Bedrock not in ctx.author.roles:
					await ctx.author.add_roles(Bedrock)
				else:
					pass
			elif item6 == 'Медь':
				embed.add_field(name = 'Медь', value = 'Шанс выпадения: 74%')
				if copper not in ctx.author.roles:
					await ctx.author.add_roles(copper)
				else:
					pass
			elif item6 == 'Уран':
				embed.add_field(name = 'Уран', value = 'Шанс выпадения: 13%')
				if Uran not in ctx.author.roles:
					await ctx.author.add_roles(Uran)
				else:
					pass
			elif item6 == 'Уголь':
				embed.add_field(name = 'Уголь', value = 'Шанс выпадения: 89%')
				if coal not in ctx.author.roles:
					await ctx.author.add_roles(coal)
				else:
					pass




	await ctx.send(embed=embed)




@client.command()
async def hunt(ctx):
	items = ['Кожа', 'Говядина', 'Свинина', 'Порох', 'Баранина', 'Кожа', 'Кожа', 'Кожа', 'Кожа', 'Кожа', 'Кожа', 'Говядина', 'Говядина', 'Говядина', 'Говядина', 'Говядина', 'Свинина', 'Свинина', 'Свинина', 'Свинина', 'Свинина', 'Свинина', 'Порох', 'Порох', 'Порох', 'Порох', 'Порох', 'Порох', 'Порох', 'Порох', 'Баранина', 'Баранина', 'Баранина', 'Баранина', 'Баранина', 'Баранина']

	kozha = get(ctx.guild.roles, name = 'Кожа')
	govyzdina = get(ctx.guild.roles, name = 'Говядина')
	svinina = get(ctx.guild.roles, name = 'Свинина')
	poroh = get(ctx.guild.roles, name = 'Порох')
	baranina = get(ctx.guild.roles, name = 'Баранина')

	item1 = random.choice(items)
	item2 = random.choice(items)
	item3 = random.choice(items)

	embed = discord.Embed(title = 'Вы сходили а охоту!', description = 'Вот что вы добыли:')


	if item1 == 'Кожа':
		embed.add_field(name = 'Кожа', value = 'Шанс выпадения: 96%')
		if kozha not in ctx.author.roles:
			await ctx.author.add_roles(kozha)
		else:
			pass
	elif item1 == 'Говядина':
		embed.add_field(name = 'Говядина', value = 'Шанс выпадения: 87%')
		if govyzdina not in ctx.author.roles:
			await ctx.author.add_roles(govyzdina)
		else:
			pass

	elif item1 == 'Свинина':
		embed.add_field(name = 'Свинина', value = 'Шанс выпадения: 78%')
		if svinina not in ctx.author.roles:
			await ctx.author.add_roles(svinina)
		else:
			pass

	elif item1 == 'Порох':
		embed.add_field(name = 'Порох', value = 'Шанс выпадения: 89%')
		if poroh not in ctx.author.roles:
			await ctx.author.add_roles(poroh)
		else:
			pass

	elif item1 == 'Баранина':
		embed.add_field(name = 'Баранина', value = 'Шанс выпадения: 93%')
		if baranina not in ctx.author.roles:
			await ctx.author.add_roles(baranina)
		else:
			pass


	if item2 == 'Кожа':
		embed.add_field(name = 'Кожа', value = 'Шанс выпадения: 96%')
		if kozha not in ctx.author.roles:
			await ctx.author.add_roles(kozha)
		else:
			pass
	elif item2 == 'Говядина':
		embed.add_field(name = 'Говядина', value = 'Шанс выпадения: 87%')
		if govyzdina not in ctx.author.roles:
			await ctx.author.add_roles(govyzdina)
		else:
			pass

	elif item2 == 'Свинина':
		embed.add_field(name = 'Свинина', value = 'Шанс выпадения: 78%')
		if svinina not in ctx.author.roles:
			await ctx.author.add_roles(svinina)
		else:
			pass

	elif item2 == 'Порох':
		embed.add_field(name = 'Порох', value = 'Шанс выпадения: 89%')
		if poroh not in ctx.author.roles:
			await ctx.author.add_roles(poroh)
		else:
			pass

	elif item2 == 'Баранина':
		embed.add_field(name = 'Баранина', value = 'Шанс выпадения: 93%')
		if baranina not in ctx.author.roles:
			await ctx.author.add_roles(baranina)
		else:
			pass


	if item3 == 'Кожа':
		embed.add_field(name = 'Кожа', value = 'Шанс выпадения: 96%')
		if kozha not in ctx.author.roles:
			await ctx.author.add_roles(kozha)
		else:
			pass
	elif item3 == 'Говядина':
		embed.add_field(name = 'Говядина', value = 'Шанс выпадения: 87%')
		if govyzdina not in ctx.author.roles:
			await ctx.author.add_roles(govyzdina)
		else:
			pass

	elif item3 == 'Свинина':
		embed.add_field(name = 'Свинина', value = 'Шанс выпадения: 78%')
		if svinina not in ctx.author.roles:
			await ctx.author.add_roles(svinina)
		else:
			pass

	elif item3 == 'Порох':
		embed.add_field(name = 'Порох', value = 'Шанс выпадения: 89%')
		if poroh not in ctx.author.roles:
			await ctx.author.add_roles(poroh)
		else:
			pass

	elif item3 == 'Баранина':
		embed.add_field(name = 'Баранина', value = 'Шанс выпадения: 93%')
		if baranina not in ctx.author.roles:
			await ctx.author.add_roles(baranina)
		else:
			pass


	await ctx.send(embed=embed)



@client.command()
async def open_craft(ctx):
	craft1 = get(ctx.guild.roles, name = 'Крафт 1')
	craft2 = get(ctx.guild.roles, name = 'Крафт 2')
	craft3 = get(ctx.guild.roles, name = 'Крафт 3')
	craft4 = get(ctx.guild.roles, name = 'Крафт 4')
	craft5 = get(ctx.guild.roles, name = 'Крафт 5')
	craft6 = get(ctx.guild.roles, name = 'Крафт 6')
	craft7 = get(ctx.guild.roles, name = 'Крафт 7')
	craft8 = get(ctx.guild.roles, name = 'Крафт 8')
	craft9 = get(ctx.guild.roles, name = 'Крафт 9')
	craft10 = get(ctx.guild.roles, name = 'Крафт 10')

	crafts_opened = 0


	if craft1 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_batareyka_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft1)
	if craft2 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_chast_ot_batareyki_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft2)
	if craft3 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_dinamit_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft3)
	if craft4 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_iron_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft4)
	if craft5 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_molot_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft5)
	if craft6 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_muka_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft6)
	if craft7 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_provoda_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft7)
	if craft8 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_provolka_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft8)
	if craft9 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_ugolniy_sterzhen_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft9)
	if craft10 in ctx.author.roles:
		await ctx.author.send(file = discord.File(fp = 'crafts/craft_yadernaya_bomba_amogus228.png'))
		crafts_opened += 1
		await ctx.author.remove_roles(craft10)


	if crafts_opened >= 1:
		await ctx.send(f'<@{ctx.author.id}> вы открыли {crafts_opened} крафт(-а, -оф)! Все они были отправлены в лс!')
	else:
		await ctx.send(f'<@{ctx.author.id}> у вас нет открытых крафтов!')



@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def case(ctx):
	craft1 = get(ctx.guild.roles, name = 'Крафт 1')
	craft2 = get(ctx.guild.roles, name = 'Крафт 2')
	craft3 = get(ctx.guild.roles, name = 'Крафт 3')
	craft4 = get(ctx.guild.roles, name = 'Крафт 4')
	craft5 = get(ctx.guild.roles, name = 'Крафт 5')
	craft6 = get(ctx.guild.roles, name = 'Крафт 6')
	craft7 = get(ctx.guild.roles, name = 'Крафт 7')
	craft8 = get(ctx.guild.roles, name = 'Крафт 8')
	craft9 = get(ctx.guild.roles, name = 'Крафт 9')
	craft10 = get(ctx.guild.roles, name = 'Крафт 10')

	items = ['печеньки', 'Крафт 1', 'Крафт 2', 'Крафт 3', 'Крафт 4', 'Крафт 5', 'Крафт 6', 'Крафт 7', 'Крафт 8', 'Крафт 9', 'Крафт 10', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки', 'печеньки']

	cookie_count1 = int(random.uniform(1, 500))
	cookie_count2 = int(random.uniform(1, 500))


	item1 = random.choice(items)
	item2 = random.choice(items)

	embed = discord.Embed(title = 'Кейс', description = 'Вы открыли кейс и вам выпало...')

	if item1 == 'печеньки':
		embed.add_field(name = 'Печеньки', value = f'Размер: {cookie_count1}')
		cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(int(cookie_count1), ctx.author.id))
		database.commit()
	elif item1 == 'Крафт 1':
		embed.add_field(name = 'Крафт №1', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft1)
	elif item1 == 'Крафт 2':
		embed.add_field(name = 'Крафт №2', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft2)
	elif item1 == 'Крафт 3':
		embed.add_field(name = 'Крафт №3', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft3)
	elif item1 == 'Крафт 4':
		embed.add_field(name = 'Крафт №4', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft4)
	elif item1 == 'Крафт 5':
		embed.add_field(name = 'Крафт №5', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft5)
	elif item1 == 'Крафт 6':
		embed.add_field(name = 'Крафт №6', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft6)
	elif item1 == 'Крафт 7':
		embed.add_field(name = 'Крафт №7', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft7)
	elif item1 == 'Крафт 8':
		embed.add_field(name = 'Крафт №8', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft8)
	elif item1 == 'Крафт 9':
		embed.add_field(name = 'Крафт №9', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft9)
	elif item1 == 'Крафт 10':
		embed.add_field(name = 'Крафт №10', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft10)

	if item2 == 'печеньки':
		embed.add_field(name = 'Печеньки', value = f'Размер: {cookie_count2}')
		cursor.execute("UPDATE users SET cash = cash + {0} WHERE id = {1}".format(int(cookie_count2), ctx.author.id))
		database.commit()
	elif item2 == 'Крафт 1':
		embed.add_field(name = 'Крафт №1', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft1)
	elif item2 == 'Крафт 2':
		embed.add_field(name = 'Крафт №2', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft2)
	elif item2 == 'Крафт 3':
		embed.add_field(name = 'Крафт №3', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft3)
	elif item2 == 'Крафт 4':
		embed.add_field(name = 'Крафт №4', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft4)
	elif item2 == 'Крафт 5':
		embed.add_field(name = 'Крафт №5', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft5)
	elif item2 == 'Крафт 6':
		embed.add_field(name = 'Крафт №6', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft6)
	elif item2 == 'Крафт 7':
		embed.add_field(name = 'Крафт №7', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft7)
	elif item2 == 'Крафт 8':
		embed.add_field(name = 'Крафт №8', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft8)
	elif item2 == 'Крафт 9':
		embed.add_field(name = 'Крафт №9', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft9)
	elif item2 == 'Крафт 10':
		embed.add_field(name = 'Крафт №10', value = 'Вы получаете рецепт крафта! Все крафты можно узнать командой !open_craft | Внимение! Крафты присылаются в лс!')
		await ctx.author.add_roles(craft10)

	await ctx.send(embed = embed)



@case.error
async def case_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(embed = discord.Embed(title = 'Не так быстро!', description = 'Ты сможешь использовать команду !case через 1 минуту!', color = 0xff0000))


# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message
# on_message





	




@client.event
async def on_message(message):
	# msg = message.content

	for row in cursor.execute(f"SELECT exp, level, cash FROM users WHERE id={message.author.id}"):
		expi = row[0]+random.randint(1, 10)
		cursor.execute(f"UPDATE users SET exp={expi} WHERE id={message.author.id}")
		lvch=expi/(row[1]*100)
		lv=int(lvch)
		# await message.channel.send(expi)
		if row[1] < lv:
			bal=100*lv
			cursor.execute(f'UPDATE users SET level={lv}, cash={bal} WHERE id={message.author.id}')
			database.commit()
			levelnow = cursor.execute(f"SELECT level FROM users WHERE id={message.author.id}").fetchone()[0]
			await message.channel.send(f'Воу! У <@{message.author.id}> новый уровень! Поздравляю! Теперь твой уровень: {levelnow}')
	await client.process_commands(message)
	database.commit()




@client.command()
async def support(ctx, *, message = 'None'):
	await ctx.message.delete()

	embed = discord.Embed(title = 'Создание тикета...', description = 'Пожалуйста, подождите пока я создаю тикет...')
	messagee = await ctx.send(embed=embed)
	role = await ctx.guild.create_role(name=ctx.author.id)
	await ctx.author.add_roles(role)
	channel = await ctx.guild.create_text_channel(ctx.author.id, reason = 'ticket')
	await channel.set_permissions(get(ctx.guild.roles, id=954405241430880306), view_channel = False)
	await channel.set_permissions(get(ctx.guild.roles, id=990661352903303188), view_channel = True)
	await channel.set_permissions(get(ctx.guild.roles, id=role.id), view_channel = True)
	await channel.send(f'<@&990661352903303188>, <@{ctx.author.id}> обратился в поддержку!')
	await channel.send(embed = discord.Embed(title = 'Вопрос / Проблема', description = message ))
	await messagee.delete()
	mesageee = await ctx.send(embed=discord.Embed(title='Тикет создан!', description = f'Тикет создан! Тикет: <#{channel.id}>'))
	await asyncio.sleep(10)
	await mesageee.delete()






@client.command()
# @commands.has_permissions(administrator = True)
async def vip(ctx, arg1, arg2 : discord.Member = None):
	role = get(ctx.guild.roles, id = 954406082636283984)
	if arg1 == 'info':
		embed = discord.Embed(title = 'Випка - Информация', description = 'Випка - это типо донат который открывает много бонусов, а именно:')
		embed.add_field(name='Роль на сервере', value = 'После покупки випки вы получите специальную роль на сервере')
		embed.add_field(name='Команды', value = 'Вы получите доступ к некоторым командам администрации потипу: !setexp и другое')
		embed.add_field(name='Значок в !profile и !rank', value = 'Рядом с вашим ником в командах !profile и !rank будет красоваться прикольный значок')
		# embed.add_field(name = ' ', value = ' ')
		embed.add_field(name = 'Хочешь випку?', value = '[Тогда кликай по этому тексту!](https://www.donationalerts.com/r/kararasenok) випка стоит всего 2 рубля или 1 гривна в месяц! И 24 рубля или 13 гривен в год! И да, при покупке випки, не забывай написать свой ник и тег в сообщении! Если вы про него забыли, обратитесь в поддержку, но тогда понадобиться докозательства оплаты (будь это скрин чека или ещё что то)')
		embed.add_field(name = 'Не получил випку?', value = 'Обратись в поддержку, выдача випки не автомизирована')


		await ctx.send(embed=embed)
	
	elif arg1 == 'add':
		if role in ctx.author.roles:
			if arg2 is None:
				await ctx.send('Укажите пользователя!')
			else:
				cursor.execute(f'UPDATE users SET vipstatus=1 WHERE id={arg2.id}')
				database.commit()

				embed = discord.Embed(title = 'Успешно!', description = f'Вы успешно выдали випку пользователю <@{arg2.id}>!', color = 0x00ff00)

				await ctx.send(embed=embed)
		else:
			await ctx.send('Недостаточно прав!')

	elif arg1 == 'delete':
		if role in ctx.author.roles:
			if arg2 is None:
				await ctx.send('Укажите пользователя!')
			else:
				cursor.execute(f'UPDATE users SET vipstatus=0 WHERE id={arg2.id}')
				database.commit()

				embed = discord.Embed(title = 'Успешно!', description = f'Вы успешно убрали випку у пользователя <@{arg2.id}>!', color = 0x00ff00)

				await ctx.send(embed=embed)
		else:
			await ctx.send('Недостаточно прав!')


@client.command()
async def rank(ctx, member : discord.Member = None):
	if member is None:
		exp = cursor.execute(f"SELECT exp FROM users WHERE id = {ctx.author.id}").fetchone()[0]
		level = cursor.execute(f"SELECT level FROM users WHERE id = {ctx.author.id}").fetchone()[0]
		vipp = cursor.execute("SELECT vipstatus FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]
		vip = int(vipp)




		embed = discord.Embed(title = 'Ранг')

		if vip == 0:
			embed.add_field(name = 'Пользователь', value = ctx.author.name)
		else:
			embed.add_field(name = 'Пользователь', value = f'{ctx.author.name}👑')
		

		embed.add_field(name = 'Опыт', value = exp)
		embed.add_field(name = 'Уровень', value = level)
	else:
		exp = cursor.execute(f"SELECT exp FROM users WHERE id = {member.id}").fetchone()[0]
		level = cursor.execute(f"SELECT level FROM users WHERE id = {member.id}").fetchone()[0]
		vipp = cursor.execute("SELECT vipstatus FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		vip = int(vipp)




		embed = discord.Embed(title = 'Ранг')
		
		if vip == 0:
			embed.add_field(name = 'Пользователь', value = member.name)
		else:
			embed.add_field(name = 'Пользователь', value = f'{member.name}👑')
		

		embed.add_field(name = 'Опыт', value = exp)
		embed.add_field(name = 'Уровень', value = level)

	await ctx.send(embed=embed)




@client.command()
async def setexp(ctx, member : discord.Member, lvl):
	role = get(ctx.guild.roles, name = '《👑》Зам. Карарасёнка')
	vipp = cursor.execute(f"SELECT vipstatus FROM users WHERE id = {ctx.author.id}").fetchone()[0]
	vip = int(vipp)

	if role in ctx.author.roles:
		cursor.execute(f"UPDATE users SET exp={lvl} WHERE id={member.id}")
		database.commit()

		embed = discord.Embed(title='Успешно!', description = f'Вы успешно изменили опыт <@{member.id}> на {lvl}')

		await ctx.send(embed=embed)
	elif vip == 1:
		cursor.execute(f"UPDATE users SET exp={lvl} WHERE id={member.id}")
		database.commit()

		embed = discord.Embed(title='Успешно!', description = f'Вы успешно изменили опыт <@{member.id}> на {lvl}')

		await ctx.send(embed=embed)
	else:
		embed=discord.Embed(title="Недостаточно прав!", description=f"<@{author_id}>, у вас не хватает прав для выполнения команды!", color=0xff0000)
		await ctx.send(embed=embed)




@client.command()
async def safe(ctx, arg1, arg2 = None, arg3 = None, arg4 = None):
	if arg1 == 'pass':
		if arg2 == 'create':
			await ctx.message.delete()
			if arg4 is None:
				await ctx.send('Повторите пароль ещё раз!')
			else:
				if arg4 == arg3:
					cursor.execute(f"UPDATE users SET safecode={arg4} WHERE id = {ctx.author.id}")
					database.commit()
					embed = discord.Embed(title = 'Успешно!', description = 'Вы успешно поставили пароль на сейф! Если вы его забудите, обратитесь в поддержку')
					await ctx.send(embed = embed)
				else:
					await ctx.send('Пароли не совпадают!')

		elif arg2 == 'delete':
			password = cursor.execute(f"SELECT safecode FROM users WHERE id = {ctx.author.id}").fetchone()[0]

			if arg3 is None:
				await ctx.send('Для удаления пароля, введите ваш текущий пароль! Если вы его забыли, обратитесь в поддержку!')
			elif int(arg3) == int(password):
				cursor.execute(f"UPDATE users SET safecode=0 WHERE id = {ctx.author.id}")
				database.commit()
				embed = discord.Embed(title = 'Успешно!', description = 'Вы успешно удалили пароль на сейф!')
				await ctx.send(embed = embed)
			else:
				await ctx.send('Пароли не совпадают! Если вы его забыли, обратитесь в поддержку!')
	elif arg1 == 'add':
		if arg2 is None:
			await ctx.send('Сколько печенек положить в сейф?')
		elif arg2 == 'all':
			bal = int(cursor.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}").fetchone()[0])

			password = cursor.execute(f"SELECT safecode FROM users WHERE id = {ctx.author.id}").fetchone()[0]

			if int(arg3) == int(password):
				await ctx.message.delete()

				cursor.execute(f"UPDATE users SET cash = cash - {bal} WHERE id = {ctx.author.id}")
				cursor.execute(f"UPDATE users SET safe = safe + {bal} WHERE id = {ctx.author.id}")

				database.commit()

				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'Ты успешно переложил в сейф {bal} :cookie:'))
		else:
			password = cursor.execute(f"SELECT safecode FROM users WHERE id = {ctx.author.id}").fetchone()[0]

			if int(arg3) == int(password):
				await ctx.message.delete()
				bal = int(cursor.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}").fetchone()[0])
				if int(arg2) > bal:
					await ctx.send('Слишком много!')
				else:

					cursor.execute(f"UPDATE users SET cash = cash - {arg2} WHERE id = {ctx.author.id}")
					cursor.execute(f"UPDATE users SET safe = safe + {arg2} WHERE id = {ctx.author.id}")

					database.commit()

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'Ты успешно переложил в сейф {arg2} :cookie:'))
	elif arg1 == 'take':
		if arg2 is None:
			await ctx.send('Сколько печенек взять из сейфа?')
		elif arg2 == 'all':
			bal = int(cursor.execute(f"SELECT safe FROM users WHERE id = {ctx.author.id}").fetchone()[0])

			password = cursor.execute(f"SELECT safecode FROM users WHERE id = {ctx.author.id}").fetchone()[0]

			if int(arg3) == int(password):
				await ctx.message.delete()

				cursor.execute(f"UPDATE users SET safe = safe - {bal} WHERE id = {ctx.author.id}")
				cursor.execute(f"UPDATE users SET cash = cash + {bal} WHERE id = {ctx.author.id}")

				database.commit()

				await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'Ты успешно взял из сейфа {bal} :cookie:'))
		else:
			password = cursor.execute(f"SELECT safecode FROM users WHERE id = {ctx.author.id}").fetchone()[0]

			if int(arg3) == int(password):
				await ctx.message.delete()
				bal = int(cursor.execute(f"SELECT safe FROM users WHERE id = {ctx.author.id}").fetchone()[0])
				if int(arg2) > bal:
					await ctx.send('Слишком много!')
				else:

					cursor.execute(f"UPDATE users SET cash = cash + {arg2} WHERE id = {ctx.author.id}")
					cursor.execute(f"UPDATE users SET safe = safe - {arg2} WHERE id = {ctx.author.id}")

					database.commit()

					await ctx.send(embed=discord.Embed(title = 'Успешно!', description = f'Ты успешно взял из сейфа {arg2} :cookie:'))




@client.command()
async def safe_hack(ctx, arg2 : discord.Member = None):
	role = get(ctx.guild.roles, id=990963555685769246)

	if arg2 is None:
		await ctx.send('Укажите пользователя!')
	else:

		if role in ctx.author.roles:
			faill = ['yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no']
			fail = random.choice(faill)

			if fail == 'yes':
				await ctx.send(embed=discord.Embed(title='Взлом сейфа', description = f'Вы решили взломать сейф <@{arg2.id}> но у вас сломалась отмычка! Придётся покупать новую и пробовать ещё раз =)'))
				await ctx.author.remove_roles(role)
			else:
				await ctx.send(embed=discord.Embed(title='Взлом сейфа', description = f'Вы решили взломать сейф <@{arg2.id}> и у вас получилось! Код был отправлен в лс!'))
				await ctx.author.remove_roles(role)

				code = cursor.execute(f"SELECT safecode FROM users WHERE id = {arg2.id}").fetchone()[0]

				await ctx.author.send(f'Код: {code}')

				hacked_user = await client.fetch_user(arg2.id)

				await hacked_user.send(embed=discord.Embed(title='Твой код взломан!', description = f'Привет <@{arg2.id}>! У меня для тебя не очень хорошие новости, твой код от сейфа был взломан! Его взломал {ctx.author.name}. Настоятельно рекомендую быстренько его сменить! Если ты его забыл, обратись в поддержку!'))
		else:
			await ctx.send('У вас нет отмычки!')


		
@client.command()
async def close_ticket(ctx, role : discord.Role):
	rolle = get(ctx.guild.roles, id = 990661352903303188)
	if rolle in ctx.author.roles:
		await ctx.send('Закрытие тикета...')
		await asyncio.sleep(3)
		await ctx.channel.delete()
		await role.delete()
	else:
		await ctx.send(embed=discord.Embed(title='Недостаточно прав!', description = 'Эту команду может использовать **ТОЛЬКО** <@&990661352903303188>!'))



@client.command()
async def rob(ctx, member : discord.Member, code = None):
	if member.id == ctx.author.id:
		await ctx.send('Вы не можете своровать у себя!')
	else:
		ball = cursor.execute(f"SELECT cash FROM users WHERE id = {member.id}").fetchone()[0]
		bal = int(ball)


		safe_ball = cursor.execute(f"SELECT safe FROM users WHERE id = {member.id}").fetchone()[0]
		safe_bal = int(safe_ball)

		if bal < 2:
			if code is None:
				await ctx.send(embed=discord.Embed(title='Ошибка!', description = 'У данного человека нету пиченек, либо они все в сейфе!'))
			else:
				codee = cursor.execute(f"SELECT safecode FROM users WHERE id = {member.id}").fetchone()[0]

				safe_code = int(codee)

				if int(code) == safe_code:
					faill = ['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no']
					fail = random.choice(faill)

					if fail == 'yes':
						grabbed = int(random.uniform(0, safe_bal))
						cursor.execute(f"UPDATE users SET cash = cash - {grabbed} WHERE id = {ctx.author.id}")
						database.commit()
						await ctx.send(embed = discord.Embed(title = 'Своровать пиченьки', description = f'Вы захотели своровать печенек, но у вас не получилось, с вас было снято {grabbed} :cookie:'))
					else:
						grabbed = int(random.uniform(0, safe_bal))

						cursor.execute(f"UPDATE users SET safe = safe - {grabbed} WHERE id = {member.id}")
						cursor.execute(f"UPDATE users SET cash = cash + {grabbed} WHERE id = {ctx.author.id}")
						database.commit()
						await ctx.send(embed = discord.Embed(title = 'Своровать пиченьки', description = f'Вы захотели своровать печенек и у вас получилось! Вы стырили {grabbed} :cookie:'))

				else:
					await ctx.send('Код неправельный!')
		else:
			faill = ['yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no']
			fail = random.choice(faill)

			if fail == 'yes':
				grabbed = int(random.uniform(0, safe_bal))
				cursor.execute(f"UPDATE users SET cash = cash - {grabbed} WHERE id = {ctx.author.id}")
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Своровать пиченьки', description = f'Вы захотели своровать печенек, но у вас не получилось, с вас было снято {grabbed} :cookie:'))
			else:
				grabbed = int(random.uniform(0, safe_bal))

				cursor.execute(f"UPDATE users SET safe = safe - {grabbed} WHERE id = {member.id}")
				cursor.execute(f"UPDATE users SET cash = cash + {grabbed} WHERE id = {ctx.author.id}")
				database.commit()
				await ctx.send(embed = discord.Embed(title = 'Своровать пиченьки', description = f'Вы захотели своровать печенек и у вас получилось! Вы стырили {grabbed} :cookie:'))


@client.command()
async def all_codes(ctx):
	role = get(ctx.guild.roles, id=954405952596099072)

	if role in ctx.author.roles:

		embed = discord.Embed(title = 'Пароли от сейфов всех пользователей')
		for row in cursor.execute(f"SELECT safecode, name FROM users WHERE server_id = {ctx.guild.id}"):
			if row[0] <= 0:
				# embed.add_field(name = f'Пароль пользователя {row[1]}', value = f'Пароль не установлен')
				pass
			else:
				embed.add_field(name=f'Пароль пользователя {row[1]}', value = f'Пароль: {row[0]}', inline = False)
		await ctx.author.send(embed=embed)
	else:
		await ctx.send('Данная команда доступна только создателю сервера!')



@client.command()
async def update(ctx):
	await ctx.send('Обновление базы данных....')
	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, {guild.id}, 0, 0, 1, 0, 0, 0)")
			else:
				pass
	database.commit()
	await ctx.send('База данных обнавлена!')


@client.command()
async def nsfw_send(ctx, *, url):
	channel = await client.fetch_channel(992800480415715479)
	await ctx.send('Ссылка отправлена на модерацию =) Ожидайте!')
	await channel.send(embed=discord.Embed(title = f'{ctx.author} отправил ссылку на модерацию!', description = f'Ссылка: {url}'))

@client.command()
@commands.has_permissions(administrator = True)
async def nsfw_add(ctx, url):
	server = ctx.guild.id
	server_id = int(server)
	cursor.execute("INSERT INTO nsfw(url, serverid) VALUES ('{}', {})".format(url, ctx.guild.id))
	database.commit()
	idd = cursor.execute("SELECT id FROM nsfw WHERE url = '{}'".format(url)).fetchone()[0]
	await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'Вы успешно добавили nsfw-ссылку в бота! ID: {idd}'))


@client.command()
@commands.has_permissions(administrator=True)
async def nsfw_delete(ctx, nsfw_id):
	cursor.execute("DELETE FROM nsfw WHERE id = {}".format(nsfw_id))
	database.commit()
	await ctx.send(embed = discord.Embed(title = 'Успешно!', description = 'Вы успешно удалили nsfw-ссылку с бота!'))


@client.command()
async def nsfw(ctx, nsfw_idd = None):
	if nsfw_idd is None:
		channels = [987749483163025428, 992800480415715479]
		if ctx.channel.id in channels:
			ids = []
			for row in cursor.execute("SELECT id FROM nsfw WHERE serverid = {}".format(ctx.guild.id)):
				ids += str(row[0])

			nsfw_id = int(random.choice(ids))

			nsfw_content = cursor.execute("SELECT url FROM nsfw WHERE id = {}".format(int(nsfw_id))).fetchone()[0]

			# embed = discord.Embed(title = 'NSFW', description = f'ID: {nsfw_id}')
			# embed.set_image(url = nsfw_content)

			await ctx.send(f'{nsfw_content} | ID: {nsfw_id}')
		else:
			await ctx.send('Это не NSFW канал!')
	else:
		channels = [987749483163025428, 992800480415715479]
		if ctx.channel.id in channels:
			nsfw_content = cursor.execute("SELECT url FROM nsfw WHERE id = {}".format(int(nsfw_idd))).fetchone()[0]

			await ctx.send(f'{nsfw_content} | ID: {nsfw_idd}')
		else:
			await ctx.send('Это не NSFW канал!')




@client.command()
async def gd_lvl_req(ctx, lvl_id, *, youtube_video = None):
	message = await ctx.send(embed=discord.Embed(title = 'Оценка уровня', description = f'{ctx.author} отправил уровень на оценку!\n \n ID: {lvl_id}\nВидео на YouTube: {youtube_video}'))

	await message.add_reaction('👍')
	await message.add_reaction('👎')




@client.command()
async def box(ctx):
	items = ['Coins', 'StarPower', 'StarPower', 'StarPower', 'StarPower', 'StarPower', 'StarPower', 'Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','Coins','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower','StarPower', 'rare', 'rare', 'rare', 'rare', 'rare', 'rare', 'rare', 'superrare', 'superrare','superrare','superrare','superrare', 'Epic','Epic','Epic','Epic','Epic', 'Mythic','Mythic','Mythic', 'Legendary', 'Legendary', 'Chromatic']
	rare = ['El primo', 'Barley', 'Poco', 'Rosa']
	superrare = ['Rico', 'Carl', 'Penny', 'Darryl', 'Jacky']
	epic = ['Piper', 'Pam', 'Frank', 'Bibi', 'Bea', 'Nani', 'Edgar', 'Griff', 'Grom', 'Bonnie']
	mythic = ['Mortis', 'Tara', 'Gene', 'Max', 'Mr P', 'Sprout', 'Byron', 'Squeak']
	legendary = ['Spike', 'Crow', 'Leon', 'Sandy', 'Amber', 'Meg']
	chromatic = ['Gale', 'Surge', 'Colette', 'Lou', 'Colonel Ruffs', 'Belle', 'Buzz', 'Ash', 'Lola', 'Fang', 'Eve', 'Janet', 'Otis']

	embed = discord.Embed(title = 'Бравл Старс - Ящик')

	item1 = random.choice(items)
	item2 = random.choice(items)


	if item1 == 'rare':
		brawler = random.choice(rare)
		embed.add_field(name = f'Новый Бравлер!', value = f':green_heart: {brawler} :green_heart:')
	elif item1 == 'superrare':
		brawler = random.choice(superrare)
		embed.add_field(name = f'Новый Бравлер!', value = f':blue_heart: {brawler} :blue_heart:')
	elif item1 == 'epic':
		brawler = random.choice(epic)
		embed.add_field(name = f'Новый Бравлер!', value = f':purple_heart: {brawler} :purple_heart:')
	elif item1 == 'mythic':
		brawler = random.choice(mythic)
		embed.add_field(name = f'Новый Бравлер!', value = f':heart: {brawler} :heart:')
	elif item1 == 'legendary':
		brawler = random.choice(mythic)
		embed.add_field(name = f'Новый Бравлер!', value = f':yellow_heart: {brawler} :yellow_heart:')
	elif item1 == 'chromatic':
		brawler = random.choice(chromatic)
		embed.add_field(name = f'Новый Бравлер!', value = f':orange_heart: {brawler} :orange_heart:')
	elif item1 == 'Coins':
		coins = random.randint(1, 100)
		embed.add_field(name = 'Монеты', value = f'{coins}')
	elif item1 == 'StarPower':
		starpower = random.randint(1, 100)
		embed.add_field(name = 'Очки силы', value = f'{starpower}')


	if item2 == 'rare':
		brawler = random.choice(rare)
		embed.add_field(name = f'Новый Бравлер!', value = f':green_heart: {brawler} :green_heart:')
	elif item2 == 'superrare':
		brawler = random.choice(superrare)
		embed.add_field(name = f'Новый Бравлер!', value = f':blue_heart: {brawler} :blue_heart:')
	elif item2 == 'epic':
		brawler = random.choice(epic)
		embed.add_field(name = f'Новый Бравлер!', value = f':purple_heart: {brawler} :purple_heart:')
	elif item2 == 'mythic':
		brawler = random.choice(mythic)
		embed.add_field(name = f'Новый Бравлер!', value = f':heart: {brawler} :heart:')
	elif item2 == 'legendary':
		brawler = random.choice(mythic)
		embed.add_field(name = f'Новый Бравлер!', value = f':yellow_heart: {brawler} :yellow_heart:')
	elif item2 == 'chromatic':
		brawler = random.choice(chromatic)
		embed.add_field(name = f'Новый Бравлер!', value = f':orange_heart: {brawler} :orange_heart:')
	elif item2 == 'Coins':
		coins = random.randint(1, 100)
		embed.add_field(name = 'Монеты', value = f'{coins}')
	elif item2 == 'StarPower':
		starpower = random.randint(1, 100)
		embed.add_field(name = 'Очки силы', value = f'{starpower}')


	await ctx.send(embed = embed)








	
		



#alive.keep_alive()






		





client.run(bot_token)
