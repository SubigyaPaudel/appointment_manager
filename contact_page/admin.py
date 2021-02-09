from django.contrib import admin
from .models import Host, Visitor, Meeting, Address
# Register your models here.

admin.site.register(Host)
admin.site.register(Visitor)
admin.site.register(Meeting)
admin.site.register(Address)