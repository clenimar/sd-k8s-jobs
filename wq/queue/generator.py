from hashlib import sha256
from random import choice, randint
from string import ascii_letters, digits
import sys

import rediswq

# consider lowercase, uppercase and digits
LETTERS = ascii_letters + digits
# NOTE(clenimar): although kube-dns setup is working fine, the name 'redis'
# doesn't resolve to the correct service address. use the hardcoded address
# until I figure out what's happening.
HOST = "10.35.249.236"


def run():
    q = rediswq.RedisWQ(name="job-hash", host=HOST)
    print("Worker with sessionID: " +  q.sessionID())
    print("Initial queue state: empty=" + str(q.empty()))

    # put a lot of strings in the queue.
    n = 100000
    # no, seriously, a lot.
    n = 10000000
    # dude...
    n = 3000000000

    i = 0
    while i < n:
        i += 1
        q.push(generate_random_string())

    print("job done! %d strings inserted!" % n)


def generate_random_string(max_string_size=8):
    """Generate a random strings."""
    return ''.join(choice(LETTERS) for _ in range(randint(1, max_string_size)))


if __name__ == '__main__':
    run()
