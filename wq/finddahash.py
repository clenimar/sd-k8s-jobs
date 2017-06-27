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
    work = rediswq.RedisWQ(name="work", host=HOST)
    print("main queue status: empty=" + str(work.empty()))

    if work.empty():
        return

    # Redis is a simple key-value storage, so we're using a main queue
    # to store the name of the queues that actually have real items to work on.
    q_name = work.lease(lease_secs=60, block=True, timeout=2)
    q = rediswq.RedisWQ(name=q_name.decode("utf-8"), host=HOST)
    print("worker queue with sessionID: " + q.sessionID())
    print("worker queue status: empty=" + str(q.empty()))


    # now process all the items in the queue. if success, return.
    while not q.empty():
        item = q.lease(lease_secs=10, block=True, timeout=2)
        if item is not None:
            string = item.decode("utf-8")
            print(string)
            h = sha256(string).hexdigest()
            q.complete(item)

            if h.startswith(prefix):
                print("string: %s with sha256sum %s" % (string, h))
                return True

    # NOTE(clenimar): if we can't find what we're looking for, break.
    # This way we make sure that only an instance that completes the
    # work will finish.
    raise Exception("job not completed.")


if __name__ == '__main__':
    work(prefix=sys.argv[1])
