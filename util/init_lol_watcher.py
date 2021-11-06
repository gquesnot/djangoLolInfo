import json

from riotwatcher import LolWatcher


def initLolWatcher():
    with open('config.json') as f:
        config = json.load(f)
    print(config)
    return LolWatcher(config['apiKey'])