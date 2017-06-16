from hashlib import sha256
from random import choice, randint
from string import ascii_lowercase
import sys

import rediswq


# NOTE(clenimar): although kube-dns setup is working fine, the name 'redis'
# doesn't resolve to the correct service address. use the hardcoded address
# until I figure out what's happening.
HOST = "10.35.250.81"


def work(prefix):
    """Done if there is one string whose SHA256 starts with `prefix`"""
    # create a new queue client
    q = rediswq.RedisWQ(name="hashfinder", host=HOST)
    print("worker with sessionID: " + q.sessionID())
    print("queue status: empty=" + str(q.empty()))

    # take one item from the queue. this item is supposed to be
    # an array of strings to be processed.
    bunch_of_strings = q.lease(lease_secs=10, block=True, timeout=2)
    if bunch_of_strings is not None:
        for item in bunch_of_strings:
            string = item.decode("utf-8")
            h = sha256(string).hexdigest()
            if h.startswith(prefix):
                print("string: %s with sha256sum %s" % (string, h))
                return True


if __name__ == '__main__':
    work(prefix=sys.argv[1])
