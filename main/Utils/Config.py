# Eventually this will be initialized from a YAML file at import time (which won't affect code which uses the
# get_option() functions)
str_dictionary = {
    "MAX_CONNECTIONS_PER_HOST": 10000
}


# Get a value from the dictionary as a string
def get_str_option(key):
    str(str_dictionary[key])
