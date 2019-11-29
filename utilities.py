from random import randint, choice
from string import ascii_letters, digits


def generate_random_string(size=10,
                           digit=True,
                           original=None):
    # random string contains letters and digits if digit is True

    letters_and_digits = ascii_letters + digits if digit is True else ascii_letters
    new_string = ''.join(choice(letters_and_digits) for i in range(size))

    if original is not None and new_string == original:
        return generate_random_string(size,
                                      digit,
                                      original)
    else:
        return new_string


def generate_random_email(original):

    email = f'{generate_random_string(size=randint(0, 50))}@' \
            f'{generate_random_string(size=randint(0, 40))}.' \
            f'{generate_random_string(size=3, digit=False)}'

    if email != original:
        return email
    else:
        return generate_random_email(original)

