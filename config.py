import json
import random
from typing import Any


def read_config() -> dict:
    try:
        with open("config.json", "r") as file:
            context: dict = dict(json.load(file))
    except (ModuleNotFoundError, json.JSONDecodeError):
        return {}
    return context


CONFIG: dict[str, Any] = read_config()

GAME_MODE: str = CONFIG.get("mode", "easy")
ATTEMPTS: int = CONFIG.get(GAME_MODE, {}).get("attempts", 4)
WORDS: int = random.choice(CONFIG.get(GAME_MODE, {}).get(
    "words", [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
)

LENGTH_OF_PSWD: int = random.choice(
    CONFIG.get(GAME_MODE, {}).get("length_of_pswd", [7])
)

if __name__ == "__main__":
    print(ATTEMPTS, WORDS, LENGTH_OF_PSWD)
