from django.contrib import admin
from .models import Silo, DataField, ValueStore

admin.site.register(Silo)
admin.site.register(DataField)
admin.site.register(ValueStore)