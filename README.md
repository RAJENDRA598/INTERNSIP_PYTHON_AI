OPEN POWERSHELL

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

py -m venv venv OR python -m venv venv

venv\scripts\activate #windows

pip install flask psycopg2-binary

#to run

py app.py or python app.py
