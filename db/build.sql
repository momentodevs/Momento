CREATE TABLE IF NOT EXISTS guilds(
    GuildID integer PRIMARY KEY,
    Prefix varchar DEFAULT 'm?',
    LogChannel varchar,
    MutedRole varchar,
    LevelMessages varchar DEFAULT 'no',
    twitchChannels varchar
);

CREATE TABLE IF NOT EXISTS "mutes" (
	UserID integer primary key,
 	GuildID integer,
 	RoleIDs	varchar
);

CREATE TABLE IF NOT EXISTS users(
    id varchar primary key,
    guildId varchar not null,
    invites integer default 0,
    xp integer default 0,
    level integer default 0,
    xplock varchar,
    warns integer default 0,
    mutes integer default 0,
    messages_sent integer default 0,
    join_date varchar default CURRENT_TIMESTAMP,
    songs_played integer default 0
);
