from __future__ import print_function
import yaml

# Get a value from the dictionary as a string
def get_str_option(selected_key):
    
    # Initialize config option function attribute
    try:
        get_str_option.config_options is None
    except AttributeError:
        get_str_option.config_options = {}
        with open('tool_configuration.yaml', 'r') as myfile:
            data = myfile.read()
            # Credit: https://stackoverflow.com/questions/13019653/converting-yaml-file-to-python-dict
            for key, value in yaml.load(data)['settings'].iteritems():
                get_str_option.config_options[key] = value

    return str(get_str_option.config_options[selected_key])
