class UserBlacklisted(Exception):
    """
    Thrown when a user is attempting to do something, but is blacklisted
    """

    def __init__(self, message="User is Blacklisted!"):
        self.message=message
        super().__init__(self.message)


class UserNotOwner(Exception):
    """
    Thrown when a user is attempting to do something, but is not an owner of the bot
    """

    def __init__(self, message="User is not an owner of the bot!"):
        self.message=message
        super().__init__(self.message)
