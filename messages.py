import symbols
import db_connection

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot

async def send_game_found(bot: Bot, player_chat_id, x_player_chat_id):
    ans = "Соперник найден. Вам выпал "
    if x_player_chat_id == player_chat_id:
        ans = ans + symbols.x_symbol
    else:
        ans = ans + symbols.o_symbol
    message = await bot.send_message(text=ans, chat_id=player_chat_id, reply_markup=getKeyboard(None))
    db_connection.set_player_message_id(player_chat_id, str(message.message_id))

async def send_game_is_over(bot: Bot, player_chat_id):
    await bot.send_message(text="Игра завершена. Начните новую игру.", chat_id=player_chat_id)

async def send_not_your_turn(bot: Bot, player_chat_id, state_with_turn):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Ход соперника!", chat_id=player_chat_id, message_id=message_id, reply_markup=getKeyboard(state_with_turn[1:]))

async def send_cell_is_occupied(bot: Bot, player_chat_id, state_with_turn):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Ячейка занята!", chat_id=player_chat_id, message_id=message_id, reply_markup=getKeyboard(state_with_turn[1:]))

async def send_win(bot: Bot, player_chat_id, state):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Вы победили!", chat_id=player_chat_id, message_id=message_id, reply_markup=getKeyboard(state))

async def send_lose(bot: Bot, player_chat_id, state):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Вы проиграли.", chat_id=player_chat_id, message_id=message_id, reply_markup=getKeyboard(state))

async def send_change_turn(bot: Bot, player_chat_id, enemy_chat_id, state):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Ход соперника.", chat_id= player_chat_id, message_id=message_id, reply_markup=getKeyboard(state))
    message_id = db_connection.get_player_message_id(enemy_chat_id)
    await bot.edit_message_text(text="Ваш ход.", chat_id=enemy_chat_id, message_id=message_id, reply_markup=getKeyboard(state))

async def send_enemy_searching(bot: Bot, player_chat_id):
    await bot.send_message(text="Поиск соперника", chat_id= player_chat_id)

async def send_draw(bot: Bot, player_chat_id, state):
    message_id = db_connection.get_player_message_id(player_chat_id)
    await bot.edit_message_text(text="Ничья!", chat_id=player_chat_id, message_id=message_id, reply_markup=getKeyboard(state))

def getKeyboard(state):
    keyboard = [[], [], []]

    # generate empty keyboard
    if state == None:
        state = ''
        for i in range(0, 9):
            state += symbols.empty_symbol

    for i in range(0, 3):
        for j in range(0, 3):
            keyboard[i].append(InlineKeyboardButton(text=state[i * 3 + j], callback_data=str(i * 3 + j) + state))

    return InlineKeyboardMarkup(inline_keyboard=keyboard)