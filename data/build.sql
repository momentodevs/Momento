CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix text DEFAULT "."
);

CREATE TABLE IF NOT EXISTS users(
    GuildID integer,
    UserID integer,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    Coins integer default 0,
    Stars integer default 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY("GuildID", "UserID")
)
