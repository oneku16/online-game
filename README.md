# mini-online-game

## Technologies used
* [FastAPI](https://fastapi.tiangolo.com/): The web framework for perfectionists with deadlines (FastAPI builds better web apps with less code).
* [PostgreSQL](https://www.postgresql.org/): The storage for data.
* [Docker](https://app.docker.com/): Command center for innovative local and cloud native container development.


## Installation
* If you wish to run your own build, first ensure you have python12<= and Docker.
* Then, Git clone this repo to your PC
    ```bash
        $ git clone https://github.com/oneku16/online-game.git
    ```

* #### Dependencies
    1. Cd into cloned repo:
        ```bash
            $ cd online-game
        ```
    2. Create and fire up your virtual environment:
        ```bash
            $ python3 -m venv .venv
            $ source .venv/bin/activate
        ```
    3. Install the dependencies needed to run the app:
        ```bash
            $ pip install -r requirements.txt
        ```
    4. Make those migrations work
        ```bash
            $ alembic revision -m "initial migrate"
            $ alembic upgrade head
        ```

* #### Run It
    Fire up the server using this one simple command:
    ```bash
        $ docker-compose up -d
    ```
    You can now access the file api service on your browser by using
    ```
        http://localhost:8000/
    ```
* #### my[py]
    ```bash
        $ mypy app test
    ```

* #### black
    ```bash
        $ black .
    ```
  
* #### ruff
    ```bash
        $ ruff check --fix
    ```
  
* #### pytest
    ```bash
        $ pytest
    ```