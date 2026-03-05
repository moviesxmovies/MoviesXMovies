---
icon: lucide/hard-drive-download
title: Installation
description: Choose your preferred method to install and run the project.
---

Here you will find the steps to set up the project. You can choose between a containerized approach using **Docker** (recommended) or running it **Natively**.

=== "🐳 Docker Way"
    ## Docker Way
 
    #### Create the Docker Compose file

    Create a `docker-compose.yml` file and paste the following configuration:

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

    1. Creates a **Postgres** container as the database.
    2. Injects `.env` as environment variables.
    3. Links database files with a volume named `postgres_data`.
    4. Healthcheck to ensure the DB is up before other services start.
    5. Creates a container using the backend **API image**.
    6. Uses the `latest` tag of our backend image.
    7. Retries automatically if the launch fails.
    8. Pulls the image to keep it updated if there are upstream changes.
    9. Injects `.env` as environment variables.
    10. Maps port `7996` of the host to port `7996` of the container.
    11. Waits for the `db` container to be healthy before starting up.
    12. Links two volumes for **static files** and **media files**.
    13. Creates a container using the **Frontend image**.
    14. Retries automatically if the launch fails.
    15. Pulls the image to keep it updated.
    16. Links frontend files with the `frontend_data` volume.
    17. Creates a volume for the database files.
    18. Creates a volume for static files mounted on a host directory.
    19. Creates a volume for media files mounted on a host directory.
    20. Creates a volume for frontend files mounted on a host directory.
    21. Creates a container using an alpine **Redis image**.
    22. Official Alpine Redis image.
    23. Healthcheck to verify Redis is ready.
    24. Creates a **worker** container (scalable if needed).
    25. Uses the backend image to get the latest code.
    26. Overrides the base command to run an `rqworker`.
    27. Ensures `db` and `redis` are up before the worker starts.
    28. Mounts volumes to allow access to static and media data.

    #### Verify Directories

    !!! warning "Important Prerequisites"
        Before running Docker Compose, ensure the following directories exist on your machine and that the Docker user has ownership of them:
        * `/var/www/moviesxmovies/app`
        * `/var/www/moviesxmovies/media`
        * `/var/www/moviesxmovies/static`

    ### Setup Environment Variables

    Create your own `.env` file using the following structure as a reference:

    ```sh title=".env"
    SECRET_KEY="any_key"
    DEBUG=false
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,192.168.0.13,moviesxmovies.jonaykb.com
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=db_name
    DB_USER=db_user
    DB_PASSWORD=bd_passowrd
    DB_HOST=127.0.0.1
    DB_PORT=5432
    ```

    #### Execute

    Run the following command to start all the necessary containers in detached mode:

    ```sh title="Terminal"
    docker compose up -d
    ```

=== "💻 Native"
    ## Native

    If you prefer to run the application natively, you need to set up the backend and frontend separately. Choose the environment you want to set up below:

    === "Backend (API)"

        ### Backend(API)

        #### Clone the repository:
        ```bash
        git clone [https://github.com/moviesxmovies/MoviesXMoviesBackend](https://github.com/moviesxmovies/MoviesXMoviesBackend)
        cd MoviesXMoviesBackend
        ```

        #### Environment Variables:
        Open `example.env` and create a `.env` file, changing the variables as needed.

        #### Setup:
        ```bash
        uv sync
        ```

        #### Execute:
        
        Using [Just](https://github.com/casey/just):
        ```bash
        just
        # or
        just dev
        ```
        Using Django's `manage.py`:
        ```bash
        uv run manage.py runserver
        ```

    === "Frontend"

        ### Frontend


        #### Clone the repository:
        ```bash
        git clone [https://github.com/moviesxmovies/MoviesXMoviesFrontend](https://github.com/moviesxmovies/MoviesXMoviesFrontend)
        cd MoviesXMoviesFrontend
        ```

        #### Environment Variables:
        Open `example.env` and create a `.env` file, changing the variables as needed.

        *#### Setup:
        ```bash
        npm install
        ```

        #### Execute:
        
        Using [Just](https://github.com/casey/just):
        ```bash
        just
        # or
        just dev
        ```
        Using npm:
        ```bash
        npm run dev
        # or build for deployment
        npm run build
        ```

---

## Accessing the Application

Once your preferred environment is up and running, you can access the different parts of the application using the following links:

| Service            | URL                                                              |
| ------------------ | ---------------------------------------------------------------- |
| 🎨 **Frontend**     | [http://localhost:5173](http://localhost:5173)                   |
| ⚙️ **API Base**     | [http://localhost:8000/api](http://localhost:8000/api)           |
| 📚 **Swagger Docs** | [http://localhost:8000/api/docs](http://localhost:8000/api/docs) |