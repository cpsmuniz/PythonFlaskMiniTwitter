import re


# Validates user_name with regex #
def validate_username(user_name):
    regex = "^[a-zA-Z0-9]{1,14}$"
    return re.match(regex, user_name)

