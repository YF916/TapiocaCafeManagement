# TapiocaCafeManagement

MicroService for Tapioca Cafe App.
This microservice used for internal management of the cafe, such as meetings, storage management.

**Steps:**

```
docker build -t yf916/tapioca-cafe-management-service .
docker image ls 
docker run -p 5001:5001 yf916/tapioca-cafe-management-service 
docker push yf916/tapioca-cafe-management-service
```