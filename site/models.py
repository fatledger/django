from django.db import models

class Diamond(models.Model):
  class Meta:
    db_table="diamond"

  sku=models.CharField(primary_key=True, max_length=12)
  shape=models.CharField(max_length=50)
  carat=models.DecimalField(max_digits=5, decimal_places=2)
  cut=models.CharField(max_length=50)
  color=models.CharField(max_length=10)
  clarity=models.CharField(max_length=50)
  vendor_price=models.DecimalField(max_digits=10, decimal_places=2)
  symmetry=models.CharField(max_length=60)
  polish=models.CharField(max_length=60)
  length=models.DecimalField(max_digits=10, decimal_places=2)
  width=models.DecimalField(max_digits=10, decimal_places=2)
  height=models.DecimalField(max_digits=10, decimal_places=2)
  fluorescence=models.CharField(max_length=60)
  cert_id=models.CharField(max_length=22)
  cert_lab=models.CharField(max_length=15)
  comment_text=models.CharField(max_length=2000)
  owner_id=models.IntegerField(max_length=10)
  purchase_date=models.DateField()
  status=models.CharField(max_length=20)
