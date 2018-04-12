from django.contrib import admin
from .models import Panchayat, RankedPanchayat, villageDetails


admin.site.register(Panchayat)
admin.site.register(RankedPanchayat)
admin.site.register(villageDetails)
