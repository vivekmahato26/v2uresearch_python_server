import pymysql
pymysql.install_as_MySQLdb()

try:
    import MySQLdb
    MySQLdb.version_info = (2, 2, 1, 'final', 0)
    MySQLdb.__version__ = '2.2.1'
except ImportError:
    pass

# Monkey-patch to bypass MySQL version check (Server handles 5.7, Django wants 8.0)
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except ImportError:
    pass
