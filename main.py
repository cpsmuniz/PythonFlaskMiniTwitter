from src.a_Presentation.UserController import *
from src.a_Presentation.PostController import *
import os

# Please replace all database variables here
os.environ['mysql_connection_string'] = 'mysql+pymysql://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{SCHEMA}'

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
