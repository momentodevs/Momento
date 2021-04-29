from orator import DatabaseManager, Model

from .. import bot_instance

# Setup the Model reference for Orator
Model.set_connection_resolver(bot_instance.db)