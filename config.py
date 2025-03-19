import json
import random

def read_config() -> dict:
    try:
        with open('config.json', 'r') as file:
            context: dict = dict(json.load(file))
    except ModuleNotFoundError:
        pass
    else:
        return context
    return {}

_configs = read_config()

ATTEMPTS: int = _configs.get("medium").get("attempts", 4)
WORDS: int = random.choice(_configs.get("medium").get("words", 12))
LENGTH_OF_PSWD: int = _configs.get("medium").get("length_of_pswd", 7)

print(ATTEMPTS)
print(WORDS)
print(LENGTH_OF_PSWD)