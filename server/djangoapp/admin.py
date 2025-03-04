from django.contrib import admin
from .models import CarMake, CarModel

# from .models import related models

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['carmodel_id', 'name', 'carmake', 'year', 'type']
    list_filter = ['carmake']
    search_fields = ['name', 'carmake']


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('carmake_id', 'name', 'description')
    list_filter = ['name']
    search_fields = ['name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)