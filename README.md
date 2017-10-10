# sd-k8s-jobs

Showcase execution of workflows using Kubernetes' notion of Job.

### Task description
Return a string whose start matches the hexadecimal prefix given by the user. E.g. given "0ce", a possible output is "MzH", whose sha256 hash is "0ce8674fc7e61461e6a3def92c8237511e90506c7a3f38ec2b0a326f1ef362cd". This task is done here using three different approaches.

### Approaches
1. `coarse/`: all prefixes (items to be processed) are stored in a RabbitMQ queue. Does not handle failures along the way.
2. `random/`: each Job resource process only one prefix at a time. You can scale up and down, but each Pod will act independently. Handles failure by restarting the Pods until the task is completed.
3. `wq/`: store the prefixes (items to be processed) in a redis instance through a Python work queue interface that handles failures and makes sure that all the items are going to be processed at least once, even if the Pods fail.

Instructions on how to run each approach are described on their respective directories.

### Docs
This work in based on Kubernetes' official documentation on Jobs. Please refer to them in case of doubt.
