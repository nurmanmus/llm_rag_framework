# FastAPI Core Service

This provides a core service for FastAPI applications. It can be used as a subrepository in your projects, allowing you to leverage its features and structure for rapid development of FastAPI services.

## Getting Started

# Local Development

## Setting Up the Environment

1. Install the required dependencies:

```bash
pip install -r core/requirements/dev.txt
```

2. Run the application:

```bash
uvicorn main:app --reload
```

## Docker

1. Example docker file and docker-compose.yml file in core/docker directory. just copy and paste in your main project directory. and run docker-compose up -d

```bash
cp core/docker/docker-compose.yml docker-compose.yml
cp core/docker/Dockerfile Dockerfile
docker-compose up -d
```

## docker and docker-compose installation

1. install docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
```

post installation steps
```bash
sudo usermod -aG docker $USER
newgrp docker
```


2. install docker-compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
