from django import forms
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'


from django import forms
from .models import Savings

class SavingsForm(forms.ModelForm):
    class Meta:
        model = Savings
        # We'll include 'amount', 'category', 'description', and 'date'
        # 'time' is usually auto-set, so we don't include it in the form for user input.
        fields = ['amount', 'category', 'description', 'date']
        
        widgets = {
            # This makes the date input a calendar picker in most browsers
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Investment

class InvestmentForm(forms.ModelForm):
    class Meta:
        model = Investment
        # Include fields that the user will input for an investment.
        # 'current_value' can be updated separately or left null initially.
        fields = ['name', 'amount', 'investment_type', 'description', 'date']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model  = Expense
        fields = ['amount', 'category', 'description', 'date']
        widgets = {'date': forms.DateInput(attrs={'type':'date'})}




from django import forms
from .models import BudgetLimit, Expense

class BudgetLimitForm(forms.ModelForm):
    class Meta:
        model = BudgetLimit
        fields = ['category', 'limit', 'frequency']
        widgets = {
            'category': forms.Select(choices=Expense.CATEGORY_CHOICES, attrs={'class': 'form-control'}),
            'limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Limit'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
        }







from django import forms
from .models import IncomeTracker

class IncomeTrackerForm(forms.ModelForm):
    class Meta:
        model = IncomeTracker
        fields = ['amount', 'source', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional description'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'source': forms.Select(),
        }
