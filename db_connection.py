import sqlite3;
 
con = sqlite3.connect("base.db")

def init_db():
    query = """CREATE TABLE IF NOT EXISTS status (name TEXT PRIMARY KEY)"""
    con.execute(query)
    query = """INSERT OR IGNORE INTO status VALUES("SEARCHING");
                INSERT OR IGNORE INTO status VALUES("PLAYING");
                INSERT OR IGNORE INTO status VALUES("NOTHING");"""
    con.executescript(query)
    query = """CREATE TABLE IF NOT EXISTS user 
                (chat_id TEXT PRIMARY KEY, 
                status TEXT NOT NULL, 
                FOREIGN KEY (status) REFERENCES status (name) ON DELETE CASCADE ON UPDATE CASCADE);"""
    con.execute(query)
    query = """CREATE TABLE IF NOT EXISTS game
                (id INTEGER PRIMARY KEY,
                player_one_chat_id TEXT NOT NULL,
                player_two_chat_id TEXT NOT NULL,
                player_turn_chat_id TEXT NOT NULL,
                x_player_chat_id TEXT NOT NULL,
                player_one_message_id TEXT NOT NULL,
                player_two_message_id TEXT NOT NULL,
                FOREIGN KEY (player_one_chat_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (player_two_chat_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (player_turn_chat_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (x_player_chat_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (player_one_message_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (player_two_message_id) REFERENCES user (chat_id) ON DELETE CASCADE ON UPDATE CASCADE);"""
    con.execute(query)

def find_enemy_db(player_chat_id):
    cursor = con.cursor()
    query = """SELECT chat_id FROM user 
                WHERE status = 'SEARCHING' and chat_id != ? LIMIT 1"""
    cursor.execute(query, (player_chat_id, ))
    enemy_chat_id = cursor.fetchone()
    if enemy_chat_id != None:
        return enemy_chat_id[0]
    return None

def start_game_db(player_one_chat_id, player_two_chat_id, player_turn_chat_id):
    cursor = con.cursor()
    query = """INSERT INTO game (player_one_chat_id, player_two_chat_id, player_turn_chat_id, x_player_chat_id) 
                VALUES (?, ?, ?, ?)"""
    cursor.execute(query, (player_one_chat_id, player_two_chat_id, player_turn_chat_id, player_turn_chat_id))
    con.commit()

def end_game_db(player_chat_id):
    cursor = con.cursor()
    query = """DELETE FROM game WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    con.commit()

def set_searching_status_db(player_chat_id):
    cursor = con.cursor()
    query = """INSERT INTO user (chat_id, status) 
                VALUES (?, 'SEARCHING') 
                ON CONFLICT (chat_id) DO UPDATE SET status='SEARCHING'"""
    cursor.execute(query, (player_chat_id, ))
    con.commit()

def set_playing_status_db(player_chat_id):
    cursor = con.cursor()
    query = """INSERT INTO user (chat_id, status) 
                VALUES (?, 'PLAYING') ON CONFLICT (chat_id) DO UPDATE SET status='PLAYING'"""
    cursor.execute(query, (player_chat_id, ))
    con.commit()

def set_noting_status_db(player_chat_id):
    cursor = con.cursor()
    query = """INSERT INTO user (chat_id, status) 
                VALUES (?, 'NOTHING') 
                ON CONFLICT (chat_id) DO UPDATE SET status='NOTHING'"""
    cursor.execute(query, (player_chat_id, ))
    con.commit()


def whose_turn_db(player_chat_id):
    cursor = con.cursor()
    query = """SELECT player_turn_chat_id 
                FROM game 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    player_turn_ans = cursor.fetchone()
    if player_turn_ans != None:
        return player_turn_ans[0]
    return None

def x_player_chat_id_db(player_chat_id):
    cursor = con.cursor()
    query = """SELECT x_player_chat_id 
                FROM game 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    x_player_ans = cursor.fetchone()
    if x_player_ans != None:
        return x_player_ans[0]
    return None

def get_enemy_chat_id_db(player_chat_id):
    cursor = con.cursor()
    query = """SELECT player_one_chat_id, player_two_chat_id 
                FROM game 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    ans = cursor.fetchone()
    if ans == None:
        return None
    if player_chat_id == ans[0]:
        return ans[1]
    else:
        return ans[0]
    
def change_turn_db(player_turn_id):
    cursor = con.cursor()
    query = """UPDATE game 
                SET player_turn_chat_id = ? 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_turn_id, player_turn_id, player_turn_id))
    con.commit()

def is_running_db(player_chat_id):
    cursor = con.cursor()
    query = """SELECT * 
                FROM game 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    res = cursor.fetchone()
    if res == None or len(res) == 0:
        return False
    return True

def set_player_message_id(player_chat_id, message_id):
    cursor = con.cursor()
    query = """UPDATE game 
                SET player_one_message_id = ? 
                WHERE player_one_chat_id = ?"""
    cursor.execute(query, (message_id, player_chat_id))
    con.commit()
    cursor = con.cursor()
    query = """UPDATE game 
                SET player_two_message_id = ? 
                WHERE player_two_chat_id = ?"""
    cursor.execute(query, (message_id, player_chat_id))
    con.commit()

def get_player_message_id(player_chat_id):
    cursor = con.cursor()
    query = """SELECT * 
                FROM game 
                WHERE player_one_chat_id = ? OR player_two_chat_id = ?"""
    cursor.execute(query, (player_chat_id, player_chat_id))
    res = cursor.fetchone()
    if res == None:
        return None
    if res[1] == player_chat_id:
        return res[5]
    elif res[2] == player_chat_id:
        return res[6]
    return None