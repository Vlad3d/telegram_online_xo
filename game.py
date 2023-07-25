import random
import messages
import symbols
import db_connection

from aiogram import Bot

async def start_game(bot: Bot, player_chat_id):
    # end previous game if player leave
    db_connection.end_game_db(player_chat_id)
    enemy_chat_id = db_connection.find_enemy_db(player_chat_id)
    if enemy_chat_id != None:
        db_connection.set_playing_status_db(player_chat_id)
        db_connection.set_playing_status_db(enemy_chat_id)
        x_player_chat_id = who_is_first(player_chat_id, enemy_chat_id)
        db_connection.start_game_db(player_chat_id, enemy_chat_id, x_player_chat_id)
        await messages.send_game_found(bot, player_chat_id, x_player_chat_id)
        await messages.send_game_found(bot, enemy_chat_id, x_player_chat_id)
    else:
        db_connection.set_searching_status_db(player_chat_id)
        await messages.send_enemy_searching(bot, player_chat_id)

async def is_running(bot: Bot, player_chat_id):
    if not db_connection.is_running_db(player_chat_id):
        await messages.send_game_is_over(bot, player_chat_id)
        return False
    return True

async def make_turn(bot: Bot, player_chat_id, state_with_turn):
    whose_turn_chat_id = db_connection.whose_turn_db(player_chat_id)
    enemy_chat_id = db_connection.get_enemy_chat_id_db(player_chat_id)
    if whose_turn_chat_id != player_chat_id:
        await messages.send_not_your_turn(bot, player_chat_id, state_with_turn)
        return
    
    x_player_chat_id = db_connection.x_player_chat_id_db(player_chat_id)
    symbol = symbols.o_symbol
    if x_player_chat_id == player_chat_id:
        symbol = symbols.x_symbol
    updated_state = try_to_make_move(state_with_turn, symbol)
    if updated_state == None:
        await messages.send_cell_is_occupied(bot, player_chat_id, state_with_turn)
        return

    if check_win(updated_state):
        await end_game(bot, player_chat_id, updated_state, True)
        return
    if check_draw(updated_state):
        await messages.send_draw(bot, player_chat_id, updated_state)
        await messages.send_draw(bot, enemy_chat_id, updated_state)
        await end_game(bot, player_chat_id, updated_state, False)
        return
    db_connection.change_turn_db(enemy_chat_id)
    await messages.send_change_turn(bot, player_chat_id, enemy_chat_id, updated_state)

async def end_game(bot: Bot, player_chat_id, updated_state, win):
    enemy_chat_id = db_connection.get_enemy_chat_id_db(player_chat_id)
    db_connection.set_noting_status_db(player_chat_id)
    if enemy_chat_id != None:
        db_connection.set_noting_status_db(enemy_chat_id)
    if win:
        await messages.send_win(bot, player_chat_id, updated_state)
        await messages.send_lose(bot, enemy_chat_id, updated_state)
    db_connection.end_game_db(player_chat_id)
    await messages.send_game_is_over(bot, player_chat_id)
    if enemy_chat_id != None:
        await messages.send_game_is_over(bot, enemy_chat_id)

def who_is_first(player_one_chat_id, player_two_chat_id):
    list = [player_one_chat_id, player_two_chat_id]
    return list[random.randint(0, 1)]

def try_to_make_move(state_with_turn, x_o_symbol):
    turn_pos = int(state_with_turn[0])
    updated_state = list(state_with_turn)
    updated_state.pop(0)
    if updated_state[turn_pos] == symbols.empty_symbol:
        updated_state[turn_pos] = x_o_symbol
    else:
        return None
    return "".join(str(e) for e in updated_state)

def check_win(state):
  if ((state[0] == state[1] and state[1] == state[2] and state[0] != symbols.empty_symbol)
    or (state[3] == state[4] and state[4] == state[5] and state[3] != symbols.empty_symbol)
    or (state[6] == state[7] and state[7] == state[8] and state[6] != symbols.empty_symbol)
    or (state[0] == state[3] and state[3] == state[6] and state[0] != symbols.empty_symbol)
    or (state[1] == state[4] and state[4] == state[7] and state[1] != symbols.empty_symbol)
    or (state[2] == state[5] and state[5] == state[8] and state[2] != symbols.empty_symbol)
    or (state[0] == state[4] and state[4] == state[8] and state[0] != symbols.empty_symbol)
    or (state[2] == state[4] and state[4] == state[6] and state[2] != symbols.empty_symbol)):
    return True
  else:
    return False

def check_draw(state):
    for i in range(0, 9):
        if state[i] == symbols.empty_symbol:
            return False
    return True
