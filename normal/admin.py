from django.contrib import admin

from .models import Address, AddressNormal, Lookup

class AddressNormalAdmin(admin.ModelAdmin):
  list_display = ['id', 'lines', 'city', 'state', 'postalCode']

class LookupAdmin(admin.ModelAdmin):
  list_display = ['provider', 'in_line1', 'in_city', 'in_state', 'in_postalCode', 'out_line1', 'out_city', 'out_state', 'out_postalCode']

admin.site.register(Address)
admin.site.register(AddressNormal, AddressNormalAdmin)
admin.site.register(Lookup, LookupAdmin)
