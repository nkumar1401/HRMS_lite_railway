import os

# This monkeypatch allows PyMySQL to act as a replacement for mysqlclient
# It is required because Django checks for mysqlclient version >= 2.2.0
try:
    import pymysql
    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
