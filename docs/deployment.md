---
icon: lucide/cloud-upload
title: Deployment
---
## Docs
Docs is deployed via GitHub Pages [HERE](./workflows.md#docs-workflows) you can see the workflow
## Docker Files

### Backend
```dockerfile title="Dockerfile Backend"
FROM python:3.14-slim # (1)!

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# (2)!
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# (3)!

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*
# (4)!

COPY pyproject.toml uv.lock ./
# (5)!
RUN uv sync --frozen --no-dev
# (6)!


COPY . .
# (7)!

RUN mkdir -p /app/staticfiles /app/media && \
    adduser --disabled-password --gecos "" django_user && \
    chown -R django_user:django_user /app
# (8)!

USER django_user
# (9)!

EXPOSE 7996

RUN uv run python manage.py collectstatic --noinput
# (10)!

CMD ["sh", "-c", "uv run python manage.py migrate && \\
 uv run uvicorn main.asgi:application --host 0.0.0.0 --port 7996 --workers 4"]
# (11)!
```
{.annotate}

1. **Creates** an **image** with **python 3.14 slim**
2. **Downloads uv**
3. **Set** the **base workdir** as **app**
4. **Downloads dependencies**
5. **Copy** **pyproject.toml** and **uv.lock**
6. **Downloads dependencies**, `--frozen` **forces** to use `uv.lock`, `--no-dev` **excludes** all **dev dependencies**
7. **Copy** **all** files
8. **Create media** and **static directories**, also **create** a **user** and **own** the **base directory**
9. **Selected** the **created** before **user**
10. **Create** **static files**
11. **Running migrations** and **application** with **4 workers**
### Frontend
```dockerfile title="Dockerfile Frontend"
FROM node:22-alpine AS build-stage
# (1)!
WORKDIR /app
# (2)!
COPY package*.json ./
# (3)!
RUN npm ci
# (4)!
COPY . .
# (5)!
RUN npm run build
# (6)!

FROM alpine:latest # (7)!
RUN apk add --no-cache coreutils
# (8)!
WORKDIR /app
# (9)!
COPY --from=build-stage /app/dist /app/
# (10)!


CMD ["sh", "-c", "echo 'Sync complete' && tail -f /dev/null"]
# (11)!
```
{.annotate}

1. **Creates** an **build image** with **node 22 alpine**
2. **Set** the **base workdir** as **app**
3. **Copy** **package.json** and **package-lock.json**
4. **Run** `npm run ci`, is the same as `npm i` but using `package-lock.json` instead of `package.json`
5. **Copy all files**
6. And `run npm build` to **create static files**
7. **Creates** an **production image** with **alpine**
8. **Add** **coreutils** dependency
9. **Set** the **base workdir** as **app**
10. From **Previus build stage**, **copy** the `app/dist` dir and **added it** to `app`
11. **Shows a message** of `Sync complete` and **keep the container alive**

!!! warning
    This **docker file**, indeed **does nothing more** than **copy the files** of the **build** in a **dir**, **serving it to other nginx**, **instead of** creating an **nginx inside** of the **container** and **proxy passing** from the **main nginx**.
## Docker Composes
### Movies X Movies
```yaml title="docker-compose.yml"
services:
  db:  # (1)!
    image: postgres:15-alpine
    container_name: movies_db
    restart: always
    env_file:
      - .env  # (2)!
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data # (3)!
    healthcheck: # (4)!
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 5

  api: # (5)!
    image: moviesxmovies/backend:latest # (6)!
    container_name: movies_api
    restart: always # (7)!
    pull_policy: always # (8)!
    env_file:
      - .env # (9)!
    ports:
      - "7996:7996" # (10)!
    depends_on:
      db: # (11)!
        condition: service_healthy
    volumes: # (12)!
      - static_data:/app/staticfiles
      - media_data:/app/media
  redis: # (21)!
    image: redis:7-alpine # (22)!
    container_name: movies_redis
    restart: always
    healthcheck:
      test: ["CMD", "redis-cli", "ping"] # (23)!
      interval: 5s
      timeout: 3s
      retries: 5

  worker: # (24)!
    image: moviesxmovies/backend:latest # (25)!
    restart: always
    pull_policy: always
    command: python manage.py rqworker default # (26)!
    env_file:
      - .env
    depends_on: # (27)!
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes: # (28)!
      - static_data:/app/staticfiles
      - media_data:/app/media
  web: # (13)!
    image: moviesxmovies/frontend:latest
    container_name: movies_frontend
    restart: always # (14)!
    pull_policy: always # (15)!
    volumes: # (16)!
      - frontend_data:/app

volumes:
  postgres_data: # (17)!
  static_data: # (18)!
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/www/moviesxmovies/static
  media_data: # (19)!
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/www/moviesxmovies/media
  frontend_data: # (20)!
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /var/www/moviesxmovies/app
```
{.annotate}

1. **Creates** a **container** of **postgres** as **DB**
2. **Adds** `.env` as **enviroments variables**
3. **Links DB files** with a **volume** named `postgres_data`
4. **Checks** if **DB** is **up** or not
5. **Creates** a **container** using our **backend image** of the **API**
6. **Our backend image** in the **latest tag**
7. If the **launch fails**, it **retries**
8. If the **docker image** has **changed**, it **pull it**, to **keep it updated**
9. **Adds** `.env` as **enviroments variables**
10. **Open port** `7996` to **port** `7996` of the **container**
11. **Before starting up** the **container**, it **checks** if the `db` **container is up**
12. **Links two volumnes**, one used for **static files**, and the other one to **media files**
13. **Creates** a **container** using our **frontend image**
14. If the **launch fails**, it **retries**
15. If the **docker image** has **changed**, it **pull it**, to **keep it updated**
16. **Links Frontend files** with a **volumne** named `frontend_data`
17. **Creates** a **volumen** for **DB files**
18. **Creates** a **volume** for **static files**, and **mount it** on a **directory** of the **machine**
19. **Creates** a **volume** for **media files**, and **mount it** on a **directory** of the **machine**
20. **Creates** a **volume** for **frontend files**, and **mount it** on a **directory** of the **machine**
21. **Creates** a **container** using an alpine **redis image**
22. **Official** alpine **redis image**
23. **Creates** a **healthcheck** to see if the **container** is **ready**
24. **Create** a **worker**, which later we can run **more** **container** to be **scalable**
25. Using the **backend image**, so it can get **latest code**
26. And **we override** the base **CMD** command and instead we **run** a **rqworker**
27. Before **creating** the **worker**, we have to **secure** that the **db** and **redis** are **up**
28. And **setup** the **volumes** to be **able** to **access** **static** and **media data**

### SonarQube
```yaml title="docker-compose.yml"
version: "3"

services:
  sonarqube:
    image:  mc1arke/sonarqube-with-community-branch-plugin:latest
    env_file:
        - .env
    depends_on:
      - sonar_db
    environment:
      SONAR_JDBC_URL=${POSTSQL_URL}
      SONAR_JDBC_USERNAME=${POSTSQL_USERNAME}
      SONAR_JDBC_PASSWORD=${POSTSQL_PASSWORD}
    ports:
      - "26453:9000"
    volumes:
      - sonarqube_conf:/opt/sonarqube/conf
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_extensions:/opt/sonarqube/extensions
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_temp:/opt/sonarqube/temp

  sonar_db:
    image: postgres:13
    env_file:
    - .env
    environment:
      POSTGRES_USER=${POSTSQL_USERNAME}
      POSTGRES_PASSWORD=${POSTSQL_PASSWORD}
      POSTGRES_DB=${POSTSQL_DB}
    volumes:
      - sonar_db:/var/lib/postgresql
      - sonar_db_data:/var/lib/postgresql/data

volumes:
  sonarqube_conf:
  sonarqube_data:
  sonarqube_extensions:
  sonarqube_logs:
  sonarqube_temp:
  sonar_db:
  sonar_db_data:
```
## Nginx Server
```nginx title="moviesxmovies.conf"
# Redirections and HTTP Security
server {
    listen 80;
    server_name moviesxmovies.jonaykb.com;
    if ($host !~* ^moviesxmovies\.jonaykb\.com$ ) { return 444; }
    return 301 https://$host$request_uri;
}
# Main Server
server {
    listen 443 ssl http2;
    server_name moviesxmovies.jonaykb.com;

    ssl_certificate /etc/letsencrypt/live/moviesxmovies.jonaykb.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/moviesxmovies.jonaykb.com/privkey.pem;


    ssl_session_timeout 1d;
    ssl_protocols TLSv1.2 TLSv1.3;

    location /api/ {
        proxy_pass http://127.0.0.1:7996/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        }

# Location for django adin
    location /admin/ {
            proxy_pass http://127.0.0.1:7996/admin/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
    }

# Location for django statics files
    location /static/ {
            alias /var/www/moviesxmovies/static/;
            expires 30d;
            add_header Cache-Control "public";
            # Si no existe el archivo, devuelve 404, NO vayas al index.html
            try_files $uri =404;
    }

# Location for django media files
    location /media/ {
            alias /var/www/moviesxmovies/media/;
            try_files $uri =404;
    }

# Redirection to MoviesXMovies docs in GitHub Pages
    location /docs {
            proxy_pass https://moviesxmovies.github.io/MoviesXMovies;
    }

# Serve frontend files
    location / {
            root /var/www/moviesxmovies/app;
            index index.html;
            try_files $uri $uri/ /index.html;

    }

}
```

## Domain

**The domain** `moviesxmovies.jonaykb.com` is **bought** at **Cloudflare** with a **record pointing** to a **Dynamic IP**, but **thanks to** [this project](https://github.com/JonayKB/DynamicDNS) **we keep** our record **updated** and **pointing** to the **correct IP**