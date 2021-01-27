import MySQLdb
import MySQLdb.cursors
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234567',
    'db': 'baoninhbinh'
}


def mysql_connect():
    conn = MySQLdb.connect(host=mysql_config['host'],  # your host, usually localhost
                           user=mysql_config['user'],  # your username
                           passwd=mysql_config['password'],  # your password
                           db=mysql_config['db'], cursorclass=MySQLdb.cursors.DictCursor)
    conn.autocommit(True)
    return conn
