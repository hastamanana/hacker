import json
import random

def read_config() -> dict:
    try:
        with open('config.json', 'r') as file:
            context: dict = dict(json.load(file))
    except (ModuleNotFoundError, json.JSONDecodeError):
        pass
    else:
        return context
    return {}

_configs = read_config()



ATTEMPTS: int = _configs.get("easy", {
        "attempts": 4},).get("attempts", 4)
WORDS: int = random.choice(_configs.get("easy", {
    "words": [5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]}).get("words", 12))
LENGTH_OF_PSWD: int = random.choice(_configs.get("easy", {"length_of_pswd": 7}).get("length_of_pswd", 7))


print(ATTEMPTS, WORDS, LENGTH_OF_PSWD)