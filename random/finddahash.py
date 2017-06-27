from hashlib import sha256
from random import choice, randint
from string import ascii_lowercase
import sys


LETTERS = ascii_lowercase


def check_string(string, prefix):
    """Checks if the given string's hash starts with the given prefix."""
    h = sha256(string).hexdigest()
    if h.startswith(prefix):
        print("string: %s with sha256sum %s" % (string, h))
        return True


def generate_string():
    """Generates a random string with size between 0 and 10."""
    return ''.join(choice(LETTERS) for _ in range(randint(0, 10)))


def main(prefix):
    tries = 0
    max_tries = 1000000
    while True:
        if tries > max_tries: break
        a = generate_string()
        tries += 1
        if check_string(a, prefix):
            print("success with %d tries" % tries)
            return True
            
    # NOTE(clenimar): if we can't find what we're looking for, break.
    # This way we make sure that only an instance that completes the
    # work will finish.
    raise Exception("failed")


if __name__ == '__main__':
    main(prefix=sys.argv[1])
