# TapiocaCafeManagement

MicroService for Tapioca Cafe App.
This microservice used for internal management of the cafe, such as meetings, storage management.

**Steps:**

Build and Run Docker
```
docker build -t tapioca-cafe-management-service .
docker run -d -p 8080:80 tapioca-cafe-management-service
```
Test Microservice Locally
```
curl http://localhost:8080
```
Push the Docker Image to Docker Hub
```
docker tag tapioca-cafe-management-service yf916/tapioca-cafe-management-service:v1
docker push yf916/tapioca-cafe-management-service:v1
```