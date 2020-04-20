from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)

# Configuring the MYSQL
app.config['MYSQL_DATABASE_USER'] = 'public'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b05qv-x4xca'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'manbasedb'

mysql = MySQL(cursorclass = DictCursor)
mysql.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

