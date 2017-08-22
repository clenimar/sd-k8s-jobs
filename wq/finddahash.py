from hashlib import sha256
from random import choice, randint
from string import ascii_lowercase
import sys

import rediswq


# NOTE(clenimar): although kube-dns setup is working fine, the name 'redis'
# doesn't resolve to the correct service address. use the hardcoded address
# until I figure out what's happening.
HOST = "10.35.249.236"

def run(prefix):
    q = rediswq.RedisWQ(name="job-hash", host=HOST)
    print("Worker with sessionID: " +  q.sessionID())
    print("Initial queue state: empty=" + str(q.empty()))
    while not q.empty():
        # NOTE(clenimar): this is far from ideal, but here's the deal:
        # take a lot of strings in a bucket, then process them.
        bucket = []
        bucket_size = 10000000
        for _ in range(bucket_size):
            i = q.lease(lease_secs=1, block=False, timeout=2)
            if item is not None:
                bucket.append(i)
                q.complete(i)
            else:
                # if we have a None item, the queue should be empty. get out.
                break

        # process it!
        print("let's find it out! bucket size: %d" % len(bucket))
        if finddahash(prefix, bucket):
            return True


def finddahash(prefix, bucket):
    """Done if there is one string whose SHA256 starts with `prefix`"""

    if bucket is None: raise Exception('no bucket, no sucess')
    if not bucket: raise Exception('empty bucket, no sucess')

    for i in bucket:
        item = i.decode("utf-8")
        h = sha256(item).hexdigest()
        if h.startswith(prefix):
            print ("found! string %s with sha256 %s" % (string, h))
            return True

    # if we run out of strings in our bucket, go get more strings!
    return False


if __name__ == '__main__':
    run(prefix=sys.argv[1])
