# Fine parallel approach

Multiple prefixes per Job definition, supporting multiple workers at the same time (each worker keeps working until there is work to be done). It is possible to scale up and down. Failures are handled by pushing the failed items back to the work queue, making sure that if the Job completes, all the items were processed at least once.

## Running

### Pre-requisites
1. A running Kubernetes cluster on which you can run applications.

### Build the image

You need to generate your own Docker image for the application. To do so, run in the same directory as `Dockerfile`:
```
# docker build . -t find-the-hash-wq
```
Tag your image, filling your Dockerhub username:
```
# docker tag find-the-hash-wq <username>/find-the-hash-wq
```
Upload it:
```
# docker push <username>/find-the-hash-wq
```

### Setup redis
All the items to be processed are stored in a work queue stored in a redis database through a simple queue interface written in Python. If you don't have a running redis instace, you can set it up by running:

```
kubectl create -f redis-pod.yaml
kubectl create -f redis-service.yaml
```

Figure out the address on which redis is running by running `kubectl get services` and overwrite it on the file `finddahash.py`, on the variable `HOST`. This is a temporary workaround (see #1).

### Fill your queue with work

You can use an interactive Pod to fill redis with prefixes to be processed:

```
$ kubectl run -i --tty temp --image redis --command "/bin/sh"
Waiting for pod default/redis2-c7h78 to be running, status is Pending, pod ready: false
Hit enter for command prompt
```
Then:
```
# redis-cli -h redis
redis:6379> rpush job "0ce"
(integer) 1
redis:6379> rpush job "babaca"
(integer) 2
redis:6379> rpush job "00000"
(integer) 3
```
You can check what's on the queue by running:
```
redis:6379> lrange job 0 -1
1) "0ce"
2) "babaca"
3) "00000"
```

### Create the Job
Now open `find-hash-wq-job.yaml` and change the Job definition accordingly. Take a look at the official documentation in order to understand all the fields and what they do.

Once you create your Job, it will spin up Pods that will look for items stored in redis. Each worker will take one item from the `job` queue, move it to a temporary `job:processing` queue and try to complete it. If it fails or if it takes longer than expected (you can define a lease timeout in the code), the item will return to the main `job` queue, so other workers can take it. If the worker fails, it will try to take other item from the `job` queue. The Job completes when both queues, the main `job` queue and the temporary `job:processing` queue, are empty. The results are stored in a third queue, `job:results`.

To create the Job, run:
```
kubectl create -f find-hash-coarse-job.yaml
```

### Keep track of your Pods
You can keep track of your Pods by running:
```
kubectl get pods -a
```
Note that the Pods that complete the task successfully are shown as "Completed". You can see their outputs (i.e. the results) at any time by typing:
```
kubectl logs <pod-name>
```

As Pods are volatile, all the complete work is stored in the `job:results` queue. Check them by going into the interactive redis Pod and running:

```
# redis-cli -h redis
redis:6379> lrange job:results 0 -1
```
### Failure

In case of a failure where the Pods are deleted or restarted or evicted, the items those Pods were working on will be moved back to main queue after the defined lease timeout, so other workers can tackle them.

In case of a failure where the Pods reach the maximum number of tries (hello, brute force!), the Pod will give up and move the item back to the main queue, grabbing the next item in the queue.

This way we make sure that, if the Job completes, all the items were completed at least once.
