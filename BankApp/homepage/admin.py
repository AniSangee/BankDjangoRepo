from django.contrib import admin
from .models import Account, Transaction


admin.site.register(Transaction)

class AccountAmsal(admin.ModelAdmin):
    list_display = ('id', 'user', 'account_number', 'account_type', 'phone_number','email','balance')
    list_filter = ('user', 'account_type')
    search_fields = ['user']
admin.site.register(Account,AccountAmsal)

