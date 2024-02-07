# CKAD

This repository contains the resources for the Certified Kubernetes Application Developer (CKAD) exam. 
I use it to prepare for the exam and to keep track of my progress.
It contains a sandbox environment to practice the exam tasks

# Lab environment 

## Prerequisites

- [x] k3d 

# 📚 Exercises

## 1️⃣ - Core concepts

### Create a basic pod

- [x] deploy a new cluster
- ```k3d cluster create --registry-create ckad-registry --agents 2 ckad```

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
- [x] 
```
    kubectl run nginx --image=nginx --restart=Never --env=var1=val1
    # then
    kubectl exec -it nginx -- env
    # or
    kubectl exec -it nginx -- sh -c 'echo $var1'
    # or
    kubectl describe po nginx | grep val1
    # or
    kubectl run nginx --restart=Never --image=nginx --env=var1=val1 -it --rm -- env
    # or
    kubectl run nginx --image nginx --restart=Never --env=var1=val1 -it --rm -- sh -c 'echo $var1' 
 ``` 

## 2️⃣  Multi container pods

create a multi-container pod with nginx and fluentd sidecar container

- [x] ```kubectl create -f lab/multi_container.yaml -n ckad```

Create a pod with an nginx container exposed on port 80. Add a busybox init container which downloads a page using "wget -O /work-dir/index.html http://neverssl.com/online". Make a volume of type emptyDir and mount it in both containers to share the downloaded `index.html` file. For the nginx container, mount it on "/usr/share/nginx/html" and for the initcontainer, mount it on "/work-dir". When done, get the IP of the created pod and create a busybox pod and run "wget -O- IP"

- [x] ```kubectl create -f lab/multi_container_init_container.yaml -n ckad```

then start port forwarding to access the nginx index page on http://localhost:8080 : `kubectl port-forward multi-container 8080:80`

## 3️⃣  Pod design

###  deployments

Create a deployment with image nginx:1.18.0, called nginx, having 2 replicas, defining port 80 as the port that this container exposes (don't create a service for this deployment)

- [x]
 ```
kubectl create deployment nginx  --image=nginx:1.18.0  --dry-run=client -o yaml > deploy.yaml
vi deploy.yaml
# change the replicas field from 1 to 2
# add this section to the container spec and save the deploy.yaml file
# ports:
#   - containerPort: 80
kubectl apply -f deploy.yaml
```

or 

```
kubectl create deploy nginx --image=nginx:1.18.0 --replicas=2 --port=80
```

get deploymet rollout status

- [x] ```kubectl rollout status deployment nginx```

view yaml of the replicaset for the deployment

- [x] ```kubectl get rs```

get the rollout history of the deployment

- [x] ```kubectl rollout history deployment nginx```

undo the last deployment and verify that the rollout history is updated

- [x] ```kubectl rollout undo deployment nginx```

### deployments strategies, rolling update and canary


Implement canary deployment by running two instances of nginx marked as version=v1 and version=v2 so that the load is balanced at 75%-25% ratio


crate a yaml for deployment with 3 replicas

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-v1
  labels:
    app: my-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
      version: v1
  template:
    metadata:
      labels:
        app: my-app
        version: v1
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: workdir
          mountPath: /usr/share/nginx/html
      initContainers:
      - name: install
        image: busybox:1.28
        command:
        - /bin/sh
        - -c
        - "echo version-1 > /work-dir/index.html"
        volumeMounts:
        - name: workdir
          mountPath: "/work-dir"
      volumes:
      - name: workdir
        emptyDir: {}
```

```bash
kubectl apply -f deployment.yaml
```

create a service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app-svc
  labels:
    app: my-app
spec:
  type: ClusterIP
  ports:
  - name: http
    port: 80
    targetPort: 80
  selector:
    app: my-app
```

test the deployment

```bash
# run a wget to the Service my-app-svc
kubectl run -it --rm --restart=Never busybox --image=gcr.io/google-containers/busybox --command -- wget -qO- my-app-svc

version-1
```
Deploy 1 replica of v2:


```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-v2
  labels:
    app: my-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
      version: v2
  template:
    metadata:
      labels:
        app: my-app
        version: v2
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
        volumeMounts:
        - name: workdir
          mountPath: /usr/share/nginx/html
      initContainers:
      - name: install
        image: busybox:1.28
        command:
        - /bin/sh
        - -c
        - "echo version-2 > /work-dir/index.html"
        volumeMounts:
        - name: workdir
          mountPath: "/work-dir"
      volumes:
      - name: workdir
        emptyDir: {}
```

Observe that calling the ip exposed by the service the requests are load balanced across the two versions:
```bash
# run a busyBox pod that will make a wget call to the service my-app-svc and print out the version of the pod it reached.
kubectl run -it --rm --restart=Never busybox --image=gcr.io/google-containers/busybox -- /bin/sh -c 'while sleep 1; do wget -qO- my-app-svc; done'

version-1
version-1
version-1
version-2
version-2
version-1
```
If the v2 is stable, scale it up to 4 replicas and shoutdown the v1:

```bash
kubectl scale --replicas=4 deploy my-app-v2
kubectl delete deploy my-app-v1
```

# update the labels
kubectl label deployment my-deployment-v1 app=my-app --overwrite

# update the selector
# 
kubectl label deployment my-deployment-v1 version=v1
```

### use helm to deploy packages
 
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

### Jobs

- [x] create a job that runs a container that sleeps for 3 second than exits

```kubectl create -f lab/simple_job.yaml -n ckad```

### Using labels

- [x] use the -l option to get pods with the label "tier=frontend"

```kubectl get pods -l tier=frontend```

- [x] edit the pod label to "tier=backend"

```kubectl edit pod simple-job-xxxx```

### setting resource limits

- [x] set the resource limits for the simpleapp deployment to 200m CPU and 100Mi memory

```YAML
    spec:
      containers:
      - name: simple-app
        image: ckad-registry:51223/simpleapp:latest
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 200m
            memory: 100Mi
```
- [x] get pod cpu and memory usage

```sh
kubectl top pod simpleapp-xxxx
```

### custom resource definitions

- [x] view CRDs currently in cluster

```sh
kubectl get crd
```

## 4️⃣ - Configuration

### Build an image from a Dockerfile and push it to a registry

Build a simple app and containerize it. Push it to a registry and deploy it to a cluster
- [x] create a simple app docker image `docker build -t simpleapp .`
- [x] make note of the k3d registry container port: `docker ps -f name=ckad-registry`
- [x] push the image to the registry:
- `docker tag simpleapp:latest localhost:<registry-port>/simpleapp:latest`
- `docker push localhost:<registry-port>/simpleapp:latest`
- [x] create a deployment for the app: `kubectl create -f lab/simpleapp.yaml -n ckad`

### authentication, authorization and admission control

TBD

### Security context

- [x] create a pod that runs as a user with UID 1000

```YAML
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```

### configmaps

- [x] create a configmap called "myconfig" with the key "mykey" and value "myvalue"

```
kubectl create configmap myconfig --from-literal=mykey=myvalue
```

- [x] Create and display a configmap from a file
```
#crate file
echo -e "key1=value1\nkey2=value2" > myconfig.txt
# create configmaps from file
kubectl create configmap myconfig --from-file=myconfig.txt
```

- [x] create a pod that uses the configmap as an environment variable

```YAML
spec:
    containers:
    - name: simple-app
        image: ckad-registry:51223/simpleapp:latest
        ports:
        - containerPort: 80
        env:
        - name: mycofnig
          valueFrom:
            configMapKeyRef:
              name: mycofnig
              key: mykey
 ```
 
 Create a configMap 'cmvolume' with values 'var8=val8', 'var9=val9'. Load this as a volume inside an nginx pod on path '/etc/lala'. Create the pod and 'ls' into the '/etc/lala' directory.
 
 - [x]
 
 ```
 kubectl create configmap cmvolume --from-literal=var8=val8 --from-literal=var9=val9
 kubectl run nginx --image=nginx --restart=Never -o yaml --dry-run=client > pod.yaml
 vim pod.yaml
```

```YAML
 apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  volumes: # add a volumes list
  - name: myvolume # just a name, you'll reference this in the pods
    configMap:
      name: cmvolume # name of your configmap
  containers:
  - image: nginx
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    volumeMounts: # your volume mounts are listed here
    - name: myvolume # the name that you specified in pod.spec.volumes.name
      mountPath: /etc/lala # the path inside your container
  dnsPolicy: ClusterFirst
  restartPolicy: Never
status: {}
```

```
kubectl create -f pod.yaml
kubectl exec -it nginx -- /bin/sh
cd /etc/lala
ls # will show var8 var9
cat var8 # will show val8
 ```
 
### Secrets

Create an nginx pod that mounts the secret my-secret in a volume on path /etc/foo
```sh

# create a secret
  kubectl create secret generic my-secret --from-literal=key1=supersecret --from-literal=key2=topsecret
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  securityContext:
    runAsUser: 1001
  containers:
  - image: nginx
    name: nginx
    ports:
    - containerPort: 80
    resources: {}
    volumeMounts:
    - name: my-secret
      mountPath: /etc/foo
  dnsPolicy: ClusterFirst
  restartPolicy: Never
  volumes:
  - name: my-secret
    secret:
      secretName: my-secret
status: {}
```

## 5️⃣ - Observability

### Configure liveness and readiness probes

- [x] alter the simpleapp deployment to add a readiness probe that checks for the /tmp/healthy file

```YAML
    spec:
      containers:
      - name: simple-app
        image: ckad-registry:51223/simpleapp:latest
        ports:
        - containerPort: 80
        readinessProbe:
          periodSeconds: 5
          exec:
            command:
              - cat
              - /tmp/healthy
```

- [x] alter the simpleapp deployment to add a liveness probe to know how long the pod stays healthy. The probe tests for port 8080 of the sidecar cotainer 
```YAML
    spec:
      containers:
      - name: simple-app
        image: ckad-registry:51223/simpleapp:latest
        ports:
        - containerPort: 80
        readinessProbe:
          periodSeconds: 5
          exec:
            command:
              - cat
              - /tmp/healthy
        livenessProbe:
          periodSeconds: 5
          exec:
            command:
              - cat
              - /tmp/healthy
```

### debugging

Create a busybox pod that runs 'ls /notexist'. Determine if there's an error (of course there is), see it. In the end, delete the pod

- [x] ```kubectl run busybox --image=busybox --restart=Never -- ls /notexist```

```
kubectl logs busybox
kubectl describe pod busybox
kubectl get events | grep -i error
```

## 6️⃣ - Services and networking

accessing an application with a service

`kubectl expose deployment/nginx --port=80 --type=NodePort`

create a pod with image nginx and expose it on port 80

`kubectl run nginx --image=nginx --restart=Never --port=80 --expose` // this creates a service as well

confirm that the clusterIP has been created, also check the endpoints

```YAML
kubectl get svc nginx # services
kubectl get ep # endpoints
```

Convert the ClusterIP to NodePort for the same service and find the NodePort port. Hit service using Node's IP. Delete the service and the pod at the end.

```
kubectl edit svc nginx
# change the type from ClusterIP to NodePort
```

Create a deployment called foo using image 'simpleapp' and 3 replicas. Label it as 'app=foo'. Declare that containers in this pod will accept traffic on port 8080 (do NOT create a service yet)

```
kubectl create deployment foo --image=ckad-registry:51223/simpleapp:latest --replicas=3 --port=8080
```

Create a service that exposes the deployment on port 6262. Verify its existence, check the endpoints

```
kubectl expose deployment foo --port=6262 --target-port=8080 --type=ClusterIP
```
Create an nginx deployment of 2 replicas, expose it via a ClusterIP service on port 80. Create a NetworkPolicy so that only pods with labels 'access: granted' can access the deployment and apply it


``` 
kubectl create deployment nginx --image=nginx --replicas=2
kubectl expose deployment nginx --port=80

kubectl describe svc nginx # see the 'app=nginx' selector for the pods
# or
kubectl get svc nginx -o yaml

vi policy.yaml
```

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: access-nginx # pick a name
spec:
  podSelector:
    matchLabels:
      app: nginx # selector for the pods
  ingress: # allow ingress traffic
  - from:
    - podSelector: # from pods
        matchLabels: # with this label
          access: granted
```

### Ingress rules

TBD


## 7️⃣ - State persistence

Create busybox pod with two containers, each one will have the image busybox and will run the 'sleep 3600' command. Make both containers mount an emptyDir at '/etc/foo'. Connect to the second busybox, write the first column of '/etc/passwd' file to '/etc/foo/passwd'. Connect to the first busybox and write '/etc/foo/passwd' file to standard output. Delete pod.

- [x] 
create template file for the pod
```kubectl run busybox --image=busybox --restart=Never -o yaml --dry-run=client -- /bin/sh -c 'sleep 3600' > pod.yaml ```

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  dnsPolicy: ClusterFirst
  restartPolicy: Never
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    imagePullPolicy: IfNotPresent
    name: busybox
    resources: {}
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    name: busybox2
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  volumes: #
  - name: myvolume #
    emptyDir: {} #
```yaml

Create a PersistentVolume of 10Gi, called 'myvolume'. Make it have accessMode of 'ReadWriteOnce' and 'ReadWriteMany', storageClassName 'normal', mounted on hostPath '/etc/foo'. Save it on pv.yaml, add it to the cluster. Show the PersistentVolumes that exist on the cluster

- [x] 
```YAML
kind: PersistentVolume
apiVersion: v1
metadata:
  name: myvolume
spec:
  storageClassName: normal
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
    - ReadWriteMany
  hostPath:
    path: /etc/foo
```
Create a busybox pod with command 'sleep 3600', save it on pod.yaml. Mount the PersistentVolumeClaim to '/etc/foo'. Connect to the 'busybox' pod, and copy the '/etc/passwd' file to '/etc/foo/passwd

- [x] 
  
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: mypvc
spec:
  storageClassName: normal
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5M
```  

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: busybox
  name: busybox
spec:
  containers:
  - args:
    - /bin/sh
    - -c
    - sleep 3600
    image: busybox
    imagePullPolicy: IfNotPresent
    name: busybox
    resources: {}
    volumeMounts: #
    - name: myvolume #
      mountPath: /etc/foo #
  dnsPolicy: ClusterFirst
  restartPolicy: Never
  volumes: #
  - name: myvolume #
    persistentVolumeClaim: #
      claimName: mypvc #
status: {}
```



## 8️⃣ - helm & custom resource definitions

