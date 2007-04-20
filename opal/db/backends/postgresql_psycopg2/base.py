"""
PostgreSQL database backend for Django.

Requires psycopg 2: http://initd.org/projects/psycopg2
"""

from opal.db.backends import util
try:
    import psycopg2 as Database
except ImportError, e:
    from opal.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured, "Error loading psycopg2 module: %s" % e

DatabaseError = Database.DatabaseError

try:
    # Only exists in Python 2.4+
    from threading import local
except ImportError:
    # Import copy of _thread_local.py from Python 2.4
    from opal.utils._threading_local import local

class DatabaseWrapper(local):
    def __init__(self):
        self.connection = None
        self.queries = []

    def cursor(self):
        from opal.conf import settings
        if self.connection is None:
            if settings.DATABASE_NAME == '':
                from opal.core.exceptions import ImproperlyConfigured
                raise ImproperlyConfigured, "You need to specify DATABASE_NAME in your Django settings file."
            conn_string = "dbname=%s" % settings.DATABASE_NAME
            if settings.DATABASE_USER:
                conn_string = "user=%s %s" % (settings.DATABASE_USER, conn_string)
            if settings.DATABASE_PASSWORD:
                conn_string += " password='%s'" % settings.DATABASE_PASSWORD
            if settings.DATABASE_HOST:
                conn_string += " host=%s" % settings.DATABASE_HOST
            if settings.DATABASE_PORT:
                conn_string += " port=%s" % settings.DATABASE_PORT
            self.connection = Database.connect(conn_string)
            self.connection.set_isolation_level(1) # make transactions transparent to all cursors
        cursor = self.connection.cursor()
        cursor.execute("SET TIME ZONE %s", [settings.TIME_ZONE])
        if settings.DEBUG:
            return util.CursorDebugWrapper(cursor, self)
        return cursor

    def _commit(self):
        return self.connection.commit()

    def _rollback(self):
        if self.connection:
            return self.connection.rollback()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

supports_constraints = True

def quote_name(name):
    if name.startswith('"') and name.endswith('"'):
        return name # Quoting once is enough.
    return '"%s"' % name

def dictfetchone(cursor):
    "Returns a row from the cursor as a dict"
    # TODO: cursor.dictfetchone() doesn't exist in psycopg2,
    # but no Django code uses this. Safe to remove?
    return cursor.dictfetchone()

def dictfetchmany(cursor, number):
    "Returns a certain number of rows from a cursor as a dict"
    # TODO: cursor.dictfetchmany() doesn't exist in psycopg2,
    # but no Django code uses this. Safe to remove?
    return cursor.dictfetchmany(number)

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    # TODO: cursor.dictfetchall() doesn't exist in psycopg2,
    # but no Django code uses this. Safe to remove?
    return cursor.dictfetchall()

def get_last_insert_id(cursor, table_name, pk_name):
    cursor.execute("SELECT CURRVAL('\"%s_%s_seq\"')" % (table_name, pk_name))
    return cursor.fetchone()[0]

def get_date_extract_sql(lookup_type, table_name):
    # lookup_type is 'year', 'month', 'day'
    # http://www.postgresql.org/docs/8.0/static/functions-datetime.html#FUNCTIONS-DATETIME-EXTRACT
    return "EXTRACT('%s' FROM %s)" % (lookup_type, table_name)

def get_date_trunc_sql(lookup_type, field_name):
    # lookup_type is 'year', 'month', 'day'
    # http://www.postgresql.org/docs/8.0/static/functions-datetime.html#FUNCTIONS-DATETIME-TRUNC
    return "DATE_TRUNC('%s', %s)" % (lookup_type, field_name)

def get_limit_offset_sql(limit, offset=None):
    sql = "LIMIT %s" % limit
    if offset and offset != 0:
        sql += " OFFSET %s" % offset
    return sql

def get_random_function_sql():
    return "RANDOM()"

def get_fulltext_search_sql(field_name):
    raise NotImplementedError

def get_drop_foreignkey_sql():
    return "DROP CONSTRAINT"

def get_pk_default_value():
    return "DEFAULT"

OPERATOR_MAPPING = {
    'exact': '= %s',
    'iexact': 'ILIKE %s',
    'contains': 'LIKE %s',
    'icontains': 'ILIKE %s',
    'gt': '> %s',
    'gte': '>= %s',
    'lt': '< %s',
    'lte': '<= %s',
    'startswith': 'LIKE %s',
    'endswith': 'LIKE %s',
    'istartswith': 'ILIKE %s',
    'iendswith': 'ILIKE %s',
}