import random
import re
import random_string


def random_int(params: str):
    rmatch = re.fullmatch(r'\s*([-+]?\d+)s*,\s*([-+]?\d+)\s*', params)
    if not rmatch:
        raise Exception(f"Bad rand int parameters: {params}. Two integers are expected: min, max.")
    min_value = int(rmatch.group(1))
    max_value = int(rmatch.group(2))
    return str(random.randint(min_value, max_value))


def random_float(params: str):
    rmatch = re.fullmatch(r'\s*([-+]?\d+(\.\d*)?)s*,\s*([-+]?\d+(\.\d*))\s*', params)
    if not rmatch:
        raise Exception(f"Bad rand int parameters: {params}. Two integers are expected: min, max.")
    min_value = float(rmatch.group(1))
    max_value = float(rmatch.group(3))
    return f"{random.uniform(min_value, max_value):.3f}"


def random_var_value(var_rand_value: str):
    rmatch = re.fullmatch(r"(int|float|digit|alpha|lower|upper|alnum|snake_case|"
                          r"lower_sisy|upper_sisy|format_cvqd|'([ -~]+)'),\s*([!-~][ -~]*[!-~])\s*", var_rand_value)
    if not rmatch:
        raise Exception(f"Bad rand value: '{var_rand_value}'.")

    rand_category = rmatch.group(1)
    match rand_category:
        case 'int':
            return random_int(rmatch.group(3))
        case 'float':
            return random_float(rmatch.group(3))

    rand_params = rmatch.group(3)
    if rand_category == 'format_cvqd':
        p_match = re.fullmatch(r"\s*'([^abefghijklmnoprstuwxyzABEFGHIJKLMNOPRSTUWXYZ]+)'\s*",
                               rand_params)
        if not p_match:
            raise Exception(f"String to format_cvqd is not a valid string: '{rand_params}'.")
        return random_string.random_format_cvqd_string(p_match.group(1))

    char_set = rmatch.group(2)
    min_len, max_len = [int(x) for x in rand_params.split(',')]
    match rand_category:
        case 'digit':
            return random_string.random_digit_string(min_len, max_len)
        case 'alpha':
            return random_string.random_alpha_string(min_len, max_len)
        case 'lower':
            return random_string.random_lower_string(min_len, max_len)
        case 'upper':
            return random_string.random_upper_string(min_len, max_len)
        case 'alnum':
            return random_string.random_alnum_string(min_len, max_len)
        case 'lower_sisy':
            return random_string.random_lower_sisy_string(min_len, max_len)
        case 'upper_sisy':
            return random_string.random_upper_sisy_string(min_len, max_len)
        case 'snake_case':
            return random_string.random_snake_case_string(min_len, max_len)
        case _:
            return random_string.random_string(char_set, min_len, max_len)
