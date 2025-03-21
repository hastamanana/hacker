import random
import sys
import logging

from config import ATTEMPTS, WORDS, LENGTH_OF_PSWD


GARBAGE_CHARS: str = "~!@#$%^&*()_+-={}[]|;:,.<>?/"


def get_words_from_file(
        filename: str = "seven_letter_words.txt",
        encoding: str = "UTF-8"
) -> list[str]:
    logging.debug(LENGTH_OF_PSWD)
    try:
        with open(filename, mode="r", encoding=encoding) as file:
            return [
                curr_word.strip().upper()
                for curr_word in file.readlines()
            ]
    except FileNotFoundError:
        logging.error("Файл не найден!")
        sys.exit()


def get_secret_password(words: list[str]) -> str:
    """Возвращает загаданное слово."""
    return random.choice(words)


def fill_blocklist_words(all_words: list[str], blocklist_words: list[str]):
    """
    Добавляет случайные слова, чтобы получить 12 слов в общей сложности.
    """
    while len(blocklist_words) < WORDS:
        blocklist_words.append(get_one_word_except_blocklist(all_words, blocklist_words))


def find_similar_words(
        words_count: int,
        matches_count: int,
        secret_password: str,
        all_words: list[str],
        temp_words: list[str],
        blocklist_words: list[str],
        attempts: int = 500,
        **kwargs
) -> None:
    is_equal_mode: bool = kwargs.get("eq", False)

    for _ in range(attempts):
        if len(temp_words) == words_count:
            blocklist_words.extend(temp_words)
            temp_words.clear()
            break  # Нашли words_count слов, выходим из цикла.

        random_word: str = get_one_word_except_blocklist(
            all_words,
            temp_words,
            blocklist_words
        )

        count: int = get_num_matching_letters(secret_password, random_word)
        if is_equal_mode:
            if count == matches_count:
                temp_words.append(random_word)
        else:
            if count != matches_count:
                temp_words.append(random_word)


def get_password_words(all_words: list[str], length: int = 7) -> list[str]:
    """
    Возвращает список слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом.
    """
    secret_password: str = get_secret_password(all_words)
    blocklist_words: list[str] = [secret_password]
    temp_words: list[str] = []

    while len(temp_words) != 2:
        random_word: str = get_one_word_except_blocklist(
            all_words,
            temp_words,
            blocklist_words
        )
        if get_num_matching_letters(secret_password, random_word) == 0:
            temp_words.append(random_word)

    blocklist_words.extend(temp_words)
    temp_words.clear()

    find_similar_words(2, 3, secret_password, all_words, temp_words, blocklist_words, eq=True)
    find_similar_words(7, 0, secret_password, all_words, temp_words, blocklist_words)

    fill_blocklist_words(all_words, blocklist_words)

    return blocklist_words

# TODO: Продолжим здесь.

def get_one_word_except_blocklist(words: list[str], temp: list[str], blocklist: list[str]=None) -> str:
    """Возвращает случайное слово из WORDS, которого нет в blocklist."""
    if blocklist is None:
        blocklist = []

    while True:
        if (len(words) < len(blocklist)):
            return False
        random_word: str = random.choice(words)
        if random_word not in blocklist and random_word not in temp:
            return random_word


def get_num_matching_letters(word1: str, word2: str) -> int | None:
    """
    Возвращает количество совпадающих букв 
    в этих двух словах на одинковых позицих.
    """
    if len(word1) != len(word2):
        return None

    matches: int = 0

    for i in range(len(word1)):
        if word1[i] == word2[i]:
            matches += 1

    return matches


def return_computer_memory_str(words) -> str:
    """
    Возвращает строку, представляющую "память компьютера".
    """

    # Выбираем по одной строке на каждое слово. Всего 16 строк,
    # но они разделены на две половины.
    lines_with_words = random.sample(range(16 * 2), len(words))
    # Начальный адрес памяти (это тоже косметика).
    memory_address = 16 * random.randint(0, 4000)

    # Создаем строку "памяти компьютера".
    computer_memory = []  # Будет содержать 16 строк, по одной на каждую линию.
    next_word = 0  # Индекс слова в words, которое нужно вставить в строку.
    for line_num in range(16):  # "Память компьютера" имеет 16 строк.
        # Создаем половину строки из случайных символов:
        left_half = ''
        right_half = ''
        for j in range(16):  # Каждая половина строки содержит 16 символов.
            left_half += random.choice(GARBAGE_CHARS)
            right_half += random.choice(GARBAGE_CHARS)

        # Вставляем слово из списка words:
        if line_num in lines_with_words:
            # Находим случайное место в половине строки для вставки слова:
            insertion_index = min(16 - len(words[next_word]), random.randint(0, 9))
            # Вставляем слово:
            left_half = (left_half[:insertion_index] + words[next_word]
                        + left_half[insertion_index + 7:])
            next_word += 1  # Переходим к следующему слову.
        if line_num + 16 in lines_with_words:
            # Находим случайное место в половине строки для вставки слова:
            insertion_index = random.randint(0, 9)
            # Вставляем слово:
            right_half = (right_half[:insertion_index] + words[next_word]
                         + right_half[insertion_index + 7:])
            next_word += 1  # Переходим к следующему слову.

        computer_memory.append('0x' + hex(memory_address)[2:].zfill(4)
                              + '  ' + left_half + '    '
                              + '0x' + hex(memory_address + (16 * 16))[2:].zfill(4)
                              + '  ' + right_half)

        memory_address += 16  # Переход от, например, 0xe680 к 0xe690.

    # Каждая строка в списке computer_memory объединяется в одну большую строку:
    return '\n'.join(computer_memory)



def get_from_user_guess_pswd(words, tries) -> None:
    """
    Позволяет игроку ввести предположение пароля.
    """
    random_word_1, random_word_2 = random.sample(words, 2)


    print(f'\nВведите пароль: (осталось {tries} попыток)\n'
          'Для выхода из программы нажмите ctrl+c')
    guess: str = input('> ').upper()
    logging.info(f"Пользователь ввел слово {guess}")
    if guess not in words:
        raise ValueError('\nЭто не одно из возможных паролей, перечисленных выше.\n'
                         f'Попробуйте ввести "{random_word_1}" или "{random_word_2}".')
    else:
        return guess


def main() -> None:
    """
    Запуск одной игры "Взлом".
    """

    print(f"{"Мини-игра 'h@ck3r'":^60}\n")
    print('''Найдите пароль в памяти компьютера. Вам даются подсказки после
каждой попытки. Например, если секретный пароль – MONITOR, а игрок
угадал CONTAIN, ему будет дана подсказка, что 2 из 7 букв правильные,
потому что и MONITOR, и CONTAIN содержат буквы O и N на 2-й и 3-й позициях.\n
У вас есть четыре попытки.\n''')

    input('Нажмите Enter, чтобы начать...')

    if not get_words_from_file():
        return False
    all_words = get_words_from_file()
    words_for_game = get_password_words(all_words)
    secret_pswd = words_for_game[0]
    res = return_computer_memory_str(words_for_game)
    print(res)

    # я сделал через while, но как я могу сделать такую же логику через for и уменьшение попыток?
    attempt = ATTEMPTS
    while attempt > 0:
        try:
            player_serve = get_from_user_guess_pswd(words_for_game, attempt)
            if player_serve == secret_pswd:
                print('Д О С Т У П   Р А З Р Е Ш Е Н')
                logging.info(f"Пользователь взломал систему!")
                break
            else:
                num_mathes_words = get_num_matching_letters(secret_pswd, player_serve)
                print(f'Доступ запрещен ({num_mathes_words}/7 правильных)')
                logging.info(f"Пользователь ввел {num_mathes_words}/7 правильных")
                attempt -= 1
        except ValueError as e:
            print(e)
            continue
    else:
        print(f'Попытки закончились. Секретный пароль был {secret_pswd}.')
        logging.info(f"Пользователь не взломал систему!")



if __name__ == '__main__':
    logging.basicConfig(
        filename='game.log',
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        encoding="UTF-8"
    )
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()