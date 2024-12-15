# SHARKVPN BOT

Telegram bot for selling VPN configs

## Stack
Python 3.11, Django, PostgreSQL, Docker, Nginx

## Packages
django, django-jazzmin, uvicorn, daphne, psycopg2-binary, aiogram

## Startup Local Development
To run a project in Docker, you need to enter the following command
```shell
docker-compose -f "docker-compose.dev.yml" up --build
```

## Startup Prod Development
To run a project in Docker, you need to enter the following command
```shell
docker-compose -f "docker-compose.prod.yml" up --build
```

or

```shell
./deploy.sh
```

when you need to pull new changes and restart project with new features

To make a migration. Locally open a terminal in the root of the project and write
```shell
cd backend
python manage.py makemigrations
```


## Authors
[Daniil Kolevatykh](https://github.com/Daniil-Danone)
