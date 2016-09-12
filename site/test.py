from apps.db.api import *

s=dbObj('user')
s.connect()
# sqltext="select id,upc,title from catalogue_product where id=1"
# fs=s.query(sqltext)
# print(fs)
# s.close()
# exit()
# query_filter = {'shape': ['RD', 'PR', 'OV'], \
#   'cut': ['Ideal', 'Very Good', 'Good'], \ 
#   'clarity': ['IF', 'VS1', 'VS2'], \
#   'color': ['D', 'E'], \
#   'carat_min': 0.5, \
#   'carat_max': 3.5, \
#   'price_min': 250.99, \
#   'price_max': 8300.99}

query_filter = {'shape': ['RD', 'PR', 'OV'], \
  'cut': ['Ideal', 'Very Good', 'Good'], \ 
  'clarity': ['IF', 'VS1', 'VS2'], \
  'color': ['D', 'E'], \
  'carat_min': 0.5, \
  'carat_max': 3.5}
s.build_sql(query_filter)
s.print_sql()
s.run()
json_out=s.resultset()
print(json_out)


import simplejson as json

json_filter=json.dumps(query_filter)

search_query="""select sku,shape,cut,color,clarity,carat,polish from app.diamond
 where 1=1"""

query_filter = json.loads(json_filter)

for key in query_filter.keys():
  if key == 'shape':
     shape_list = filter(None, query_filter['shape'])
  elif key == 'cut':
     cut_list = filter(None, query_filter['cut'])
  elif key == 'color':
     color_list = filter(None, query_filter['color'])
  elif key == 'clarity':
     clarity_list = filter(None, query_filter['clarity'])
  elif key == 'carat_min':
     carat_min = query_filter['carat_min']
  elif key == 'carat_max':
     carat_max = query_filter['carat_max']
  elif key == 'price_min':
     price_min = query_filter['price_min']
  elif key == 'price_max':
     price_max = query_filter['price_max']
 
if len(shape_list) > 0:
  filter_clause=" and shape in ('%s')" % "','".join(shape_list)
  search_query += filter_clause

if len(cut_list) > 0:
  filter_clause=" and cut in ('%s')" % "','".join(cut_list)
  search_query += filter_clause

if len(color_list) > 0:
  filter_clause=" and color in ('%s')" % "','".join(color_list)
  search_query += filter_clause

if len(clarity_list) > 0:
  filter_clause=" and clarity in ('%s')" % "','".join(clarity_list)
  search_query += filter_clause

if carat_min is not None:
  filter_clause=" and carat >= %d" % carat_min
  search_query += filter_clause

if carat_max is not None:
  filter_clause=" and carat <= %d" % carat_max
  search_query += filter_clause

if price_min is not None:
  filter_clause=" and price >= %d" % price_min
  search_query += filter_clause

if price_max is not None:
  filter_clause=" and price <= %d" % price_max
  search_query += filter_clause
