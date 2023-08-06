Django-LODField
------------------

A Django model representation for a list of python objects.

##### 1) Installation
```
pip install django-lodfield
```
or
```
git clone https://github.com/nakule/django-lodfield.git django-lodfield
cd django-lodfield
python setup.py install
```

##### 2) Import the List of Dictionary (LOD) model field
```
from LODField import LODField
```

##### 3) Define the model Field
```
class Invoice(models.Model):
	paid = models.BooleanField(default=False)

	# Simple Usage
	invoice_lines = LODField(max_length=10000)

	# Set Limit for Admin Form
	invoice_lines = LODField(max_length=10000, lines=10)

	# Set Fields for the Dictionaries in the List
	invoice_lines = LODField(max_length=10000, lines=10,
		keys=["Description", "Amount in Cents",
		"Amount in Dollars"])
```

##### 4) Register Model to the Django Admin Interface (Optional)
```
from django.contrib import admin
admin.site.register(Invoice)
```