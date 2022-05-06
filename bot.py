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
# import alive




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

	channel = await client.fetch_channel(959111892364820500)

	time = datetime.datetime.now()

	embed = discord.Embed(title = 'Бот запущен!', description = 'Вы можете использовать бота!', color = 0x00ff00)
	embed.set_footer(text = f'Запустился: {time}')	

	await channel.send(embed=embed)

	cursor.execute("""CREATE TABLE IF NOT EXISTS users(
			name TEXT,
			id INT,
			cash BIGINT,
			rep INT,
			lvl INT,
			server_id INT,
			warns INT
		)""")

	for guild in client.guilds:
		for member in guild.members:
			if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
				cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, {guild.id}, 0)")
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


@client.event
async def on_member_join(member):
	if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
		cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, {member.guild.id}, 0)")
		database.commit()
	else:
		pass

		





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
		embed=discord.Embed(title="Выберите котегорию:", description="!help mod\n!help fun\n!help other\n!help info\n!help economy\n", color=0x0000ff)
	elif cotegory == 'mod':
		embed=discord.Embed(title="Команды бота - Модерация", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент", color=0x0000ff)
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
		embed.add_field(name='!buy "[придмет]" {кол-во}', value='Купить что то (пример: !buy "хлеб" 2)', inline=True)
		embed.add_field(name='!calc [пример]', value='калькулятор (пример команды: !calc 2+2)', inline=True)
		embed.add_field(name='!strcount {что нужно найти в сообщении} {сообщение}', value='Поиск слова/буквы/слога в сообщении')
		embed.add_field(name='!coin <Орёл | Решка>', value = 'Орёл или Решка')
		embed.add_field(name='!rps <Камень | Ножницы | Бумага>', value = 'Камень, Ножницы, Бумага')
	elif cotegory == 'other':
		embed=discord.Embed(title="Команды бота - Прочее", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент", color=0x0000ff)
		embed.add_field(name="!suggest [идея]", value="отправить идею", inline=True)
		embed.add_field(name="!sos [нарушитель] {причина}", value="Оповестить модерацию о нарушителе", inline=True)
	elif cotegory == 'info':
		embed=discord.Embed(title="Команды бота - Информация", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент", color=0x0000ff)
		embed.add_field(name='!changelog', value='Список Изменений бота', inline=True)
		embed.add_field(name='!about', value='мини информация о боте', inline=True)
		embed.add_field(name='!server', value='Показывает информацию о сервере', inline=True)
	elif cotegory == 'economy':
		embed=discord.Embed(title="Команды бота - Экономика", description="Аргументы:\n[] - обязательный аргумент\n{} - необязательный аргумент", color=0x0000ff)
		embed.add_field(name='!balance {юзер}', value = 'Посмотреть баланс пользователя')
		embed.add_field(name='!addmoney [юзер] [сколько передать]', value = 'Добавить печеньки к пользователю')
		embed.add_field(name='!remmoney [юзер] [сколько отнять]', value = 'Отнимает печеньки у пользователя')
		embed.add_field(name='!resetmoney {юзер}', value = 'Сбросить печеньки')
		embed.add_field(name='!work', value = 'подзароботать печенек')
		embed.add_field(name='!givemoney [юзер] [сколько передать]', value = 'Передать печеньки пользователю')
		embed.add_field(name='!rate [юзер] [сколько звёзд]', value = 'Поставить оценку (репутацию) юзеру')
		embed.add_field(name='!lb', value = 'Лидерборд по печенькам')
		embed.add_field(name='!promo {промокод}', value = 'Активировать промокод или узнать о них')
	else:
		await ctx.send('Неизвестная котегория!')



	await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, user: discord.Member, mute_time = '0', *, reason = 'None'):
	mute_role = get(ctx.message.guild.roles, name='Impostor')
	default_role = get(ctx.message.guild.roles, name='Рыбка')
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
	mute_role = discord.utils.get(ctx.message.guild.roles, name='Impostor')
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
	mod = ctx.message.author
	member_id = member.id
	memebir_id = await client.fetch_user(member_id)

	await memebir_id.send(f'Вы были забанены на сервере **Море с рыбами | Карарасёнок =)**\nМодератор: {mod}\nПричина: {reason}')

	await member.ban(reason=reason)
	embed=discord.Embed(title="Участник забанен!", description=f"Пользователь {member} был забанен по причине: {reason}", color=0x00ff00)
	await ctx.send(embed=embed)
	

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
async def create_role(ctx, permissionsid = 0, *, name = 'No Name'):
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
async def buy(ctx, item = 'None', count = 1):
	if item == 'None':
		await ctx.send('Вы забыли сказать что вы хотите купить!')
	else:
		author_id = ctx.message.author.id

		await ctx.send(f'<@{author_id}> купил {item} в количестве {count} штук(-а / -и)!')



@client.command()
async def about(ctx):
	embed=discord.Embed(title="Немного о нас", description="Привет! Это бот Амогус 228! Он создан для сервера Море с рыбами | Карарасёнок =)\nСоздал <@640926869948203030>\n**Соц Сети создателя**\n[YouTube](https://www.youtube.com/channel/UCnPdFplgMbo5pNPoBJf0kIQ)\n[Telegram](https://t.me/prime_eight_team)\n \n[Донаты (DonationAlerts)](https://www.donationalerts.com/r/kararasenok)\n[Донаты + контент которого нет на ютуб канале (Boosty)](https://boosty.to/kararasenochek)", color=0x1100ff)
	await ctx.send(embed=embed)



@client.command(aliases = ['changelog'])
async def change_log(ctx):
	embed=discord.Embed(title="Последние изменения", description="Версия 0.4 (<t:1648155600:D>(<t:1648155600:R>)):\n- Добавлена команда !about и !changelog\n - Бот работает теперь круглосуточно с небольшими перебоями!\n \nВерсия 0.5 (<t:1648155600:D>(<t:1648155600:R>))\n- Добавлен новый текст в Rich Presence\n \nВерсия 0.6 (<t:1648242000:D>(<t:1648242000:R>))\n- Добавлена команда !calc\n \nВерсия 0.7 (<t:1648760400:D>(<t:1648760400:R>))\n- Немного изменена команда !mute\n- Добавлено уведомление на сервере о включении бота\n- Добавлено сообщение если команды нет (к примеру: команды !test2373465736 нет и бот скажет что команда не существует)\n- Немного изменена команда !verify\n \nВерисия 0.8 (<t:1648846800:D>(<t:1648846800:R>))\n- Добавлена команда !server\n- Добавлены команды !close и !open\n- Добавлены команды !setup и !setupnosend\n- Добавлена команда !card\n- Добавлено сообщение если недостаточно прав на выполнение команды\n \nВерсия 0.9 (<t:1648933200:D>(<t:1648933200:R>))\n- Добавлено 2 новых сообщения об ошибке (неизвестная ошибка / пропушен обязательный аргумент)\n- Была изменена команда !mute\n- Добавлена команда !echo_embed\n \nВерсия 1.0 (<t:1649538000:D>(<t:1649538000:R>))\n- Добавлена команда !strcount\n- Была изменена команда !help\n \nВерсия 1.1 CodeName: Global (<t:1649710800:D> - <t:1649797200:D>(<t:1649797200:R>))\n- Добавлена экономика (!help economy)\n- Добавлена команда !profile\n \nВерсия 1.2 (<t:1649883600:D>(<t:1649883600:R>))\n- Добавлена команда !leaderboard\n- Добавлен коулдаун на команду !work\n \nВерсия 1.3 (<t:1650747600:D>(<t:1650747600:R>))\n- Добавлена команда !warn и !remwarn\n- Добавлен пункт 'Предупреждения' в команду !profile\n- Исправлено парочка багов\n \nВерсия 1.4 (<t:1651501776:f>(<t:1651501776:R>))\n- Исправлен баг с кодировкой\n- Добавлена команда !rps и !coin\n- Добавлены промокоды (!promo)\n \nВерсия 1.5 (<t:1651595343:f>(<t:1651595343:R>))\n- Добавлена команда !mute_setup\n- Была изменена команда !mute\n- Исправлены баги", color=0x0000ff)
	embed.set_footer(text="Версия бота: 1.5")
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
	elif isinstance(error, commands.CommandOnCooldown):
		embed=discord.Embed(title="Не так быстро!", description=f"<@{ctx.author.id}>, на команду стоит ограничение по времени использования!", color=0xff0000)
		await ctx.send(embed=embed)
	else:
		embed=discord.Embed(title="Неизвестная ошибка!", description=f"<@{author_id}>, произошла неизвестная ошибка! Пожалуйста, сообщите о ней создателю!", color=0xff0000)
		await ctx.send(embed=embed)





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
		await ctx.send(embed = discord.Embed(title = f'Баланс пользователя {ctx.author}', description = f'Баланс: {cursor.execute("SELECT cash FROM users WHERE id = {}".format(ctx.author.id)).fetchone()[0]} :cookie:'))
	else:
		await ctx.send(embed = discord.Embed(title = f'Баланс пользователя {member}', description = f'Баланс: {cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]} :cookie:'))


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
		database.commit()

		await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'<@{ctx.author.id}> вы успешно сбросили печеньки!', color = 0x00ff00))

	else:
		cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
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





@client.command(aliases = ['pay', 'give', 'givemoney'])
async def give_money(ctx, member : discord.Member = None, amount = None):
	if member is None:
		await ctx.send('Укажите кому передать!')
	else:
		if amount is None:
			await ctx.send('Укажите сколько передать!')
		elif int(amount) < 1:
			await ctx.send('Задайте значение больше 1!')
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
		elif stars > 5:
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
		user_id = ctx.message.author.id
		user_name = ctx.author.name
		user_avatar = ctx.author.avatar_url

		embed =	discord.Embed(title = f'Статистика пользователя {user_name}', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)
		embed.set_footer(text = f'Запросил: {ctx.author.name}', icon_url = user_avatar)
		embed.set_thumbnail(url = user_avatar)
		embed.add_field(name = 'Ник', value = user_name)
		embed.add_field(name = 'АйДи', value = user_id)
		embed.add_field(name = 'Печеньки (деньги)', value = money)
		embed.add_field(name = 'Репутация', value = reputation)
		embed.add_field(name = 'Предупреждения', value = f'{warns}/5')

		await ctx.send(embed = embed)
	else:
		money = cursor.execute("SELECT cash FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		reputation = cursor.execute("SELECT rep FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		warns = cursor.execute("SELECT warns FROM users WHERE id = {}".format(member.id)).fetchone()[0]
		user_id = member.id
		user_name = member.name
		user_avatar = member.avatar_url


		embed =	discord.Embed(title = f'Статистика пользователя {user_name}', description = 'Тут указана подробная информация о пользователе', color = 0x0000ff)
		embed.set_footer(text = f'Запросил: {ctx.author.name}', icon_url = ctx.author.avatar_url)
		embed.set_thumbnail(url = user_avatar)
		embed.add_field(name = 'Ник', value = user_name)
		embed.add_field(name = 'АйДи', value = user_id)
		embed.add_field(name = 'Печеньки (деньги)', value = money)
		embed.add_field(name = 'Репутация', value = reputation)
		embed.add_field(name = 'Предупреждения', value = f'{warns}/5')

		await ctx.send(embed = embed)


@client.command(aliases = ['lb'])
async def leaderboard(ctx):
	embed = discord.Embed(title = 'Топ 10 по печенькам')
	counter = 0

	for row in cursor.execute("SELECT name, cash FROM users WHERE server_id = {} ORDER BY cash DESC LIMIT 10".format(ctx.guild.id)):
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
			await ctx.send(embed = discord.Embed(title = 'Успешно!', description = f'Модератор <@{ctx.author.id}> убрал 1 пред у <@{member.id}>! Теперь у <@{member.id}> {warns}/5 предов!'))


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




# alive.keep_alive()





		





client.run(bot_token)