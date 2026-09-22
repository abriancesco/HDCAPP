from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Property, PropertyImage   # ← ADD THIS

class PropertyResource(resources.ModelResource):
    class Meta:
        model = Property
        import_id_fields = ['address']  # LOCATION is unique enough
        fields = (
            'address',
            'county',
            'site_size',
            'sale_price',
            'sale_date',
            'sqft',
            'access',
            'comments',
            'dom',
        )
        field_mapping = {
            'address': 'LOCATION',
            'county': 'COUNTY',
            'site_size': 'SIZE',
            'sale_price': 'PRICE',
            'sale_date': 'SALEDATE',
            'sqft': 'SQFT',
            'access': 'ACCESS',
            'comments': 'COMMENTS',
            'dom': 'DOM',
        }
        widgets = {
            'sale_date': {'format': '%m/%d/%Y'},
        }

class PropertyAdmin(ImportExportModelAdmin):
    resource_class = PropertyResource

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)   # ← ADD THIS
