python manager.py shell

====
# import simplejson as json
from apps.db.api import *

# s=dbObj('user')
s=search('search')
s.connect()

query_obj = { \
'filter': {'shape': ['RD', 'PR', 'OV'], \
'cut': ['Ideal', 'Very Good', 'Good'], \ 
'clarity': ['IF', 'VS1', 'VS2'], \
'color': ['D', 'E'], \
'carat_min': 0.5, \
'carat_max': 3.5}, \
'page': {'offset':1, 'limit':5}, \
'sort_by': ('shape', 'color', 'clarity', 'cut', 'carat') \
}

s.build_sql(query_obj)
s.print_sql()
s.run()

json_out=s.resultset()
print(json_out)
dict_out=s.dict_resultset()
print(dict_out)
