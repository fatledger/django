from apps.db.api import *

s=dbo('user')
s.connect()
sqltext="select id,upc,title from catalogue_product where id=1"
fs=s.query(sqltext)
print(fs)
s.close()
exit()
