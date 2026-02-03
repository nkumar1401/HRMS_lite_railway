import os

# Only attempt to use pymysql if we are on Railway and mysqlclient is not available
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('MYSQL_HOST'):
    try:
        import pymysql
        pymysql.version_info = (2, 2, 1, "final", 0)
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
