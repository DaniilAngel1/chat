from pywebio import start_server, config
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js
import asyncio
from datetime import datetime
from style import css

chat_msgs = []
online_users = set()

MAX_MESSAGES_COUNT = 100



@config(css_style=css)
async def main():
	global chat_msgs

	put_markdown("### 🌉 Добро пожаловать в 共通 (перев. яп. \"общий\")!\n💎Создатель: Песчаный Гаара (Гаара), DaniilAngel или ник дракон, по вопросам обращайтесь к нему, если он не в чате, то пишите ему в соц. сетях ([телега (чаще всего он там находится)](https://t.me/DaniilAngel) или [в вк](https://vk.com/daniil_kokko))!")

	msg_box = output()
	put_scrollable(msg_box, heigth=300, keep_bottom=True)

	niсkname = await input("🏧Войти в чат", required=True, placeholder="🗣Ваше имя", validate=lambda n: "⚠️Такой ник уже используется!" if n in online_users or n == '🔊' else None)
	online_users.add(niсkname)

	chat_msgs.append(('📣', f"`{niсkname}` присодинился к чату!"))
	msg_box.append(put_markdown('📣', f"`{niсkname}` присодинился к чату!"))

	refresh_task = run_async(refresh_msg(niсkname, msg_box))

	while True:
		data = await input_group("📥 Новое сообщение", [
			input(placeholder="📝Текст сообщения", name="msg"),
			actions(name="cmd", buttons=["📤Отправить", {'label':"📴Выйти из чата", 'type':"cancel"}])
			], validate=lambda m: ('msg', "✏️Введите текст сообщения!") if m["cmd"] == "📤Отправить" and not m["msg"] else None)

		if data is None:
			break

		msg_box.append(put_markdown(f"`{niсkname}`: {data['msg']}"))
		chat_msgs.append((niсkname, data['msg']))

	refresh_task.close()

	online_users.remove(niсkname)
	toast("Вы вышли из чата!")
	msg_box.append(put_markdown(f"📴 Пользователь `{niсkname}` покинул чат!"))
	chat_msgs.append(('📴', f" Пользователь `{niсkname}` покинул чат!"))

	put_buttons(["🌀Перезайди"], onclick=lambda btn: run_js('window.location.reload()'))

async def refresh_msg(niсkname, msg_box):
	global chat_msgs
	last_idx = len(chat_msgs)

	while True:
		await asyncio.sleep(1)

		for m in chat_msgs[last_idx:]:
			if m[0] != niсkname:
				msg_box.append(put_markdown(f"`{m[0]}`: {m[1]}"))

				if len(chat_msgs) > MAX_MESSAGES_COUNT:
					chat_msgs = chat_msgs[len(chat_msgs) // 2:]

				last_idx = len(chat_msgs)

if __name__ == "__main__":
	start_server(main, debug=True, port=8080, cdn=True)