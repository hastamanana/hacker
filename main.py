import random 
import sys
import logging

from config import ATTEMPTS, WORDS, LENGTH_OF_PSWD


GARBAGE_CHARS: str = '~!@#$%^&*()_+-={}[]|;:,.<>?/'


def get_words_from_txt_file(filename='seven_letter_words.txt') -> list[str]:
    print(LENGTH_OF_PSWD)
    try:
        with open(filename) as words_list_file:
            if LENGTH_OF_PSWD != 7:
                return [curr_word.strip().upper() for curr_word in words_list_file.readlines() if len(curr_word.strip()) == LENGTH_OF_PSWD + 1]
            return [curr_word.strip().upper() for curr_word in words_list_file.readlines() if len(curr_word.strip()) == LENGTH_OF_PSWD]
    except FileNotFoundError:
        logging.error("Файл не найден!")
        sys.exit()
    

def get_secret_pswd(words) -> str:
    """
    Возвращает загаданное слово
    """
    return random.choice(words)

def get_twelve_words(words_from_file) -> list[str]:
    """
    Возвращает список из 12 слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом.
    """
    
    secret_password: str = get_secret_pswd(words_from_file)
    words:list[str] = [secret_password]
    temp_words: list[str] = []

    # Находим еще два слова; они не имеют совпадающих букв.
    while len(temp_words) != 2:
        random_word: str = get_one_word_except_blocklist(words_from_file, temp_words, words)
        if get_num_matching_letters(secret_password, random_word) == 0:
            temp_words.append(random_word)

    words.extend(temp_words)
    temp_words.clear()

    # Находим два слова, которые имеют 3 совпадающие буквы
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(temp_words) == 2:
            words.extend(temp_words)
            temp_words.clear()
            break  # Нашли 5 слов, выходим из цикла.

        random_word: str = get_one_word_except_blocklist(words_from_file, temp_words, words)
        if get_num_matching_letters(secret_password, random_word) == 3:
            temp_words.append(random_word)

    # Находим хотя бы семь слов, которые имеют хотя бы одну совпадающую букву
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(temp_words) == 7:
            words.extend(temp_words)
            temp_words.clear()
            break  # Нашли 7 или более слов, выходим из цикла.

        random_word: str = get_one_word_except_blocklist(words_from_file, temp_words, words)
        if get_num_matching_letters(secret_password, random_word) != 0:
            temp_words.append(random_word)

    # Добавляем случайные слова, чтобы получить 12 слов в общей сложности.
    while len(words) < WORDS:
        random_word: str = get_one_word_except_blocklist(words_from_file, words)
        words.append(random_word)

    return words


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


def get_num_matching_letters(word1: str, word2: str) -> int:
    """
    Возвращает количество совпадающих букв 
    в этих двух словах на одинковых позицих.
    """
    matches: int = 0
    
    if len(word1) != len(word2):
        return
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

    if not get_words_from_txt_file():
        return False
    all_words = get_words_from_txt_file()
    words_for_game = get_twelve_words(all_words)
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