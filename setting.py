import yaml

SETTING_FILE_NAME = "setting.yml"

with open(SETTING_FILE_NAME) as file:
    setting = yaml.load(file)

def reload():
    global setting

    with open(SETTING_FILE_NAME) as file:
        setting = yaml.load(file)
