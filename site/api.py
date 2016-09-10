from django.db import connection, connections
import json
from decimal import Decimal

db_schemas = {
  'user' : 'db1',
  'search' : 'db2',
  'cart' : 'db2'
}

def dbName(schema):
  if schema == None:
    return 'default'
  elif schema in db_schemas:
    return db_schemas[schema]
  else:
    return None

class MyJSONEncoder(json.JSONEncoder):
  def default(self, obj):
      """ convert Decimal to str """
      if isinstance(obj, Decimal):
        obj = str(obj)
      return obj

class dbo(object):
  """Establishes DB connection, run query, and return resultset"""

  def __init__(self,schema=None):
    self.db_name=dbName(schema)
    # self.resultset = {}

  def connect(self):
    if self.db_name == 'default':
       self.cursor = connection.cursor()
    else:
       self.cursor = connections[self.db_name].cursor()

  def query(self,sqltext):
    self.cursor.execute(sqltext)

    # retrieve column names
    cols=[col[0] for col in self.cursor.description]

    # build multi-dimensional dictionary for resultset
    # self.resultset= [
    #       dict(zip(cols, row))
    #       for row in cursor.fetchall()
    #   ] 
    self.dictobj= [
          dict(zip(cols, row))
          for row in self.cursor.fetchall()
      ] 

    return json.dumps(self.dictobj, cls=MyJSONEncoder)

  def close(self):
    self.cursor.close()
