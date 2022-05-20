import os.path
import re


async def save_to_txt(state) -> bool:
	async with state.proxy() as data:
		if 	os.path.exists('data/users.txt') == False:
			open(f"data/{data.get('user_id')}_anketa.txt", 'w', encoding='utf-8')
		with open(f"data/{data.get('user_id')}_anketa.txt", 'a', encoding='utf-8') as file:
			file.write(f"ПІБ : {data.get('name')}\n"
					   f"Вік : {data.get('age')}\n"
					   f"Навички : {data.get('skills')}\n"
					   f"Номер телефону : {data.get('phone')}\n")
		with open('data/users.txt','a', encoding='utf-8') as file:
			file.write(f"{data.get('user_id')} \n")
		return True

async def check_user(user_id:int) -> bool:
	if 	os.path.exists("data/users.txt") == False:
		open("data/users.txt",'w', encoding='utf-8')
	with open("data/users.txt",'r', encoding='utf-8') as f:
		lines = f.read().split()
	return True if str(user_id) in lines else False


async def see_file(user_id:str) -> str:
	if 	await check_user(user_id) == False:
		text = "Ти не заповнював анкету!"
	else:
		text = "Твоє резюме:\n"
		with open(f"data/{user_id}_anketa.txt", 'r', encoding='utf-8') as f:
			for line in f.readlines():
				text = text + line
			f.close()
	return text

async def delete_file(user_id:str) -> str:
	if 	await check_user(user_id) == False:
		text = "Ти не заповнював анкету!"
	else:
		text = "Твій файл видалено!\n"
		os.remove(f"data/{user_id}_anketa.txt")
		with open("data/users.txt") as f:
			lines = f.readlines()
		pattern = re.compile(re.escape(str(user_id)))
		with open("data/users.txt", 'w') as f:
			for line in lines:
				result = pattern.search(line)
				if result is None:
					f.write(line)

	return text