import pymysql
import os

# Check if we are running in a production/Railway environment
# Railway usually sets RAILWAY_ENVIRONMENT, but we can also check for MYSQLHOST
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('MYSQLHOST')

if IS_RAILWAY:
    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()
