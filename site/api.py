from django.db import connection, connections
# import json
import simplejson as json
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

# no longer need with simplejson
class MyJSONEncoder(json.JSONEncoder):
  def default(self, obObj):
      """ convert Decimal to str """
      if isinstance(obj, Decimal):
        obj = str(obj)
      return obj

class dbObj(object):
  """Establishes DB connection, run query, and return resultset"""

  def __init__(self,schema=None):
    self.db_name=dbName(schema)
    # self.resultset = {}
    self.filter_clause=None
    self.json_obj = None
    self.dict_obj = None
    self.sql_text = "select current_database() db_name"  # default query if custom query is not provided

  def connect(self):
    if self.db_name == 'default':
       self.cursor = connection.cursor()
    else:
       self.cursor = connections[self.db_name].cursor()

  def build_sql(self, filter_obj):
    pass

  def print_sql(self):
    print(self.sql_text)

  def run(self):
    self.cursor.execute(self.sql_text)

    # retrieve column names
    cols=[col[0] for col in self.cursor.description]

    # build multi-dimensional dictionary for resultset
    self.returnObj = {'error':None}

    # (doesn't work) self.rset = self.cursor.dictfetchall()

    # build query resultset
    # self.resultset= [
    #       dict(zip(cols, row))
    #       for row in cursor.fetchall()
    #   ] 
    self.rset = [
          dict(zip(cols, row))
          for row in self.cursor.fetchall()
      ] 

    self.returnObj.update({'result':self.rset})

    # return json.dumps(self.dictobj, cls=MyJSONEncoder)
    self.json_obj = json.dumps(self.returnObj)

  def resultset(self):
    return self.json_obj

  def dict_resultset(self):
    return self.returnObj

  def close(self):
    self.cursor.close()


class search(dbObj):
  def build_sql(self, filter_obj):

    self.sql_text = """select sku,shape,cut,color,clarity,carat,polish from app.diamond where 1=1"""

    if filter_obj['filter'] is not None:
      for key in filter_obj['filter'].keys():
        if key in ('shape','cut','color','clarity'):
           self.inlist = filter(None, filter_obj['filter'][key])
           if len(self.inlist) > 0:
             self.filter_clause=" and %s in ('%s')" % (key, "','".join(self.inlist))
             self.sql_text += self.filter_clause
        elif key == 'carat_min':
           self.carat_min = filter_obj['filter'][key]
           if self.carat_min is not None:
             self.filter_clause=" and carat >= %d" % self.carat_min
             self.sql_text += self.filter_clause
        elif key == 'carat_max':
           self.carat_max = filter_obj['filter'][key]
           if self.carat_max is not None:
             self.filter_clause=" and carat <= %d" % self.carat_max
             self.sql_text += self.filter_clause
        elif key == 'price_min':
           self.price_min = filter_obj['filter'][key]
           if self.price_min is not None:
             self.filter_clause=" and price >= %d" % self.price_min
             self.sql_text += self.filter_clause
        elif key == 'price_max':
           self.price_max = filter_obj['filter'][key]
           if self.price_max is not None:
             self.filter_clause=" and price <= %d" % self.price_max
             self.sql_text += self.filter_clause     

    if filter_obj['page'] is not None:
      for key in filter_obj['page'].keys():
        if key == 'offset':
          self.offset = filter_obj['page'][key]
          self.sql_text += ' offset %d' % self.offset
        elif key == 'limit':
          self.offset = filter_obj['page'][key]
          self.sql_text += ' limit %d' % self.offset

class diamond_detail(dbObj):
  def build_sql(self, sku):
    self.sql_text = """select sku,shape,cut,color,clarity,carat,polish,symmetry, cert_id,cert_lab
from app.diamond where sku='%s'""" % sku

