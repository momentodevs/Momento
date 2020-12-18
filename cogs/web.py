from flask import Flask
from discord.ext import commands, menus, tasks

app = Flask(__name__)


class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app.route("/") 
    def home():
        return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)    

def setup(bot):
    bot.add_cog(Webserver(bot))

