# TapiocaCafeManagement

MicroService for Tapioca Cafe App.
This microservice used for internal management of the cafe, such as meetings, storage management.

**Steps:**

```
docker build -t yf916/tapioca-cafe-management-service .
docker build --platform linux/amd64 -t yf916/tapioca-cafe-management-service .
docker image ls 
docker run -p 5001:5001 yf916/tapioca-cafe-management-service 
docker push yf916/tapioca-cafe-management-service

docker pull yf916/tapioca-cafe-management-service
docker ps
docker stop <container-id>
docker run -p 5001:5001 yf916/tapioca-cafe-management-service
http://ec2-13-58-188-11.us-east-2.compute.amazonaws.com:5001
```
