# Momento

Momento is an opensource discord bot filled with features

## Installation

Use Git clone to install momento:
```
git clone https://github.com/momentodevs/Momento.git

python3 -m pip install -r requirements.txt
```
## Database
With Momento you have the choice of 3 different databases to store data. You can use sqlite (file storage), MySQL (most known database) and also PostGresQL (a no SQL database thats a lot easier to understand). We recommend PostGresQL for its speed and reliability.
## Config
config.yml

```yaml
discord:
    TOKEN:

databases:
    default: sqlite
    sqlite:
      driver: sqlite
      database: Momento\database\discord.db
      log_queries: True
      prefix:
    mysql:
      driver: mysql
      host: 
      database: 
      port:
      user: 
      password: 
      log_queries:
    postgres:
      driver: postgres
      host:
      database:
      port:
      user:
      password:
      log_queries:
  
config:
  utils:
    bot_logging: True
    bot_settings: True
    bot_utils: True
  logging_mode: 'w'
```

## Usage

```python
python3 run.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

![Discord Banner](https://discordapp.com/api/guilds/734397485346455572/widget.png?style=banner4)
[JOIN](https://discord.gg/xrqSPATnBb)
