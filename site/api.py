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
    self.sql_text = """select sku,shape,cut,color,clarity,carat,polish from app.diamond
 where 1=1"""

  def connect(self):
    if self.db_name == 'default':
       self.cursor = connection.cursor()
    else:
       self.cursor = connections[self.db_name].cursor()

  def build_sql(self, filter_obj):
    for key in filter_obj.keys():
      if key == 'shape':
         self.shape_list = filter(None, filter_obj['shape'])
         if len(self.shape_list) > 0:
           self.filter_clause=" and shape in ('%s')" % "','".join(self.shape_list)
           self.sql_text += self.filter_clause
      elif key == 'cut':
         self.cut_list = filter(None, filter_obj['cut'])
         if len(self.cut_list) > 0:
           self.filter_clause=" and cut in ('%s')" % "','".join(self.cut_list)
           self.sql_text += self.filter_clause
      elif key == 'color':
         self.color_list = filter(None, filter_obj['color'])
         if len(self.color_list) > 0:
           self.filter_clause=" and color in ('%s')" % "','".join(self.color_list)
           self.sql_text += self.filter_clause
      elif key == 'clarity':
         self.clarity_list = filter(None, filter_obj['clarity'])
         if len(self.clarity_list) > 0:
           self.filter_clause=" and clarity in ('%s')" % "','".join(self.clarity_list)
           self.sql_text += self.filter_clause
      elif key == 'carat_min':
         self.carat_min = filter_obj['carat_min']
         if self.carat_min is not None:
           self.filter_clause=" and carat >= %d" % self.carat_min
           self.sql_text += self.filter_clause
      elif key == 'carat_max':
         self.carat_max = filter_obj['carat_max']
         if self.carat_max is not None:
           self.filter_clause=" and carat <= %d" % self.carat_max
           self.sql_text += self.filter_clause
      elif key == 'price_min':
         self.price_min = filter_obj['price_min']
         if self.price_min is not None:
           self.filter_clause=" and price >= %d" % self.price_min
           self.sql_text += self.filter_clause
      elif key == 'price_max':
         self.price_max = filter_obj['price_max'] 
         if self.price_max is not None:
           self.filter_clause=" and price <= %d" % self.price_max
           self.sql_text += self.filter_clause     

  def print_sql(self):
    print(self.sql_text)

  def run(self):
    self.cursor.execute(self.sql_text)

    # retrieve column names
    cols=[col[0] for col in self.cursor.description]

    # build multi-dimensional dictionary for resultset
    # self.resultset= [
    #       dict(zip(cols, row))
    #       for row in cursor.fetchall()
    #   ] 
    self.dict_obj= [
          dict(zip(cols, row))
          for row in self.cursor.fetchall()
      ] 

    # return json.dumps(self.dictobj, cls=MyJSONEncoder)
    self.json_obj = json.dumps(self.dict_obj)

  def resultset(self):
    return self.json_obj

  def close(self):
    self.cursor.close()
