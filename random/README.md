# Random approach

One prefix per Job definition. It is possible to scale up and down, but all the replicas will run independently. Failures are handled by retrying the Pods.

## Running

### Pre-requisites
1. A running Kubernetes cluster on which you can run applications.

### Build the image

You need to generate your own Docker image for the application. To do so, run in the same directory as `Dockerfile`:
```
# docker build . -t find-the-hash-random
```
Tag your image, filling your Dockerhub username:
```
# docker tag find-the-hash-random <username>/find-the-hash-random
```
Upload it:
```
# docker push <username>/find-the-hash-random
```

### Create the Job
Now open `finddahash.yaml` and change the Job definition accordingly. Take a look at the official documentation in order to understand all the fields and what they do.

The field `spec.template.spec.containers.command` describes the entrypoint of your application. As the main script takes two arguments, i.e. the prefix you are looking for and the maximum number of tries before failing, change it accordingly.

For instance, the line `command: ["python", "finddahash.py", "ababab", "1000000"]` will look for strings whose hash starts with 'ababab' and will fail if the program tries more than 1000000 times without success (yes, it uses brute force).

To create the Job, run:
```
kubectl create -f finddahash.yaml
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

### Failure

In case of failure, the task will be restarted depending on what you specify on the field `spec.template.spec.restartPolicy`. If the field is set to `OnFailure`, the Pod will be restarted in case of failure. If it's set to `Never`, a new Pod will be created in case of failure.
