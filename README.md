# CKAD

This repository contains the resources for the Certified Kubernetes Application Developer (CKAD) exam. 
I use it to prepare for the exam and to keep track of my progress.
It contains a sandbox environment to practice the exam tasks

# Lab environment 

## Prerequisites

- [x] k3d 

# 📚 Exercises

## 1️⃣ - Core [concepts](concepts)

### Create a basic pod

- [x] deploy a new cluster
- ```k3d cluster create --agents 2 ckad ```

- [x] create a basic pod

create a pod with the name "basic" [and](and) the image "nginx"
- [x] ```kubectl create namespace ckad```

- [x] ```kubectl create -f lab/basic.yaml -n ckad```

or without yaml file:

- [x] ```kubectl run basic --image=nginx --restart=Never --port=80 -n ckad```

describe the pod
- [x] ```kubectl describe pod basic ```

Change pod's image to nginx:1.7.1. Observe that the container will be restarted as soon as the image gets pulled
- [x] ```kubectl set image pod/basic basic=nginx:1.7.1```

enable port forwarding to access the pod. Listen on port 8080 on the host and forward to port 80 in the pod
- [x] ```kubectl port-forward basic 8080:80 ```

shutdown the pod:
- [x] ```kubectl delete pod basic```

create new service for the pod
- [x] ```[kubectl](kubectl) create -f lab/basic_svc.yaml -n ckad```

- [x] create a busybox pod that runs the command "env"
- ```kubectl run busybox --image=busybox --restart=Never  -n ckad --command -- env```

- Get the YAML for a new namespace called 'myns' without creating it
- [x] ```kubectl create namespace ckad -o yaml --dry-run=client```

### Multi container pods

create a multi-container pod with nginx and fluentd sidecar container

- [x] ```kubectl create -f lab/multi_container.yaml -n ckad```

### Create a deployment


## 2️⃣ - Lists

- [ ] task 3
