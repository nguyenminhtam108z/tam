from dSql.dmysql import Dmysql
import os
import json
from pathlib import Path

config_path = Path('./config')
production = os.environ.get('PRODUCTION')
mysql_config = {
    "host": "localhost",
    "user": "root",
    "passwd": "123456",
    "db": "baoninhbinh"
}
if production:
    config_file = config_path / 'config.json'
    config = json.load(open(config_file,'r'))
    mysql_config = config['mysql']

baoninhbinh = Dmysql(**mysql_config)
