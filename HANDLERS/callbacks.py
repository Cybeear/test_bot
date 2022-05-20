from aiogram import types


from dispatcher import dp, bot
import Datapacks


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('fao_btn'))
async def fao_callback_button(callback_query: types.CallbackQuery):
	code = callback_query.data[-1]
	if code.isdigit():
		code = int(code)
		await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, text = Datapacks.fao_answer[code+1])


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('work_btn'))
async def work_callback_button(callback_query: types.CallbackQuery):
	code = callback_query.data[-1]
	if code.isdigit():
		code = int(code)
		await bot.answer_callback_query(callback_query.id)
	await bot.send_message(callback_query.from_user.id, text = Datapacks.vacancies[code+1])