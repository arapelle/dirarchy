import random
import string


def random_string(char_set, min_len: int, max_len=None):
    s_len = min_len if max_len is None else random.randint(min_len, max_len)
    assert s_len >= 0
    return ''.join(random.choice(char_set) for i in range(s_len))


def random_digit_string(min_len: int, max_len=None):
    return random_string(string.digits, min_len, max_len)


def random_alpha_string(min_len: int, max_len=None):
    return random_string(string.ascii_letters, min_len, max_len)


def random_lower_string(min_len: int, max_len=None):
    return random_string(string.ascii_lowercase, min_len, max_len)


def random_upper_string(min_len: int, max_len=None):
    return random_string(string.ascii_uppercase, min_len, max_len)


def random_alnum_string(min_len: int, max_len=None):
    return random_string(string.ascii_letters + string.digits, min_len, max_len)


def random_sisy_string(consonants, vowels, codas, min_len: int, max_len=None):
    assert len(consonants) > 0
    assert len(vowels) > 0
    assert len(codas) > 0
    s_len = min_len if max_len is None else random.randint(min_len, max_len)
    assert s_len >= 0
    if s_len == 1:
        return random.choice(vowels)
    sisy_str = ''.join(random.choice(consonants) + random.choice(vowels) for i in range(s_len // 2))
    if s_len % 2 == 1:
        sisy_str += random.choice(codas)
    return sisy_str


def random_lower_sisy_string(min_len: int, max_len=None):
    return random_sisy_string("bdfgklmnprtvyz", "aeiou", "klrx", min_len, max_len)


def random_upper_sisy_string(min_len: int, max_len=None):
    return random_sisy_string("BDFGKLMNPRTVYZ", "AEIOU", "KLRX", min_len, max_len)


def random_snake_case_string(min_len: int, max_len=None):
    s_len = min_len if max_len is None else random.randint(min_len, max_len)
    assert s_len >= 0
    res_str = ""
    g_len = s_len
    while g_len > 1:
        sub_len = min(random.randint(2, 5), g_len)
        if random.randint(0, 5) < 3 or len(res_str) == 0:
            p_str = random_lower_sisy_string(sub_len)
            res_str += p_str
            g_len -= len(p_str)
        else:
            p_str = random_digit_string(sub_len)
            res_str += p_str
            g_len -= len(p_str)
        if g_len > 1:
            res_str += '_'
            g_len -= 1
    res_str += random_lower_sisy_string(s_len - len(res_str))
    assert len(res_str) == s_len
    return res_str


def random_format_cvqd_string(cvqd_str: str):
    res_str = ""
    for i in range(len(cvqd_str)):
        ch = cvqd_str[i]
        match ch:
            case 'c':
                res_str += random.choice("bdfgklmnprtvyz")
            case 'C':
                res_str += random.choice("BDFGKLMNPRTVYZ")
            case 'v':
                res_str += random.choice("aeiou")
            case 'V':
                res_str += random.choice("AEIOU")
            case 'q':
                res_str += random.choice("klrx")
            case 'Q':
                res_str += random.choice("KLRX")
            case 'd':
                res_str += random.choice(string.digits)
            case _:
                res_str += ch
    return res_str
