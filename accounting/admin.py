from django.contrib import admin
from .models import Journal, Account_names, Entities


admin.site.register(Journal)
admin.site.register(Entities)
admin.site.register(Account_names)
