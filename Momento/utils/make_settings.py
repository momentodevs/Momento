import os

import jthon


class MakeSettings:
    def __init__(self, settings="settings"):
        settings += "bot_settings.json"
        if not os.path.isfile(settings):
            self.config = jthon.load(settings)
            self.prefix = ["m?"]
            self.description = None
            self.pm_help = False
            self.case_insensitive = False
            self.get_info()
            self.config.data = {
                "traceback": False,
                "Bot Settings": {
                    "command_prefix": self.prefix,
                    "coowners": [598625004279693460, 616582088845688843],
                    "description": self.description,
                    "pm_help": self.pm_help,
                    "case_insensitive": self.case_insensitive,
                },
            }
            self.config.save()

        self.config = jthon.load(settings)

    def get_info(self):
        prefix = input(
            "Please enter the prefix you would like to use. Separate multiple prefixes with a space. (default is !): "
        )
        if prefix:
            self.prefix = prefix.split(" ")
        description = input("Please enter you bots description (optional):  ")
        self.description = f"""{description}"""
        pm = input("Would you like the help menu to be sent in a PM? (y/n):")
        if pm.lower() in ["y", "yes"]:
            self.pm_help = True
        case_insensitive = input(
            "Would you like commands to be case insensitive? (y/n): "
        )
        if case_insensitive.lower() in ["y", "yes"]:
            self.case_insensitive = True
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def get_settings(self):
        return self.config