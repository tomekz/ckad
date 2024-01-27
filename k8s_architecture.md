---
id: k8s_architecture
aliases:
  - k8s architecture
  - intro
tags: []
---

[[k8s]]


## intro

- `k8s` builds on 15 years of experience at Google in project Borg. 
- **scaling**: instead of one big monolithic system, `k8s` approaches the problem by breaking it down into a set of independent microservices.
- most legacy applications are not designed to run in a distributed environment and most likely will have to be re-architected to run on `k8s`.

![[Pasted image 20240109101443.png]]

## components

1. **pods**
A Pod consists of one or more containers which share an IP address, access to storage and namespace. Typically, one container in a Pod runs an application, while other containers support the primary application

2. **operators aka controllers**
Orchestration is managed through a series of watch-loops, also known as operators or controllers. Each operator interrogates the kube-apiserver for a particular object state, modifying the object until the declared state matches the current state. Example of an operator:
- deployment
- replica set 
- job
- cron job
3. control plane (kubernetes master)
    - kube-apiserver
    - kube-scheduler
    - etcd database
4 worker nodes
    - kubelet
    - kube-proxy
    - container runtime (docker, containerd, cri-o, etc)
