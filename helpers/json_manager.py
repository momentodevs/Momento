import json


def add_user_to_blacklist(user_id: int) -> None:
    """
    This function will add a user based on its ID to the blacklist.json file
    :param user_id: The ID of the user to blacklist
    """
    with open("blacklist.json", "r+") as file:
        file_data = json.load(file)
        file_data['ids'].append(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)


def remove_user_from_blacklist(user_id: int) -> None:
    """
    This function will remove a user based on its ID from the blacklist.json file.
    :param user_id: The ID of the user that should be removed from the blacklist.json file.
    """
    with open("blacklist.json", "r") as file:
        file_data = json.load(file)
        file_data["ids"].remove(user_id)
    with open("blacklist.json", "w") as file:
        file.seek(0)
        json.dump(file_data, file, indent=4)
