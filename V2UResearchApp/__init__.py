import pymysql
pymysql.install_as_MySQLdb()

try:
    import MySQLdb
    MySQLdb.version_info = (2, 2, 1, 'final', 0)
    MySQLdb.__version__ = '2.2.1'
except ImportError:
    pass
