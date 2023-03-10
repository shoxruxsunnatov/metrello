import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from trello import TrelloManager

load_dotenv()

conn = psycopg2.connect(
    dbname=os.environ.get('dbname'),
    user=os.environ.get('user'),
    password=os.environ.get('password'),
    host=os.environ.get('host'),
    port=os.environ.get('port')
)

cursor = conn.cursor()


def check_chat_id_from_database(chat_id):
    with conn.cursor() as cur:
        cur.execute(f"SELECT chat_id FROM users WHERE chat_id::TEXT LIKE '{chat_id}%'")
        chat_id_in_database = cur.fetchall()
        return chat_id_in_database


def write_trello_to_database(username, bot_chat_id, full_name):
    members = TrelloManager(username).get_member()
    trello_boards = TrelloManager(username).get_boards()

    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO members(fullname, trello_username, member_trello_id)"
            f" VALUES ('{members.get('fullName')}', '{username}', '{members.get('id')}')"
            f"ON CONFLICT (member_trello_id) DO UPDATE SET fullname=excluded.fullname,"
            f"trello_username=excluded.trello_username, member_trello_id=excluded.member_trello_id")

        cur.execute(f"SELECT id FROM members WHERE member_trello_id='{members.get('id')}'")
        member_id = cur.fetchall()[0][0]

        cur.execute(f"INSERT INTO users(chat_id, fullname, username, member_id)"
                    f"VALUES ('{bot_chat_id}', '{full_name}', '{username}', '{member_id}')"
                    f"ON CONFLICT (chat_id) DO UPDATE SET chat_id=excluded.chat_id, fullname=excluded.fullname,"
                    f"username=excluded.username, member_id=excluded.member_id")

        for i in range(len(trello_boards)):
            cur.execute(f"INSERT INTO boards(name, board_trello_id)"
                        f"VALUES ('{trello_boards[i].get('name')}', '{trello_boards[i].get('id')}')"
                        f"ON CONFLICT (board_trello_id) DO UPDATE SET name=excluded.name,"
                        f" board_trello_id=excluded.board_trello_id")

            lists = TrelloManager(username).get_lists_on_a_board(trello_boards[i].get('id'))
            labels = TrelloManager(username).get_labels_board(trello_boards[i].get('id'))

            for j in range(len(lists)):
                cur.execute(f"SELECT id FROM boards WHERE board_trello_id='{trello_boards[i].get('id')}'")
                board_id = cur.fetchall()[0][0]
                cur.execute(f"INSERT INTO lists(name, list_trello_id, board_id)"
                            f"VALUES ('{lists[j].get('name')}', '{lists[j].get('id')}', '{board_id}')"
                            f"ON CONFLICT (list_trello_id) DO UPDATE SET name=excluded.name,"
                            f"list_trello_id=excluded.list_trello_id, board_id=excluded.board_id")

                cur.execute(f"SELECT id FROM lists WHERE list_trello_id='{lists[j].get('id')}'")
                list_id = cur.fetchall()[0][0]

                cards = TrelloManager(username).get_cards_on_a_list(lists[j].get('id'))

                for k in range(len(cards)):
                    cur.execute(f"INSERT INTO cards(name, card_trello_id, url, description, lists_id)"
                                f"VALUES ('{cards[k].get('name')}', '{cards[k].get('id')}', '{cards[k].get('url')}',"
                                f"'{cards[k].get('desc')}','{list_id}')"
                                f"ON CONFLICT (card_trello_id) DO UPDATE SET name=excluded.name,"
                                f"card_trello_id=excluded.card_trello_id, description=excluded.description,"
                                f"lists_id=excluded.lists_id")

                    cur.execute(f"SELECT id FROM cards WHERE card_trello_id='{cards[k].get('id')}'")
                    card_id = cur.fetchall()[0][0]

                    cur.execute(f"INSERT INTO cards_members(card_id, member_id) VALUES  ('{card_id}','{member_id}')"
                                f"ON CONFLICT (card_id, member_id) DO UPDATE SET card_id=excluded.card_id,"
                                f"member_id=excluded.member_id")

            for n in range(len(labels)):
                if labels[n].get('name'):
                    cur.execute(
                        f"INSERT INTO labels(name,label_trello_id,board_id)"
                        f"VALUES  ('{labels[n].get('name')}', '{labels[n].get('id')}', '{board_id}')"
                        f"ON CONFLICT (label_trello_id) DO UPDATE SET name=excluded.name,"
                        f"label_trello_id=excluded.label_trello_id, board_id=excluded.board_id")

                    cur.execute(f"SELECT id FROM labels WHERE label_trello_id='{labels[n].get('id')}'")
                    label_id = cur.fetchall()[0][0]

                    cur.execute(
                        f"INSERT INTO cards_labels(card_id, labels_id) VALUES  ('{card_id}', '{label_id}')"
                        f"ON CONFLICT (card_id, labels_id) DO UPDATE SET card_id=excluded.card_id,"
                        f"labels_id=excluded.labels_id")

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id FROM boards")
        board_id = cur.fetchall()

        for i in range(len(board_id)):
            cur.execute(f"INSERT INTO board_members(board_id, member_id)"
                        f"VALUES ('{board_id[i].get('id')}', '{member_id}')"
                        f"ON CONFLICT (board_id) DO UPDATE SET board_id=excluded.board_id,"
                        f"member_id=excluded.member_id")

        conn.commit()


def get_boards():

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT name, id FROM boards")
        return cur.fetchall()


def get_lists(board_id):

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT name, id FROM lists WHERE board_id={board_id}")
        return cur.fetchall()


def get_cards(list_id):

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT name, id, url FROM cards WHERE lists_id={list_id}")
        return cur.fetchall()


def check_size(board_id):

    return len(
        get_lists(board_id)
    )


def update_database(bot_chat_id, full_name):

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(f"SELECT username FROM users WHERE chat_id={bot_chat_id}")
        username = cur.fetchall()[0].get("username")

    write_trello_to_database(username, bot_chat_id, full_name)

    return "Malumotlar qayta yuklandi. /boards"

