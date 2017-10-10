# Coarse parallel approach

Multiple prefixes per Job definition, supporting multiple workers at the same time (each work takes one item, processes it, and completes or fails). It is possible to scale up and down. Failures are handled by retrying the Pods, but the work items stored in RabbitMQ may be lost.

## Running

### Pre-requisites
1. A running Kubernetes cluster on which you can run applications.

### Build the image

You need to generate your own Docker image for the application. To do so, run in the same directory as `Dockerfile`:
```
# docker build . -t find-the-hash-coarse
```
Tag your image, filling your Dockerhub username:
```
# docker tag find-the-hash-coarse <username>/find-the-hash-coarse
```
Upload it:
```
# docker push <username>/find-the-hash-coarse
```

### Setup RabbitMQ

This approach uses RabbitMQ to store messages. You can use an existing intance of RabbitMQ as well as other message service, as long as you adapt the RabbitMQ-specific instructions for you setup.

In case you don't have a RabbitMQ instance, you can run it in Kubernetes as well. Configure it through the files `rabbitmq-controller.yaml` and `rabbitmq-service.yaml`, then run:

```
kubectl create -f rabbitmq-controller.yaml
kubectl create -f rabbitmq-service.yaml
```

### Fill your queue with work

You can use `amqp-tools` to add messages to the queue. Follow the steps described in [the official Kubernetes documentation](https://kubernetes.io/docs/tasks/job/coarse-parallel-processing-work-queue/#testing-the-message-queue-service).

### Create the Job
Now open `find-hash-coarse-job.yaml` and change the Job definition accordingly. Take a look at the official documentation in order to understand all the fields and what they do.

Once you create your Job, it will spin up instances that will look for messages store in a RabbitMQ. Please note that each worker will take one item from the queue, process it and then exit. If it fails in the process, other works won't be able to tackle this item. Once the queue is empty, the Job is done and the Pod completes.

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

### Failure

In case of failure, the task will be restarted depending on what you specify on the field `spec.template.spec.restartPolicy`. If the field is set to `OnFailure`, the Pod will be restarted in case of failure. If it's set to `Never`, a new Pod will be created in case of failure.
Note that if a worker fails after taking one item from the queue, this item will be lost. You should use this approach if your tasks are going to finish certainly.
