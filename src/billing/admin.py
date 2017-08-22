from django.contrib import admin
from .models import Transaction
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
	list_display = ["__str__", "timestamp"]

	class Meta:
		model = Transaction

admin.site.register(Transaction, TransactionAdmin)