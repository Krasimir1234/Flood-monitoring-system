# Austrian Flood Monitoring and Emergency Response System

### Run the project

### 1) Install 2 more dependencies (for connecting MySQL):
*pip install mysql*	   
*pip install mysql-connector-python*

### 2 Add your “MySQL” credentials
[server.py]() file in the def *__init__(self)* f.e. my credentials:
                *host="localhost",
                user="root",
                password="x",
                database="flood_monitor"*

### 3) Create tables for data in MySQL
Run file [flood_monitor.sql](flood_monitor.sql) in [“MySQL workbench”](https://dev.mysql.com/downloads/installer/) app

### 4) Integration IDE & MySQL
Connect the created tables (not yet finished) in the database with your chosen IDE (PyCharm, VS code...)



### Run the webserver
You can start the app by executing
```bash
python start.py
```
Then, you can navigate to http://127.0.0.1:7890/



### Testing with [pytest](https://docs.pytest.org/)
To trigger the automated tests, execute
```bash
pytest
```
Note, that your `print` statements will not be visible, 
unless you add the `-s` argument to the call, i.e. `pytest -s`