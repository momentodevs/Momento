import psycopg2
from datetime import datetime
import atexit
import random


def connect_db():
    con = psycopg2.connect(host="",
                            database="", user="",
                            password="", port="")
    return con


conn = connect_db()
print(conn)


def create_users_table(conn):
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE users ( id varchar PRIMARY KEY, guild_id varchar, invites integer, xp integer, level integer, warns integer, mutes integer, messages_sent integer, join_date timestamp, songs_played integer);")
    cur.close()


def insert_test_user_data(conn):
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (id, guild_id, invites, xp, level, warns, mutes, messages_sent, join_date, songs_played) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (616582088845688843, 734397485346455572, 0, 0, 0, 0, 0, 0, "2021-4-22", 0))
    conn.commit()
    cur.close()


def disconnect_db(conn):
    conn.close()


def runCommand(*args):
    commandToRun = args[0]
    commands= ['userMessagesIncrement']
    for i in commands:
        if commandToRun == i:
            globals()[commandToRun](conn, args)


def userMessagesIncrement(conn, args):
    userId = args[1]
    guildId = args[2]
    cur = conn.cursor()
    cur.execute("INSERT INTO users (id, guild_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (str(userId), str(guildId)))
    conn.commit()
    cur.close()
    cur = conn.cursor()
    cur.execute("UPDATE users SET messages_sent = messages_sent + 1 WHERE (id = %s::varchar AND guild_id = %s::varchar);", (userId, guildId))
    conn.commit()
    cur.close()


def getLevels(conn, args):
    userId = args[1]
    guild_id= args[2]
    cur = conn.cursor()


atexit.register(disconnect_db, conn=conn)
