import logging

# Setup Orator logging
logger = logging.getLogger("orator.connection.queries")
logger.setLevel(logging.DEBUG)

# Settings for printing to console
formatter = logging.Formatter(
    "It took %(elapsed_time)sms to execute the query %(query)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Settings for adding to the discord log file
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="a")
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s: %(query)s - %(elapsed_time)ss"
)
handler.setFormatter(formatter)
logger.addHandler(handler)