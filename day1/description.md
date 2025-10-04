# Day 1
## Goal: Setup & Basic CRUD

1) Create a python virtual environment

        #on windows
                python -m venv learn
        # on windows:
                learn/Scripts/activate

        # on linux and mac:
                python3 -m venv learn
        # on linux and mac:
                source learn/bin/activate

2) Install fastAPI and uvicorn

        pip install "fastapi[standard]" uvicorn

3) Run the server

        uvicorn main:app --reload