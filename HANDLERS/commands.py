from logging import currentframe
from aiogram import types, exceptions
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup


from dispatcher import dp, bot
from .keyboards import *
from .functions import *
import Datapacks


from pathlib import Path


#Команда /start обернута в декоратор dp.message_handler, можна було не використовувати декоратор, 
#а написати в кінці файлу dp.add_handler(CommandHandler('start', start))

@dp.message_handler(commands= ["start"], commands_prefix="/")
async def start(message: types.Message):
	if message.chat.type != 'private':
		return
	else: await message.bot.send_message(chat_id=message.chat.id, 
									  text="Привіт це бот який допоможе тобі знайти роботу!", 
									  parse_mode="Markdown", reply_markup=menu_keyboard())


@dp.message_handler(Text(equals='Меню', ignore_case=True), state = '*')
async def menu(message: types.Message, state: FSMContext):
	if await state.get_state() is not None:
		await state.finish()
	if message.chat.type != 'private':
		return
	else: await message.bot.send_message(chat_id=message.chat.id, 
									  text="Ти перейшов до головного меню!", 
									  parse_mode="Markdown", reply_markup=menu_keyboard())


@dp.message_handler(Text(equals='Допомога', ignore_case=True))
async def send_help(message: types.Message):
	text = """Пошук роботи – процес не з легких, особливо, якщо ви це робите вперше. Наші поради допоможуть досягти позитивного результату.
	1. Визначте список своїх слабких і сильних сторін
		Почніть з того, що визначте свої сильні і слабкі професійні сторони. Випишіть їх в список. Він стане в нагоді вам, коли  будете готувати резюме, зіставляти свої вміння і навички з вимогами роботодавця, писати супровідний лист або готуватися до співбесіди.
		Навіть якщо без списку ви усвідомлюєте свої професійні переваги, коли оформите все на папері, буде набагато простіше орієнтуватися при пошуку роботи і резюме.
	2. Актуалізуйте своє резюме
		Ваше резюме повинне бути актуальним. Шукаючи роботу, завжди вносьте зміни щодо місця роботи, обов'язків, нових навичок, результатів роботи, пройдених майстер-класів або тренінгів.
		Не виключено, що вам доведеться трохи переробити своє резюме, зробивши акцент на тих уміннях і навичках, які більш важливі для конкретного роботодавця, але в будь-якому випадку кістяк резюме буде готовий.
	3. Розкажіть знайомим і друзям, що шукаєте роботу
		Не варто недооцінювати можливості, які може надати живе спілкування. Можливо, робота сама знайде вас або ж вам повідомлять про вакансію, яку поки не опублікували на сайтах пошуку роботи чи на сторінці компанії, або ви її не помітили.
	4. Зорієнтуйтеся на ринку праці
		Навіть якщо ви ще тільки починаєте шукати роботу, спробуйте зорієнтуватися, що відбувається на ринку праці. Почитайте профільні статті, перегляньте вакансії, щоб зрозуміти актуальні вимоги роботодавців, поговоріть з професіоналами у своїй сфері. Не варто переоцінювати ситуацію або навпаки – виключати наявність можливостей і стверджувати, що нічого знайти не можна, шанси працевлаштуватися завжди є.
	5. Запасіться витримкою і завзятістю
		Якщо ви з самого початку будете налаштовані, що пошук роботи може зайняти певний час і що відмови роботодавців є невід'ємною частиною цього процесу – ви захистите себе від багатьох неприємних моментів.
		Головне – не витрачати цей час даремно. Намагайтеся розвиватися, розширювати професійні знання. Навіть якщо відразу не вдається знайти підходящу вакансію, намагайтеся продовжувати бути активним в пошуку роботи і не втрачати мотивацію."""
	await message.bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown")


@dp.message_handler(Text(equals='ФАО', ignore_case=True))
async def send_fao(message: types.Message):
	info ="Це фао бота, оберіть розділ який вас цікавить:"
	if message.chat.type != 'private':
		return
	else: await message.bot.send_message(chat_id=message.chat.id, text=info, parse_mode="Markdown", reply_markup=fao_keyboard())


@dp.message_handler(Text(equals='Гід', ignore_case=True))
async def send_gid(message: types.Message):
	await message.reply(Datapacks.gid)


@dp.message_handler(Text(equals='Робота', ignore_case=True))
async def send_works(message: types.Message):
	if message.chat.type != 'private':
		return
	else: await message.bot.send_message(chat_id=message.chat.id, text="Вакансії які зараз доступні", 
									  parse_mode="Markdown", reply_markup=work_keyboard())


@dp.message_handler(Text(equals='Переглянути анкету', ignore_case=True))
async def send_anketa_action(message: types.Message):
	text = await see_file(message.from_user.id)
	await message.reply(text=text)
	

@dp.message_handler(Text(equals='Видалити анкету', ignore_case=True))
async def delete_action(message: types.Message):
	text = await delete_file(message.from_user.id)
	await message.reply(text=text)


#Частина логіки бота зв`язана зі станами кінцевого автомату, стани зберігаються в оперативній пам`яті,
#тому при перезапускі бота  поточні стани буде зкинуто, якщо потрібно зробити, 
#щоб вони не втрачалися бібліотека може працювати з NoSql базами даних Redis та Vedis


#Клас кінцевого автомату, тут задаються всі стани роботи бота
class FSM(StatesGroup):
	user_id = State()
	name = State()
	age = State()
	skills = State()
	phone = State()
	file_ = State()
	fin = State()


#Хендлер обернутий в декоратор який задає стан роботи з документами
@dp.message_handler(Text(equals='Відіслати резюме', ignore_case=True))
async def send_cv(message: types.Message, state: FSMContext):
	text ="Надішли мені файл з резюме!"
	if message.chat.type != 'private':
		return
	else: 
		await message.bot.send_message(chat_id=message.chat.id, text=text, parse_mode="Markdown", reply_markup=file_menu_keyboard())
		await FSM.file_.set()


#Хендлер обернутий в декоратор який отримує всі повідомлення з документами, якщо поточний стан є станом роботи з документами
@dp.message_handler(state=FSM.file_ ,content_types=['document'])
async def save_files(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return
	file = await message.document.get_file()

	#path = "download/documents/"
	ext = Path(f"{file['file_path']}").suffix
	await bot.download_file(file_path = file.file_path, destination = f"download/documents/{message.from_user.id}{ext}")

	await message.reply("Я скачав твій файл",reply_markup = menu_keyboard())
	await state.finish()


#Хендлер обернутий в декоратор який отримує повідомлення команду та задає початковий стан для реєстрації
@dp.message_handler(Text(equals= "Реєстрація"))
async def registration_action(message: types.Message, state: FSMContext):
	if await check_user(message.from_user.id) == False:
		await message.answer('Почнемо реєстрацію!\nНаписни на кнопку і введи свої дані.\n Якщо хочеш відмінити реєстрацію натисни "Скасувати реєстрацію".\nЯкщо хочеш відмінити дію натисни"Відміна"та обери іншу дію.',
					  reply_markup = reg_keyboard())
		await FSM.user_id.set()
		async with state.proxy() as data:
			data['user_id'] = message.from_user.id
	else:
		await message.reply("Ти вже заповнив анкету!")


#Хендлер обернутий в декоратор який реагує на текстове повідомлення 'ПІБ', змінює стан користувача на введення ПІБ
@dp.message_handler(Text(equals='ПІБ', ignore_case=True), state='*')
async def name_handler(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
	await FSM.name.set()
	await message.answer("Введіть свій ПІБ:")


#Хендлер обернутий в декоратор який реагує на всі текстові повідомлення та записує їх в словник , якщо повідомлення задовільняє всі параметри
@dp.message_handler(state=FSM.name)
async def name_handler_rec(message: types.Message, state: FSMContext):
	text = name = ''
	if message.text == 'Вік':
		await FSM.age.set()
		text = "Введіть свій вік:"
	elif message.text == 'Навички':
		await FSM.skills.set()
		text = "Введіть свої навички:"
	elif message.text == 'Номер телефону':
		await FSM.phone.set()
		text = "Введіть свій номер телефону:"
	elif message.text == 'Відміна':
		await FSM.fin.set()
		text = "Дію відмінено, тепер ти можеш завершити реєстрацію або обрати іншу дію!"
	elif message.text == 'Завершити реєстрацію':
		text = 'Ти не завершив поточну дію, натисни "Відміна" і тоді ти зможеш завершити реєстрацію'
	else:
		name = message.text
		await FSM.fin.set()
		if name.replace(' ', '').isalpha():
			async with state.proxy() as data:
				data['name'] = name
			text = "Виберіть наступний крок."
		elif [s for s in name if s in '1234567890']:
			async with state.proxy() as data:
				data['name'] = name
			text = "Введіть свій ПІБ без цифр!"
		else:
			text = "Перевірте правильність введених даних!"
	await message.answer(text)
	

@dp.message_handler(Text(equals='Вік', ignore_case=True), state='*')
async def age_handler(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return
	await FSM.age.set()
	await message.answer("Введіть свій вік:")


@dp.message_handler(state=FSM.age)
async def age_handler_rec(message: types.Message, state: FSMContext):
	text=''
	if message.text == 'ПІБ':
		await FSM.name.set()
		text ="Введіть свій ПІБ:"
	elif message.text == 'Навички':
		await FSM.skills.set()
		text ="Введіть свої навички:"
	elif message.text == 'Номер телефону':
		await FSM.phone.set()
		text ="Введіть свій номер телефону:"
	elif message.text == 'Відміна':
		await FSM.fin.set()
		text = "Дію відмінено, тепер ти можеш завершити реєстрацію або обрати іншу дію!"
	elif message.text == 'Завершити реєстрацію':
		text = 'Ти не завершив поточну дію, натисни "Відміна" і тоді ти зможеш завершити реєстрацію'
	else:
		if message.text.isnumeric() and 18 <= int(message.text) <= 100:
			async with state.proxy() as data:
				data['age'] = message.text
			text = 'Виберіть наступний крок.'
			await FSM.fin.set()

		else:
			text = "Відповідь має містити лише числа!\nА також діапазон введеного значення має знаходитись від 18 до 100!"
	await message.answer(text)

@dp.message_handler(Text(equals='Навички', ignore_case=True), state='*')
async def skills_handler(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return
	await FSM.skills.set()
	await message.answer("Введіть свої навички:")


@dp.message_handler(state=FSM.skills)
async def skills_handler_rec(message: types.Message, state: FSMContext):
	text=''
	if message.text == 'ПІБ':
		await FSM.name.set()
		text = "Введіть свій ПІБ:"
	elif message.text == 'Вік':
		await FSM.age.set()
		text = "Введіть свій вік:"
	elif message.text == 'Номер телефону':
		await FSM.phone.set()
		text = "Введіть свій номер телефону:"
	elif message.text == 'Відміна':
		await FSM.fin.set()
		text = "Дію відмінено, тепер ти можеш завершити реєстрацію або обрати іншу дію!"
	elif message.text == 'Завершити реєстрацію':
		text = 'Ти не завершив поточну дію, натисни "Відміна" і тоді ти зможеш завершити реєстрацію'
	else:
		async with state.proxy() as data:
			data['skills'] = message.text
		text = "Виберіть наступний крок."
		await FSM.fin.set()
	await message.answer(text)


@dp.message_handler(Text(equals='Номер телефону', ignore_case=True), state='*')
async def phone_handler(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return
	await FSM.phone.set()
	await message.answer("Введіть свій номер телефону:")


@dp.message_handler(state=FSM.phone)
async def phone_handler_rec(message: types.Message, state: FSMContext):	
	text=''
	if message.text == 'ПІБ':
		await FSM.name.set()
		text = "Введіть свій ПІБ:"
	elif message.text == 'Вік':
		await FSM.age.set()
		text = "Введіть свій вік:"
	elif message.text == 'Навички':
		await FSM.skills.set()
		text ="Введіть свої навички:"
	elif message.text == 'Відміна':
		await FSM.fin.set()
		text = "Дію відмінено, тепер ти можеш завершити реєстрацію або обрати іншу дію!"
	elif message.text == 'Завершити реєстрацію':
		text = 'Ти не завершив поточну дію, натисни "Відміна" і тоді ти зможеш завершити реєстрацію'
	else:
		if message.text.isnumeric() and len(message.text) == 10:
			async with state.proxy() as data:
				data['phone'] = message.text
				await FSM.fin.set()
			text ="Виберіть наступний крок."
		else:
			text = "Номер має складатися з 10 цифр, без пробілів та без перших символів (+38), в форматі (1234567891)"
	await message.answer(text)


@dp.message_handler(Text(equals='Відміна', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
	text=''
	if await state.get_state() is None:
		return
	elif await state.get_state() == 'FSM:fin':
		text = "Зараз немає активної дії, ти можеш завершити реєстрацію або обрати дію."
	else: 
		text = "Дію відмінено, тепер ти можеш завершити реєстрацію або обрати іншу дію!"
		await FSM.fin.set()
	await message.reply(text)


@dp.message_handler(Text(equals='Завершити реєстрацію', ignore_case=True), state='*')
async def close_registration_action(message: types.Message, state: FSMContext):
	if await state.get_state() is None:
		return

	text = "Ваші дані які ви ввели:"
	async with state.proxy() as data:
		if data.get('name') is not None:
			text = text + "\nПІБ :" + str(data.get('name'))
		else:
			await message.reply("Ви не ввели ПІБ, будь ласка введіть ПІБ.")
			return

		if data.get('age') is not None:
			text = text + "\nВік :" + str(data.get('age'))
		else:
			await message.reply("Ви не ввели вік, будь ласка введіть вік.")
			return

		if data.get('skills') is not None:
			text = text + "\nНавички :" + str(data.get('skills'))
		else:
			await message.reply("Ви не ввели свої навички, будь ласка введіть навички.")
			return

		if data.get('phone') is not None:
			text = text + "\nНомер телефону :" + str(data.get('phone'))
		else:
			await message.reply("Ви не ввели свій номер телефону, будь ласка введіть номер телефону.")
			return

	if await save_to_txt(state) == True:
		text = text + "\nДані було збережено до файлу!"
	else: 
		text = text + "\nДані не було збережено до файлу, виникла помилка!"
	await state.finish()
	await message.reply(text = text, reply_markup = menu_keyboard())


@dp.message_handler()
async def echo(message: types.Message):
	await message.answer("Не зрозумів вашої команди. Перевірте правильність вводу")
