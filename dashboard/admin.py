from django.contrib import admin
from .models import UserProfile, Savings, Investment, Expense, BudgetLimit, IncomeTracker, StockData, MutualFundData, CommodityData, CryptoHistoryData, DeleteAccountOTP, ExpenseActivityLog


# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Savings)
admin.site.register(Investment)

admin.site.register(Expense)
admin.site.register(BudgetLimit)
admin.site.register(IncomeTracker)
admin.site.register(StockData)
admin.site.register(MutualFundData)
admin.site.register(CommodityData)
admin.site.register(CryptoHistoryData)



admin.site.register(DeleteAccountOTP)


admin.site.register(ExpenseActivityLog)



