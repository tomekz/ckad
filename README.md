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
- ```kubectl create -f basic.yaml ```
describe the pod
- ```kubectl describe pod basic ```

## 2️⃣ - Lists

- [ ] task 3