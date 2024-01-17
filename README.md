# CKAD

This repository contains the resources for the Certified Kubernetes Application Developer (CKAD) exam. 
I use it to prepare for the exam and to keep track of my progress.
It contains a sandbox environment to practice the exam tasks

# Lab environment 

## Prerequisites

- [x] k3d 

# 📚 Exercises

## 1️⃣ - Core concepts

- [x] deploy a new cluster
- ```k3d cluster create --agents 2 ckad ```

- [x] create a basic pod

create a pod with the name "basic" and the image "nginx"
- ```kubectl create namespace ckad```

- ```kubectl create -f lab/basic.yaml -n ckad```

or without yaml file:

- ```kubectl run basic --image=nginx --restart=Never -n ckad```

describe the pod
- ```kubectl describe pod basic ```

enable port forwarding to access the pod. Listen on port 8080 on the host and forward to port 80 in the pod
- ```kubectl port-forward basic 8080:80 ```

shutdown the pod:
- ```kubectl delete pod basic```

- [x] create a busybox pod that runs the command "env"

- ```kubectl run busybox --image=busybox --restart=Never  -n ckad --command -- env```

## 2️⃣ - Lists

- [ ] task 3
