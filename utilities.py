from random import randint, choice
from string import ascii_letters, ascii_lowercase, digits, punctuation


def generate_random_string(size=10,
                           lower=False,
                           digit=True,
                           punc=False,
                           original=None):
    # random string contains letters and digits if digit is True

    chars = ascii_lowercase if lower is True else ascii_letters
    if digit is True:
        chars += digits
    if punc is True:
        chars += punctuation

    new_string = ''.join(choice(chars) for i in range(size))

    if original is not None and new_string == original:
        return generate_random_string(size,
                                      digit,
                                      punc,
                                      original)
    else:
        return new_string


def generate_random_email(original):

    email = f'{generate_random_string(size=randint(0, 20), lower=True, digit=False)}@' \
            f'{generate_random_string(size=randint(0, 20), lower=True, digit=False)}.' \
            f'{generate_random_string(size=3, lower=True, digit=False)}'

    if email != original:
        return email
    else:
        return generate_random_email(original)


def generate_two_numbers(max_value):

    value1 = randint(1, max_value)
    value2 = randint(1, max_value)
    if value1 != value2:
        return value1, value2
    else:
        return generate_two_numbers(max_value)



