# Телеграм бот, для игры в крестики-нолики в режиме игрок против игрока.

`/start` - Начало работы с ботом (выводит приветственное сообщение);

`/startgame` - Начать игру. Эта команда начинает поиск соперника для игры и, после нахождения, стартует игру.

`/endgame` - Завершить игру. Эта команда завершает текущую игру, либо прекращает поиск игры.

# Как всё работает.
Бот использует базу данных (sqlite), в которой есть 3 таблицы:

`status` - текущий статус игрока. Содержит одно поле name в котором хранятся следующие значения: PLAYING - пользователь находится в игре, SEARCHING - пользователь ищет игру, NOTHING - пользователь бездействует.

`user` - описание игрока. Содержит два поля: chat_id - id чата с игроком; status - содержит статус из таблицы status

`game` - описание игры. Содержит поля: id - первичный ключ; player_one_chat_id - id чата с первым игроком; player_two_chat_id - id чата со вторым игроком; player_turn_chat_id - id чата игрока, который сейчас ходит; x_player_chat_id - id чата игроа, который ходит крестиком; player_one_message_id - id сообщения с игрой первого игрока; player_two_message_id - id сообщения с игрой второго игрока

Пользователям отправляется поле 3 x 3 из кнопок, каждая кнопка - ячейка для хода.
При каждом ходе сообщение с кнопками редактируется (чтобы игра шла в одном сообщении и не создавалась куча игровых полей).

Каждая кнопка передает текущее состояние и ход. Состояние и ход хранятся списком из 10 элементов: {ход}{девять состояний ячеек}, т.е. состояние выглядит так:
`6◻❌◻⭕◻◻◻◻❌`
где 6 это ячейка куда был сделан ход, а `◻❌◻⭕◻◻◻◻❌` соответствует:
```
◻❌◻
⭕◻◻
◻◻❌
```
В боте реализованы проверки на случаи, если игрок пытается сходить в занятую клетку или сделать второй ход подряд.

# Установка и настройка:
Сначала необходимо создать бота и получить его токен. 
Для этого нужно написать боту @BotFather команду /newbot . После чего заполнить все необходимые данные (имя бота и т.д.)
После заполнения всех данных @BotFather пришлет сообщение, в котором будет содержаться токен. Этот токен необходимо поместить в config.py (поле BOT_TOKEN)

Для запуска бота необходимо, чтобы был установлен python 3, и библиотеки из файла requirements.txt
