from django.contrib import admin

from accounts.models import Account, Balance

admin.site.register(Account)
admin.site.register(Balance)
