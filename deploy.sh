#!/bin/bash

# Остановить и удалить Docker Compose
sudo docker-compose -f "docker-compose.prod.yml" down

# Обновить код из репозитория
git pull

# Построить Docker Compose
sudo docker-compose -f "docker-compose.prod.yml" build

# Запустить Docker Compose в фоновом режиме
sudo docker-compose -f "docker-compose.prod.yml" up -d

# Удаляем не используемые образы
sudo docker image prune -f