<div align="center">
    <img width="350" height="48" src="app/static/images/admin/logo_full.png">
</div>

# :mountain_snow: NORDEND

Nordend is a minimalistic CMS build on top of Flask and Vue.js

## Prerequisites

- [Redis](https://redis.io)

## How to run the development server?

After cloning this repository open a terminal inside its directory and
follow these steps:

1. Set up a Python virtual environment and activate it
    ```bash
    python3 -m venv env
    source env/bin/activate 
    ```

2. Install all required packages/dependencies
    ```bash
    pip install -r requirements.txt
    npm ci
    ```

3. Compile the JavaScript sources
    ```bash
    npm run dev
    ```

4. Create a SQLite database
    ```bash
    flask db upgrade
    ```

5. Run the Flask development server
    ```bash
    flask run --no-reload
    ```

Now go and visit [localhost:5000/admin](http://localhost:5000/admin)