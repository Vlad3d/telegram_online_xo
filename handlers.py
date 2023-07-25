import game
import symbols

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет. Для начала игры нажми в 'Меню' пункт 'Начать игру'")

@router.message(Command("endgame"))
async def end_handler(msg: Message, bot: Bot):
    player_chat_id = str(msg.chat.id)
    empty_state = ''
    for i in range(0, 9):
        empty_state += symbols.empty_symbol
    await game.end_game(bot, player_chat_id, empty_state, False)

@router.message(Command("startgame"))
async def start_handler(msg: Message, bot: Bot):
    player_chat_id = str(msg.chat.id)
    await game.start_game(bot, player_chat_id)

@router.callback_query()
async def callback_handler(query: CallbackQuery, bot: Bot):
    # check that game is not over
    player_chat_id = str(query.message.chat.id)
    if not await game.is_running(bot, player_chat_id):
        return

    state_with_turn = query.data
    await game.make_turn(bot, player_chat_id, state_with_turn)
    await query.answer()