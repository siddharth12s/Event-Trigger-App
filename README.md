# Segwise Backend Assessment

## Installation and Setup Guide

- Installing Docker and it's repositories

```sh
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg


echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt install docker.io
sudo apt install docker-compose
```

- Verify installation

```sh
docker --version
```

- Managing Docker as NON-ROOT User

```sh
sudo usermod -aG docker $USER

newgrp docker
```


- Enable and start docker
```sh
sudo systemctl enable docker
sudo systemctl start docker
```


## Cloning Repo of APP

```sh
git clone https://github.com/siddharth12s/segwise.git
```

- Change directory to segwise (Project folder)

```sh
cd segwise
```

## Create Configs.py (Environment variables file)

```sh
sudo nano configs.py
```

- COPY-PASTE the following database CONFIG in the FILE

```python3
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "segwise_db_2",
        "USER": "segwise_user",
        "PASSWORD": "password",
        "HOST": "postgres",  # Docker Image
        # "HOST": "127.0.0.1", # For local
        "PORT": "5432",
    }
}
SECRET_KEY = "7fc27e0d108a776dd6c1b7cba2a5d7d2a105308bbc892befd81e03dfe863c950"
```

## Run the DOCKER

```sh
docker-compose build
```

```sh
docker-compose up
```
## Possible Errors on Windows OS

```
sh
Gracefully stopping... (press Ctrl+C again to force)
Error response from daemon: error while creating mount source path '/run/desktop/mnt/host/c/Users/siddh/Desktop/segwise/segwise': mkdir /run/desktop/mnt/host/c: file exists
```

- Solutions 

Bring the containers down, remove and restart docker service on windows

```sh
docker-compose down
docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
```

- Run on Powershell
```powershell
Stop-Service -Name com.docker.service
Start-Service -Name com.docker.service
```

- Build again
```sh
docker-compose build
docker-compose up
```
## Payload 

1. Recurring Events:- 
 ```js
 {
   "name": "string",
  "is_scheduled_trigger": true,
  "start_time": "2025-01-07T02:58:59.649Z",
  "schedule_time": "2025-01-07T02:58:59.649Z",
  "is_recurring": true,
  "recurring_minutes": 2147483647,
  "is_test_trigger": true,
}
```

2. Non Recurring Events:- 
```js
{
  "name": "string",
  "start_time": "2025-01-07T02:58:59.649Z",
  "schedule_time": "2025-01-07T02:58:59.649Z",
  "is_recurring": false,
  "payload": "string",
  "is_test_trigger": true,
}
```

### APP Interface

- Go to http://0.0.0.0:8000/api/v1/docs for checking out the OpenAPI Schema

![text](image.png)

## Live APP 
- url :-  http://3.80.85.23:8000/api/v1/docs/
![alt text](image-1.png)


### Costing

- I'm using Amazon EC2 t2.micro instance which comesup with 750 free hours.

- So, for 30 * 24 or 31 * 24 = 720 to 744 hours the effective cost would be 0$, even for 5 API requests/day. 

### RESOURCES used
- ChatGPT, Stackoverflow
- https://www.django-rest-framework.org/api-guide/generic-views/
- Reddit for Docker queries and deployment.


### Additional Features

- Added JWTAuth for the API services 


![alt text](image-2.png)

- User creation endpoint
![alt text](<Screenshot from 2024-12-16 02-10-55.png>)