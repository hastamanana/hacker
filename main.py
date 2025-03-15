import random 
import sys


GARBAGE_CHARS: str = '~!@#$%^&*()_+-={}[]|;:,.<>?/'


def get_words_from_txt_file() -> list[str]:
    with open('seven_letter_words.txt') as words_list_file:
        WORDS: list[str] = [i.strip().upper() for i in words_list_file.readlines()]
        return WORDS
    
WORDS = get_words_from_txt_file()
    


def get_twelve_words(words_from_file) -> list[str]:
    """
    Возвращает список из 12 слов, которые могут быть паролем.

    Секретный пароль будет первым словом в списке.
    Чтобы игра была честной, мы стараемся включить слова с разным
    количеством совпадающих букв с секретным словом.
    """
    
    secret_password: str = random.choice(words_from_file)
    words:list[str] = [secret_password]

    # Находим еще два слова; они не имеют совпадающих букв.
    # Используем "< 3", потому что секретный пароль уже в списке.
    while len(words) < 3:
        randow_word: str = get_one_word_except_blocklist(words)
        if return_num_matching_letters(secret_password, randow_word) == 0:
            words.append(randow_word)

    # Находим два слова, которые имеют 3 совпадающие буквы
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 5:
            break  # Нашли 5 слов, выходим из цикла.

        randow_word: str = get_one_word_except_blocklist(words)
        if return_num_matching_letters(secret_password, randow_word) == 3:
            words.append(randow_word)

    # Находим хотя бы семь слов, которые имеют хотя бы одну совпадающую букву
    # (но сдаемся после 500 попыток, если не можем найти достаточно).
    for i in range(500):
        if len(words) == 12:
            break  # Нашли 7 или более слов, выходим из цикла.

        randow_word: str = get_one_word_except_blocklist(words)
        if return_num_matching_letters(secret_password, randow_word) != 0:
            words.append(randow_word)

    # Добавляем случайные слова, чтобы получить 12 слов в общей сложности.
    while len(words) < 12:
        randow_word: str = get_one_word_except_blocklist(words)
        words.append(randow_word)

    assert len(words) == 12
    return words


def get_one_word_except_blocklist(blocklist=None) -> str: 
    """Возвращает случайное слово из WORDS, которого нет в blocklist."""
    if blocklist == None:
        blocklist = []

    while True:
        random_word: str = random.choice(WORDS)
        if random_word not in blocklist:
            return random_word



def return_num_matching_letters(word1, word2) -> int:
    """
    Возвращает количество совпадающих букв в этих двух словах.
    """
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
            insertion_index = random.randint(0, 9)
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
    """Позволяет игроку ввести предположение пароля."""
    while True:
        print(f'\nВведите пароль: (осталось {tries} попыток)')
        guess: str = input('> ').upper()
        if guess in words:
            return guess
        print('Это не одно из возможных паролей, перечисленных выше.')
        print(f'Попробуйте ввести "{words[0]}" или "{words[1]}".')




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

    all_words = get_words_from_txt_file()
    words_for_game = get_twelve_words(all_words)
    secret_pswd = random.choice(words_for_game) 
    res = return_computer_memory_str(words_for_game)
    print(res)

    for user_tries in range(4, 0, -1):
        player_serve = get_from_user_guess_pswd(words_for_game, user_tries)
        if player_serve == secret_pswd:
            print('Д О С Т У П   Р А З Р Е Ш Е Н')
            return
        else:
            num_mathes_words = return_num_matching_letters(secret_pswd, player_serve)
            print(f'Доступ запрещен ({num_mathes_words}/7 правильных)')
    print(f'Попытки закончились. Секретный пароль был {secret_pswd}.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()