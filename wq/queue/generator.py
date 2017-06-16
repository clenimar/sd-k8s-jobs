from hashlib import sha256
from random import choice, randint
from string import ascii_lowercase
import sys


LETTERS = ascii_lowercase

# TODO: fill the redis queue with these strings.
def generate_string_bucket(bucket_size=4096, string_size=16):
    """Generate a bucket of random strings."""
    return [''.join(choice(LETTERS) for _ in range(randint(0, string_size))) for _ in range(bucket_size)]


def main():
    print(generate_string_bucket())


if __name__ == '__main__':
    main()
