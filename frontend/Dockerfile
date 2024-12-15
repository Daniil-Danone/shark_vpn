# Установка Node.js
FROM node:20-alpine

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY package*.json .

# Установка зависимостей
RUN npm install

# Копирование кода
COPY . .

# Сборка React-приложения
RUN npm run build
