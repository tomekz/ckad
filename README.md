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

create a busybox pod that runs the command "env"
- [x] ```kubectl run busybox --image=busybox --restart=Never  -n ckad --command -- env```

Get the YAML for a new namespace called 'myns' without creating it
- [x] ```kubectl create namespace ckad -o yaml --dry-run=client```

Create an nginx pod and set an env value as 'var1=val1'. Check the env value existence within the pod
- [x] ```kubectl run nginx --image=nginx --restart=Never --env=var1=val1
    # then
    kubectl exec -it nginx -- env
    # or
    kubectl exec -it nginx -- sh -c 'echo $var1'
    # or
    kubectl describe po nginx | grep val1
    # or
    kubectl run nginx --restart=Never --image=nginx --env=var1=val1 -it --rm -- env
    # or
    kubectl run nginx --image nginx --restart=Never --env=var1=val1 -it --rm -- sh -c 'echo $var1' ``` 

### Multi container pods

create a multi-container pod with nginx and fluentd sidecar container

- [x] ```kubectl create -f lab/multi_container.yaml -n ckad```

Create a pod with an nginx container exposed on port 80. Add a busybox init container which downloads a page using "wget -O /work-dir/index.html http://neverssl.com/online". Make a volume of type emptyDir and mount it in both containers to share the downloaded `index.html` file. For the nginx container, mount it on "/usr/share/nginx/html" and for the initcontainer, mount it on "/work-dir". When done, get the IP of the created pod and create a busybox pod and run "wget -O- IP"

- [x] ```kubectl create -f lab/multi_container_init_container.yaml -n ckad```

then start port forwarding to access the nginx index page on http://localhost:8080 : `kubectl port-forward multi-container 8080:80`

### Labels and annotations

create a pod nginx with the labels "tier=frontend" and "app=v1"

- [x] ```kubectl run nginx --image=nginx --labels=app=v1,tier=frontend```

to get the labels of the pod:

- [x] ```kubectl get pod nginx --show-labels```

get only pods with the label "tier=frontend"

- [x] ```kubectl get pod -l tier=frontend```

add annotation "description='my description'" to the pod

- [x] ```kubectl annotate pod nginx description='my description'```

### Pod placement

Create a pod that will be deployed to a Node that has the label 'tier=frontend'

Add the label to a node:

```bash
kubectl label nodes <your-node-name> tier=frontend
kubectl get nodes --show-labels
```

We can use the 'nodeSelector' property on the Pod YAML:

```YAML
apiVersion: v1
kind: Pod
metadata:
  name: cuda-test
spec:
  containers:
    - name: cuda-test
      image: "k8s.gcr.io/cuda-vector-add:v0.1"
  nodeSelector: # add this
    tier:frontend # the selection label
```


## 2️⃣ - Build

- [ ] task 3
