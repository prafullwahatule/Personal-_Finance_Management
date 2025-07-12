from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone
from django.db import models

class UserProfile(models.Model):
    INVESTMENT_GOALS_CHOICES = [
        ("Short Term", "Short Term"),
        ("Long Term", "Long Term"),
        ("Retirement", "Retirement"),
        ("Wealth Growth", "Wealth Growth"),
        ("Tax Saving", "Tax Saving"),
    ]
    
    RISK_CHOICES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High")]
    GENDER_CHOICES = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    mobile = models.CharField(max_length=15, null=True, blank=True)
    dob = models.DateField(null=True, blank=True, default=timezone.now)  # Default DOB as current date
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    
    
    savings = models.FloatField(null=True, blank=True)
    existing_investments = models.FloatField(null=True, blank=True)

    risk_appetite = models.CharField(max_length=10, choices=RISK_CHOICES, null=True, blank=True)
    investment_goals = models.CharField(max_length=20, choices=INVESTMENT_GOALS_CHOICES, null=True, blank=True)
    preferred_investments = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # Profile creation time
    updated_at = models.DateTimeField(auto_now=True)  # Auto update when modified

    def __str__(self):
        return f"{self.user.username} - Profile"



# savings_app/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone # Make sure this is imported!

class Savings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    CATEGORY_CHOICES = [
        ('Emergency Fund', 'Emergency Fund'),
        ('Down Payment', 'Down Payment'),
        ('Retirement', 'Retirement'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now) # This will store the date in Asia/Kolkata timezone
    time = models.TimeField(default=timezone.now) # This will store the time in Asia/Kolkata timezone

    def __str__(self):
        return f"{self.user.username} — {self.category}: ₹{self.amount} on {self.date} at {self.time.strftime('%I:%M %p')}"

    class Meta:
        verbose_name_plural = "Savings"
        ordering = ['-date', '-time']




# investments_app/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone # Make sure this is imported!

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    INVESTMENT_TYPE_CHOICES = [
        ('Stocks', 'Stocks'),
        ('Mutual Funds', 'Mutual Funds'),
        ('Bonds', 'Bonds'),
        ('Real Estate', 'Real Estate'),
        ('Cryptocurrency', 'Cryptocurrency'),
        ('Fixed Deposit', 'Fixed Deposit'),
        ('Other', 'Other'),
    ]
    investment_type = models.CharField(max_length=50, choices=INVESTMENT_TYPE_CHOICES)
    
    name = models.CharField(max_length=255)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now) # Date of investment or last update in Asia/Kolkata
    time = models.TimeField(default=timezone.now) # Time of investment or last update in Asia/Kolkata

    def __str__(self):
        return f"{self.user.username} — {self.name} ({self.investment_type}): ₹{self.amount} on {self.date} at {self.time.strftime('%I:%M %p')}"

    class Meta:
        verbose_name_plural = "Investments"
        ordering = ['-date', '-time']





# # expense data model
class Expense(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Rent', 'Rent'),
        ('Utilities', 'Utilities'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]
    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    date        = models.DateField(default=timezone.now)
    time        = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} — {self.category}: ₹{self.amount} on {self.date}"




class BudgetLimit(models.Model):
    FREQUENCY_CHOICES = [
        ('monthly', 'Monthly'),
        ('annually', 'Annually'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    category    = models.CharField(max_length=20, choices=Expense.CATEGORY_CHOICES)
    limit       = models.DecimalField(max_digits=10, decimal_places=2)
    frequency   = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='monthly')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.category} ({self.frequency}): ₹{self.limit}"




# Income Model
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class IncomeTracker(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    amount      = models.DecimalField(max_digits=10, decimal_places=2)
    SOURCE_CHOICES = [
        ('Salary', 'Salary'),
        ('Freelance', 'Freelance'),
        ('Business', 'Business'),
        ('Investment', 'Investment'),
        ('Gift', 'Gift'),
        ('Other', 'Other'),
    ]
    source      = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    description = models.TextField(blank=True)
    date        = models.DateField(default=timezone.now)
    time        = models.TimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} — {self.source}: ₹{self.amount} on {self.date}"






# # stock data model
class StockData(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=20)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('date', 'symbol')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.symbol} - {self.date}"



# Updated MutualFundData model
from django.db import models

class MutualFundData(models.Model):
    scheme_code = models.CharField(max_length=50)
    scheme_name = models.CharField(max_length=500)
    isin_div_payout = models.CharField(max_length=50, null=True, blank=True)
    isin_div_reinvestment = models.CharField(max_length=50, null=True, blank=True)
    net_asset_value = models.FloatField()
    date = models.DateField()

    class Meta:
        unique_together = ('scheme_code', 'date')  # Ek scheme ek date mein ek hi record hona chahiye

    def __str__(self):
        return f"{self.scheme_name} (NAV ₹{self.net_asset_value} on {self.date})"





# # commodity data model
class CommodityData(models.Model):
    date = models.DateField()  # Date of the commodity data entry
    name = models.CharField(max_length=100)  # Name of the commodity (symbol)
    open = models.FloatField()  # Opening price
    high = models.FloatField()  # High price during the day
    low = models.FloatField()  # Low price during the day
    close = models.FloatField()  # Closing price
    volume = models.IntegerField()  # Volume traded
    price_inr = models.FloatField(null=True)  # Price in INR (if applicable, can be null)
    unit = models.CharField(max_length=10, default='kg')  # Unit of the commodity (default: kg)

    class Meta:
        # Ensure that no duplicate data is inserted for the same commodity on the same day
        constraints = [
            models.UniqueConstraint(fields=['name', 'date'], name='unique_commodity_data')
        ]

    def __str__(self):
        # Return a string representation with price_inr and unit
        return f"{self.name} - {self.date} - ₹{self.price_inr} per {self.unit}"






#crypto data model
class CryptoHistoryData(models.Model):
    name = models.CharField(max_length=50)  # Name of the cryptocurrency
    symbol = models.CharField(max_length=10)  # Symbol of the cryptocurrency (e.g., BTC, ETH)
    date = models.DateField()  # Date of the record (specific to each day)
    price_inr = models.FloatField()  # Price in INR for that day
    market_cap_inr = models.FloatField()  # Market capitalization in INR for that day
    volume_24h = models.FloatField()  # 24-hour trading volume for that day
    change_24h = models.FloatField()  # 24-hour price change (percentage) for that day

    class Meta:
        unique_together = ('name', 'symbol', 'date')  # Unique records based on cryptocurrency name, symbol, and date

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.date}"






from django.db import models
from django.contrib.auth.models import User

class DeleteAccountOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"






# models.py
class ExpenseActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=10)  # 'Added' or 'Remove'
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} — {self.action} — {self.created_at}"
