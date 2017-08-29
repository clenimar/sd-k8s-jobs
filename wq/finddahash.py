#!/usr/bin/env python
from hashlib import sha256
from random import choice, randint
from string import ascii_letters
from string import digits
import sys

import rediswq


LETTERS = ascii_letters + digits
# TODO(clenimar): implement MAX_TRIES as an input parameter.
# How many unsuccessful tries before letting it go.
MAX_TRIES = 10000000
# How many seconds before unblocking an item and returning it to the DB.
LEASE_SECS = 30
# NOTE(clenimar): for some reason the Job pods cannot resolve the redis name.
# That's bit weird, but that's life. Hardcode it. (And fix it later, of course)
HOST = "10.35.252.5"


#FIXME(clenimar): implement this properly. No queue as an argument, dude.
def check_string(string, prefix, q):
    """Checks if the given string's hash starts with the given prefix."""
    h = sha256(string).hexdigest()
    if h.startswith(prefix):
        print("found! string: %s \nsha256sum: %s" % (string, h))
        q.publish_result("%s: %s" % (prefix, string))
        return True


def generate_string():
    """Generates a random string with size between 1 and 8."""
    return ''.join(choice(LETTERS) for _ in range(randint(1, 9)))


def find(prefix, q):
    print("looking for a hash whose prefix is %s" % prefix)
    tries = 0
    max_tries = MAX_TRIES
    while tries < max_tries:
        a = generate_string()
        tries += 1
        if check_string(a, prefix, q):
            print("success with %d tries" % tries)

            return True

    print("failing. get the next one...")
    q.check_expired_leases()

    return False


def run():
    q = rediswq.RedisWQ(name="job", host=HOST)
    print("Worker with sessionID: " + q.sessionID())
    print("Initial queue state: empty=" + str(q.empty()))
    while not q.empty():
        item = q.lease(lease_secs=LEASE_SECS, block=True, timeout=2)
        if item is not None:
            prefix = item.decode("utf=8")
            if find(prefix, q):
                q.complete(item)
        else:
            # TODO(clenimar): find a better way to regularly check expired
            # leases. Preferably in the Redis queue implementation itself.
            q.check_expired_leases()
            print("Waiting for work")
            continue

    print("Queue empty, exiting")


if __name__ == '__main__':
    run()
