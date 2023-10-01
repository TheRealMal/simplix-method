# -*- coding: utf-8 -*-
import telebot
from simplix import Simplix
from bot_token import bot_token

bot = telebot.TeleBot(bot_token, parse_mode="html")

@bot.message_handler(commands=['start'])
def send_start(message) -> None:
    example = "0 -1 1 0 0 0\n1 -2 1 0 0 2\n2 -1 0 -1 0 2\n1 1 0 0 1 5"
    bot.send_message(message.chat.id, "В первой строке F, в остальных строках A\nПример:\n<pre>{}</pre>".format(example))

@bot.message_handler()
def solve_simplix(message) -> None:
    msg = message.text.splitlines()
    F = [int(_) for _ in msg[0].split()]
    A = [[int(__) for __ in msg[_].split()] for _ in range(1, len(msg))]
    output = []
    data = Simplix(
        F=F,
        A=A
    )
    data.print(output)
    data.solve(output)
    if data.iterations == 100:
        bot.send_message(message.chat.id, "<pre>Бесконечный цикл</pre>")
    else:
        bot.send_message(message.chat.id, "<pre>" + "".join(output) + "</pre>")

bot.infinity_polling()