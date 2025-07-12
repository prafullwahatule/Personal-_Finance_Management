from reportlab.pdfbase import pdfmetrics

def wrap_text(text, max_width, font_name, font_size):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + (' ' if current_line else '') + word
        test_line_width = pdfmetrics.stringWidth(test_line, font_name, font_size)
        if test_line_width <= max_width:
            current_line = test_line
        else:
            # current_line full, start new line
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines



from datetime import timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import numpy as np # Although numpy isn't directly used in calculations, it's good practice to keep imports if they were intended for future use.
from django.utils import timezone
from django.db.models import Sum
from .models import IncomeTracker


def get_income_analysis(user, period='annual', custom_start=None, custom_end=None):
    today = timezone.now().date()
    start_date = today
    end_date = today
    income_all = IncomeTracker.objects.none() # Initialize as an empty queryset

    if period == 'overall':
        # Get all income entries for the user
        income_all = IncomeTracker.objects.filter(user=user)
        # Determine start_date: if data exists, use the earliest date, otherwise today
        start_date = income_all.order_by('date').first().date if income_all.exists() else today
        end_date = today # End date is always today for overall

    elif period == 'annual':
        start_date = today.replace(month=1, day=1)  # Start of the current year
        end_date = today # End date is today
        income_all = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    elif period == 'monthly':
        start_date = today.replace(day=1) # Start of the current month
        end_date = today # End date is today
        income_all = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    elif period == 'custom' and custom_start and custom_end:
        # Ensure custom dates are date objects if they come as strings, though Django usually handles this.
        start_date = custom_start
        end_date = custom_end
        income_all = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    else:
        # Default to annual if an invalid period is passed
        start_date = today.replace(month=1, day=1)
        end_date = today
        income_all = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    # --- Calculations with Robustness ---

    # Calculate the number of months in the period. Ensure a minimum of 1 month to avoid division by zero.
    # This calculation considers the full span of months from start_date to end_date.
    months = ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month) + 1
    months = max(months, 1) # Ensure months is at least 1, even if the date range is very short or inverted.

    # Total income for the period
    total_income = income_all.aggregate(total=Sum('amount'))['total'] or 0.0

    # Source-wise totals
    source_totals = income_all.values('source').annotate(total=Sum('amount')).order_by('-total')

    # Safely get highest and lowest source
    highest_source = source_totals[0] if source_totals.exists() else {'source': 'N/A', 'total': 0.0}
    lowest_source = source_totals.last() if source_totals.exists() else {'source': 'N/A', 'total': 0.0}

    # Average monthly income, handling division by zero
    average_monthly_income = total_income / months if months > 0 else 0.0

    # Passive income calculation
    passive_sources = ['Investment', 'Gift'] # Define your passive income sources
    passive_income_total = income_all.filter(source__in=passive_sources).aggregate(total=Sum('amount'))['total'] or 0.0
    passive_ratio = (passive_income_total / total_income) * 100 if total_income > 0 else 0.0

    # Average entry frequency
    monthly_entry_counts = defaultdict(int)
    for income in income_all:
        month_key = income.date.strftime("%Y-%m")
        monthly_entry_counts[month_key] += 1

    # Ensure avg_entry_frequency is 0.0 if there are no entries or no months calculated
    total_entries = sum(monthly_entry_counts.values())
    avg_entry_frequency = total_entries / months if months > 0 else 0.0

    # Data for charts (source labels and amounts, monthly bar chart)
    source_labels = [item['source'] for item in source_totals]
    source_amounts = [float(item['total']) for item in source_totals] # Ensure float for all amounts

    bar_labels = []
    bar_values = []
    # Iterate through each month in the determined range (start_date to end_date)
    current_date_iter = start_date
    while current_date_iter <= end_date:
        key = current_date_iter.strftime("%Y-%m")
        bar_labels.append(key)
        bar_values.append(monthly_entry_counts.get(key, 0)) # Default to 0 if no entries for the month
        current_date_iter += relativedelta(months=1)

    return {
        'total_income': round(float(total_income), 2), # Ensure float and round
        'highest_source': highest_source,
        'lowest_source': lowest_source,
        'average_monthly_income': round(float(average_monthly_income), 2), # Ensure float and round
        'passive_ratio': round(float(passive_ratio), 2), # Ensure float and round
        'avg_entry_frequency': round(float(avg_entry_frequency), 1), # Ensure float and round
        'source_labels': source_labels,
        'source_amounts': source_amounts,
        'bar_labels': bar_labels,
        'bar_values': bar_values,
    }


def generate_detailed_income_summary(analysis_data):
    total_income = analysis_data['total_income']
    highest_source = analysis_data['highest_source']
    lowest_source = analysis_data['lowest_source']
    average_monthly_income = analysis_data['average_monthly_income']
    passive_ratio = analysis_data['passive_ratio']
    avg_entry_frequency = analysis_data['avg_entry_frequency']

    text_summary = "INCOME FINANCIAL OVERVIEW\n\n"

    text_summary += "1. TOTAL INCOME:\n"
    text_summary += f"   The total income received during the selected period is Rs.{total_income:.2f}. " \
                    "This value represents the sum of all income amounts recorded by you, " \
                    "regardless of the source or frequency. It provides a comprehensive overview " \
                    "of your earnings over the chosen timeframe.\n\n"

    if highest_source:
        text_summary += "2. HIGHEST INCOME SOURCE:\n"
        text_summary += f"   The source contributing the highest portion of your income is '{highest_source['source']}', " \
                        f"which contributed Rs.{highest_source['total']:.2f}. " \
                        "This helps identify the main pillar of your earnings and allows you to focus on sustaining or growing this income stream.\n\n"
    else:
        text_summary += "2. HIGHEST INCOME SOURCE:\n   No income sources recorded for this period.\n\n"

    if lowest_source and lowest_source != highest_source:
        text_summary += "3. LOWEST INCOME SOURCE:\n"
        text_summary += f"   The source contributing the least income is '{lowest_source['source']}', " \
                        f"with a total of Rs.{lowest_source['total']:.2f}. " \
                        "This information can help you evaluate if this income source is worth maintaining or improving.\n\n"

    text_summary += "4. AVERAGE MONTHLY INCOME:\n"
    text_summary += f"   Your average monthly income over the selected period is Rs.{average_monthly_income:.2f}. " \
                    "This figure is calculated by dividing the total income by the number of months considered. " \
                    "It gives a sense of your regular monthly earning capacity.\n\n"

    text_summary += "5. PASSIVE INCOME RATIO:\n"
    text_summary += f"   Out of your total income, {passive_ratio:.2f}% comes from passive income sources such as investments or gifts. " \
                    "Passive income is beneficial as it requires less active effort to maintain and can provide financial stability.\n\n"

    text_summary += "6. AVERAGE INCOME ENTRY FREQUENCY:\n"
    text_summary += f"   On average, you record income entries {avg_entry_frequency:.1f} times per month. " \
                    "This metric indicates how frequently income is logged, which could reflect the diversity and regularity of your income streams.\n\n"

    text_summary += "7. MONTHLY INCOME ENTRY FREQUENCY BREAKDOWN:\n"
    text_summary += "   This section lists the number of income entries recorded each month during the period:\n"
    for label, value in zip(analysis_data['bar_labels'], analysis_data['bar_values']):
        text_summary += f"     - {label}: {value} entries\n"

    # Final paragraph in sentence case
    text_summary += ("\nInterpreting this data helps you understand not just how much you earn, "
                     "but also where it comes from, how regularly you receive it, and how stable or diversified your income streams are. "
                     "This detailed understanding enables better financial planning, budgeting, and investment decisions.\n")

    return text_summary




from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Expense, BudgetLimit
from decimal import Decimal

def get_expense_analysis(user, period='annual', custom_start=None, custom_end=None):
    today = timezone.now().date()
    start_date = today 
    end_date = today   
    expenses_for_period = Expense.objects.none() # Renamed to avoid confusion with overall_expenses

    # --- Unified date filtering logic ---
    if period == 'overall':
        # For 'overall', filter all user expenses first to find the true start date
        all_user_expenses = Expense.objects.filter(user=user)
        start_date = all_user_expenses.order_by('date').first().date if all_user_expenses.exists() else today
        end_date = today
        expenses_for_period = all_user_expenses # All expenses are relevant for overall
    
    elif period == 'annual':
        # Current calendar year: Jan 1st to today
        start_date = today.replace(month=1, day=1) 
        end_date = today
        expenses_for_period = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    elif period == 'monthly':
        # Current month: 1st to today
        start_date = today.replace(day=1) 
        end_date = today
        expenses_for_period = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    elif period == 'custom' and custom_start and custom_end:
        start_date = custom_start
        end_date = custom_end
        expenses_for_period = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    else:
        # Default to annual (current calendar year) if invalid period or missing custom dates
        start_date = today.replace(month=1, day=1) 
        end_date = today
        expenses_for_period = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    # Ensure dates are consistent and valid for calculations
    if start_date > end_date:
        start_date, end_date = end_date, start_date 

    # Calculate total expense for the period, ensuring it's a Decimal
    total_expense = expenses_for_period.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')

    # --- Dynamic Monthly Expense Trend (bar_labels, bar_values) ---
    # This section is now fully adaptive to the start_date and end_date of the chosen period.
    bar_labels, bar_values = [], []

    # Calculate the number of full months (or partial if current month is not complete)
    # from start_date to end_date.
    current_iterator_date = start_date.replace(day=1) # Start from the first day of the start_date's month

    while current_iterator_date <= end_date:
        month_label = current_iterator_date.strftime("%b %y") # e.g., Jan 24, Feb 24
        
        # Determine the end of the current iterating month, but don't exceed end_date
        # This is crucial for monthly views where end_date might be today.
        month_end_date = current_iterator_date.replace(day=calendar.monthrange(current_iterator_date.year, current_iterator_date.month)[1])
        
        # If the end_date is within the current iterating month, cap the month_end_date at end_date
        if month_end_date > end_date:
            month_end_date = end_date

        # Filter expenses for this specific month range (or partial month if it's the end_date month)
        monthly_exp = expenses_for_period.filter(
            date__gte=current_iterator_date,
            date__lte=month_end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
        
        bar_labels.append(month_label)
        bar_values.append(float(monthly_exp)) 
        
        current_iterator_date += relativedelta(months=1) # Move to the first day of the next month


    # --- Monthly growth % ---
    monthly_growth = []
    if len(bar_values) > 1:
        for i in range(1, len(bar_values)):
            prev = bar_values[i-1] 
            current = bar_values[i] 
            
            if prev == 0.0: 
                growth = 0.0 if current == 0.0 else 100.0 
            else:
                growth = ((current - prev) / prev) * 100.0 
            
            monthly_growth.append(round(growth, 2)) 


    # --- Category-wise spending summary ---
    category_data = expenses_for_period.values('category').annotate(total=Sum('amount')).order_by('-total')
    category_list = list(category_data) 

    category_labels = [entry['category'] for entry in category_list]
    category_totals = [float(entry['total']) for entry in category_list]
    
    category_percentages = []
    for entry in category_list:
        if total_expense > Decimal('0.0'): 
            percentage = (entry['total'] / total_expense) * Decimal('100.0') 
        else:
            percentage = Decimal('0.0')
        category_percentages.append(round(float(percentage), 2)) 

    highest = category_list[0] if category_list else {'category': 'N/A', 'total': Decimal('0.0')}
    lowest = category_list[-1] if len(category_list) > 1 else highest 

    # --- Budget vs actual ---
    budget_comparison = []
    budget_limits = BudgetLimit.objects.filter(user=user, frequency='monthly')
    
    for limit in budget_limits:
        actual = expenses_for_period.filter(category=limit.category).aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
        
        percentage_used = Decimal('0.0') 
        if limit.limit > Decimal('0.0'): 
            percentage_used = (actual / limit.limit) * Decimal('100.0') 
        
        budget_comparison.append({
            'category': limit.category,
            'limit': float(limit.limit), 
            'actual': float(actual),     
            'percentage_used': round(float(percentage_used), 2),
        })

    # --- Frequency of entries per month ---
    avg_frequency = 0.0
    # Determine the number of months in the analysis period for frequency calculation
    # This logic is similar to `num_months_in_period` for bar chart, covering the full range
    num_analysis_months = ((end_date.year - start_date.year) * 12 + end_date.month - start_date.month) + 1
    num_analysis_months = max(num_analysis_months, 1)

    if num_analysis_months > 0:
        total_entries = expenses_for_period.aggregate(count=Count('id'))['count'] or 0
        avg_frequency = float(total_entries) / num_analysis_months 
    
    # --- Spending by weekday ---
    weekday_data = [Decimal('0.0')] * 7 
    for exp in expenses_for_period: # Use expenses_for_period
        weekday_data[exp.date.weekday()] += exp.amount 
    weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    weekday_data_output = [float(amount) for amount in weekday_data]

    # --- Spending by Day of Month - only for monthly period ---
    dom_data, dom_labels = [], []
    if period == 'monthly':
        # For 'monthly' period, dom_data should cover days from 1st to today
        current_day_of_month = today.day
        dom_data = [Decimal('0.0')] * current_day_of_month 
        dom_labels = list(range(1, current_day_of_month + 1))
        
        # Filter expenses only for the current month within the already period-filtered expenses
        current_month_expenses_for_dom = expenses_for_period.filter(
            date__year=today.year,
            date__month=today.month
        )
        for exp in current_month_expenses_for_dom:
            day = exp.date.day
            if 1 <= day <= current_day_of_month: 
                dom_data[day - 1] += exp.amount 
    
    dom_data_output = [float(amount) for amount in dom_data]


    return {
        'total_expense': round(float(total_expense), 2),
        'bar_labels': bar_labels,
        'bar_values': bar_values, 
        'monthly_growth': monthly_growth, 
        'category_labels': category_labels,
        'category_totals': category_totals, 
        'category_percentages': category_percentages, 
        'budget_comparison': budget_comparison, 
        'highest_category': {
            'category': highest['category'],
            'total': float(highest['total']), 
        },
        'lowest_category': {
            'category': lowest['category'],
            'total': float(lowest['total']), 
        },
        'avg_entry_frequency': round(avg_frequency, 2),
        'weekday_labels': weekday_labels,
        'weekday_data': weekday_data_output, 
        'dom_labels': dom_labels,
        'dom_data': dom_data_output, 
    }



def generate_detailed_expense_summary(analysis_data):
    total_expense = analysis_data['total_expense']
    highest_category = analysis_data['highest_category']
    lowest_category = analysis_data['lowest_category']
    avg_entry_frequency = analysis_data['avg_entry_frequency']
    budget_comparison = analysis_data['budget_comparison']
    bar_labels = analysis_data['bar_labels']
    bar_values = analysis_data['bar_values']

    text_summary = "EXPENSE FINANCIAL OVERVIEW\n\n"

    text_summary += "1. TOTAL EXPENSE:\n"
    text_summary += f"   The total expense during the selected period is Rs.{total_expense:.2f}. " \
                    "This includes all recorded spending, giving you a comprehensive view of your outflows.\n\n"

    if highest_category:
        text_summary += "2. HIGHEST SPENDING CATEGORY:\n"
        text_summary += f"   You spent the most in '{highest_category['category']}', with a total of Rs.{highest_category['total']:.2f}. " \
                        "This helps identify areas of significant expenditure and potential overspending.\n\n"
    else:
        text_summary += "2. HIGHEST SPENDING CATEGORY:\n   No expense categories were recorded.\n\n"

    if lowest_category and lowest_category != highest_category:
        text_summary += "3. LOWEST SPENDING CATEGORY:\n"
        text_summary += f"   The least was spent in '{lowest_category['category']}', amounting to Rs.{lowest_category['total']:.2f}. " \
                        "This can help you understand underutilized areas or potentially controlled spending.\n\n"

    text_summary += "4. AVERAGE MONTHLY EXPENSE ENTRY FREQUENCY:\n"
    text_summary += f"   On average, you recorded expense entries {avg_entry_frequency:.1f} times per month. " \
                    "This reflects your expense logging habits and the regularity of spending events.\n\n"

    text_summary += "5. MONTHLY EXPENSE TREND:\n"
    text_summary += "   Here's a breakdown of monthly expenses recorded over the selected period:\n"
    for label, value in zip(bar_labels, bar_values):
        text_summary += f"     - {label}: Rs.{value:.2f}\n"
    text_summary += "\n"

    if budget_comparison:
        text_summary += "6. BUDGET VS ACTUAL SPENDING:\n"
        for item in budget_comparison:
            text_summary += f"   Category: {item['category']} — Budget: Rs.{item['limit']:.2f}, " \
                            f"Actual: Rs.{item['actual']:.2f}, Used: {item['percentage_used']:.2f}%\n"
        text_summary += "\n"
    else:
        text_summary += "6. BUDGET VS ACTUAL SPENDING:\n   No budget limits were set for this period.\n\n"

    # Final paragraph - not in uppercase
    text_summary += ("  - This detailed breakdown helps you understand not only how much you spend, \n"
                     "but also where, how consistently, and how it aligns with your financial planning. \n"
                     "These insights are essential for improving budgeting, identifying cost leaks, and achieving savings goals.\n")

    return text_summary




# Assuming you have an Investment model like this:
# from django.db import models
# class Investment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#     # Add other fields like 'type', 'asset_name' etc.

# For now, I'll add a placeholder query for Investment.
# Make sure to import this model if you create it.
# from .models import Investment # If you have an Investment model

from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
import calendar
from django.utils import timezone
from .models import IncomeTracker, Expense, BudgetLimit, UserProfile # Import UserProfile
from decimal import Decimal

def get_combined_financial_analysis(user, period='monthly', custom_start=None, custom_end=None):
    today = timezone.now().date()
    
    start_date = today 
    end_date = today   
    
    income_qs = IncomeTracker.objects.none() 
    expense_qs = Expense.objects.none()

    if period == 'overall':
        earliest_income_date = IncomeTracker.objects.filter(user=user).order_by('date').first()
        earliest_expense_date = Expense.objects.filter(user=user).order_by('date').first()
        
        # Consider earliest investment date too if you have an Investment model
        # earliest_investment_date = Investment.objects.filter(user=user).order_by('date').first()

        all_dates = []
        if earliest_income_date: all_dates.append(earliest_income_date.date)
        if earliest_expense_date: all_dates.append(earliest_expense_date.date)
        # if earliest_investment_date: all_dates.append(earliest_investment_date.date) # If using Investment model

        start_date = min(all_dates) if all_dates else today
        end_date = today

    elif period == 'annual':
        start_date = today.replace(month=1, day=1) 
        end_date = today

    elif period == 'monthly':
        start_date = today.replace(day=1) 
        end_date = today

    elif period == 'custom' and custom_start and custom_end:
        start_date = custom_start
        end_date = custom_end

    else:
        start_date = today.replace(month=1, day=1) 
        end_date = today
    
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    income_qs = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
    expense_qs = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

    # --- Fetch Investment for the period ---
    # This is the crucial part. If you have an Investment model, filter and sum.
    # If UserProfile has a specific field for *period-specific* investment, use that.
    
    # Placeholder: Let's assume for now, UserProfile has an 'actual_investment_for_period' field
    # that is either updated by another process, or you intend to just use a total value.
    # This is less dynamic for period-based analysis.

    # BEST APPROACH: Use a dedicated Investment model similar to IncomeTracker/Expense
    actual_investment = Decimal('0.0')
    try:
        # Assuming you have an 'Investment' model defined
        # from .models import Investment (make sure to import this)
        # actual_investment = Investment.objects.filter(user=user, date__gte=start_date, date__lte=end_date).aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
        
        # If UserProfile has a static 'total_invested_overall' and you want to use it regardless of period
        # This will be less precise for short periods but fulfills the "UserProfile model" requirement.
        user_profile = UserProfile.objects.get(user=user)
        # Assuming UserProfile has a field like 'total_invested_amount'
        actual_investment = user_profile.total_invested_amount if hasattr(user_profile, 'total_invested_amount') else Decimal('0.0')

    except UserProfile.DoesNotExist:
        actual_investment = Decimal('0.0')
    except Exception as e:
        # Log the error if the field doesn't exist or there's another issue
        print(f"Error fetching investment from UserProfile: {e}")
        actual_investment = Decimal('0.0')

    # Now total_income and total_expense are for the period
    total_income = income_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
    total_expense = expense_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
    
    if total_expense > 0:
        income_expense_ratio = round(total_income / total_expense, 2)
    elif total_income > 0 and total_expense == 0:
        income_expense_ratio = float('inf') 
    else:
        income_expense_ratio = Decimal('0.0') 

    # --- Monthly Cash Flow ---
    monthly_flow = {}
    current_month_iterator = start_date.replace(day=1) 

    while current_month_iterator <= end_date:
        month_label = current_month_iterator.strftime("%b %y")
        month_end_date = current_month_iterator.replace(day=calendar.monthrange(current_month_iterator.year, current_month_iterator.month)[1])
        if month_end_date > end_date:
            month_end_date = end_date

        current_month_income = IncomeTracker.objects.filter(
            user=user, date__gte=current_month_iterator, date__lte=month_end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
        current_month_expense = Expense.objects.filter(
            user=user, date__gte=current_month_iterator, date__lte=month_end_date
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 

        monthly_flow[month_label] = { # Changed key to month_label for consistency
            "income": float(current_month_income), 
            "expense": float(current_month_expense), 
            "net_flow": float(current_month_income - current_month_expense) 
        }
        current_month_iterator += relativedelta(months=1)

    # --- Annual Cash Flow for last 5 years (independent of period) ---
    annual_flow = {}
    current_year = today.year
    for y in range(current_year - 4, current_year + 1):
        year_start = datetime(y, 1, 1).date()
        year_end = datetime(y, 12, 31).date()

        annual_income_sum = IncomeTracker.objects.filter(
            user=user, date__gte=year_start, date__lte=year_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
        annual_expense_sum = Expense.objects.filter(
            user=user, date__gte=year_start, date__lte=year_end
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 

        annual_flow[str(y)] = {
            "income": float(annual_income_sum), 
            "expense": float(annual_expense_sum), 
            "net_flow": float(annual_income_sum - annual_expense_sum) 
        }

    # --- Budget vs Actual Category-wise ---
    category_analysis = []
    # Filter expenses for the specific period determined at the start
    expense_categories = set(expense_qs.values_list('category', flat=True)) # Use expense_qs filtered by period
    budget_categories = set(BudgetLimit.objects.filter(user=user, frequency='monthly').values_list('category', flat=True))
    
    all_unique_categories = sorted(list(expense_categories.union(budget_categories)))

    for cat in all_unique_categories:
        budget_obj = BudgetLimit.objects.filter(user=user, category=cat, frequency='monthly').first()
        budget_limit = budget_obj.limit if budget_obj else Decimal('0.0') 
        
        # Use expense_qs for actual spending specific to the chosen period
        actual = expense_qs.filter(category=cat).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
        remaining = max(Decimal('0.0'), budget_limit - actual) 
        
        percentage_used = Decimal('0.0') 
        if budget_limit > 0:
            percentage_used = (actual / budget_limit) * Decimal('100.0') 
        
        over_budget = Decimal('0.0') 
        if actual > budget_limit:
            over_budget = actual - budget_limit 

        category_analysis.append({
            "category": cat,
            "budget": float(budget_limit), 
            "actual": float(actual),       
            "remaining": float(remaining), 
            "percentage_used": round(float(percentage_used), 2), 
            "over_budget": float(over_budget) 
        })

    # --- Budget Accuracy Score ---
    accuracy_scores = []
    for item in category_analysis:
        budget = Decimal(str(item["budget"])) 
        actual = Decimal(str(item["actual"])) 

        score = Decimal('0.0') 
        if budget > 0:
            score = max(Decimal('0.0'), Decimal('100.0') - abs((actual - budget) / budget) * Decimal('100.0'))
            accuracy_scores.append(float(score)) 
        elif budget == 0 and actual == 0:
            accuracy_scores.append(100.0) 
    
    avg_accuracy = round(sum(accuracy_scores) / len(accuracy_scores), 2) if accuracy_scores else 0.0

    # --- Ideal vs Actual Spend-Save-Invest Ratio ---
    ideal_ratio = {"spend": 50, "save": 30, "invest": 20} 
    actual_spend_percent = Decimal('0.0') 
    actual_save_percent = Decimal('0.0') 
    existing_investments = Decimal('0.0') 

    # Calculate actual percentages based on period's total income, expense, and now investment
    total_spend_save_invest_base = total_expense + actual_investment # Sum up what was spent and invested
    
    # How much is 'saved'? This is tricky without a dedicated savings tracker.
    # Often, "saving" is implicitly what's left after spending and investing from income.
    # If total_income is the base, then:
    # Savings = total_income - total_expense - actual_investment
    
    actual_savings = Decimal('0.0')
    if total_income > Decimal('0.0'):
        actual_savings = max(Decimal('0.0'), total_income - total_expense - actual_investment)
        
        # Calculate percentages based on total_income
        actual_spend_percent = (total_expense / total_income) * Decimal('100.0')
        actual_save_percent = (actual_savings / total_income) * Decimal('100.0')
        actual_invest_percent = (actual_investment / total_income) * Decimal('100.0')
    
    # Ensure percentages sum up to 100% (or very close) if based on income
    # Due to floating point (even with Decimal), there might be slight discrepancies.
    # You might want to normalize them if they don't exactly sum to 100 due to rounding
    # For now, we'll sum and let the rounding happen.
    
    actual_ratio = {
        "spend": round(float(actual_spend_percent), 2), 
        "save": round(float(actual_save_percent), 2),   
        "invest": round(float(actual_invest_percent), 2), 
    }

    # --- Final result ---
    result = {
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "income_expense_ratio": float(income_expense_ratio) if isinstance(income_expense_ratio, Decimal) else income_expense_ratio, 
        "budget_accuracy_score": float(avg_accuracy),
        "ideal_vs_actual_ratio": {
            "ideal": ideal_ratio,
            "actual": actual_ratio
        },
        "budget_vs_actual": category_analysis, 
        "monthly_cash_flow": monthly_flow, 
        "annual_cash_flow": annual_flow,   
    }

    return result



def generate_detailed_combined_summary(data):
    summary = []

    total_income = data.get("total_income", 0)
    total_expense = data.get("total_expense", 0)
    income_expense_ratio = data.get("income_expense_ratio", '∞')
    budget_score = data.get("budget_accuracy_score", None)
    ideal_ratio = data.get("ideal_vs_actual_ratio", {}).get("ideal", {})
    actual_ratio = data.get("ideal_vs_actual_ratio", {}).get("actual", {})
    category_analysis = data.get("budget_vs_actual", [])
    monthly_flow = data.get("monthly_cash_flow", {})
    annual_flow = data.get("annual_cash_flow", {})

    text_summary = "COMBINED FINANCIAL OVERVIEW\n\n"

    if total_income > 0:
        text_summary += f"1. TOTAL INCOME AND EXPENSES:\n"
        text_summary += f"   You have earned a total of Rs.{total_income:,.2f} during this period, " \
                        f"while your total expenses amounted to Rs.{total_expense:,.2f}.\n\n"

        if total_expense > 0:
            text_summary += f"2. INCOME-TO-EXPENSE RATIO:\n"
            text_summary += f"   This gives you an income-to-expense ratio of {income_expense_ratio}, " \
                            "indicating how well your income covers your expenses.\n"
            if income_expense_ratio == '∞':
                text_summary += "   Since your expenses are zero, the income-expense ratio is infinite.\n\n"
            elif income_expense_ratio > 1:
                text_summary += "   This is a positive sign, showing that your income exceeds your expenses " \
                                "and you are able to save money.\n\n"
            elif income_expense_ratio == 1:
                text_summary += "   You are spending exactly what you earn, so consider finding ways to save more.\n\n"
            else:
                text_summary += "   You are spending more than your income, which can be financially risky.\n\n"
        else:
            text_summary += "2. EXPENSES:\n"
            text_summary += "   Your expenses are zero, which may mean incomplete data or that you saved all your income.\n\n"
    else:
        text_summary += "1. INCOME DATA:\n"
        text_summary += "   No income data was recorded for this period.\n\n"

    if budget_score is not None:
        text_summary += "3. BUDGET ACCURACY SCORE:\n"
        text_summary += f"   Your average budget accuracy score is {budget_score:.2f}, " \
                        "indicating how closely you followed your planned budget.\n"
        if budget_score >= 80:
            text_summary += "   This is great — your spending stayed well within your budget.\n\n"
        elif budget_score >= 50:
            text_summary += "   There's room for improvement in sticking to your budget.\n\n"
        else:
            text_summary += "   Your spending often exceeded your budget, so more control is needed.\n\n"

    text_summary += "4. IDEAL VS ACTUAL SPEND-SAVE-INVEST RATIOS:\n"
    text_summary += f"   Financial experts recommend allocating approximately " \
                    f"{ideal_ratio.get('spend', 50)}% to spending, " \
                    f"{ideal_ratio.get('save', 30)}% to savings, and " \
                    f"{ideal_ratio.get('invest', 20)}% to investments from your income.\n"
    text_summary += f"   Based on your actual data, you spend {actual_ratio.get('spend', 0)}%, save {actual_ratio.get('save', 0)}%, " \
                    f"and invest {actual_ratio.get('invest', 0)}% of your income.\n"
    if actual_ratio.get('invest', 0) == 0:
        text_summary += "   Currently, your investment portion is zero, which might be something to consider for long-term growth.\n\n"
    else:
        text_summary += "\n"

    text_summary += "5. CATEGORY-WISE BUDGET VS ACTUAL SPENDING:\n"
    if category_analysis:
        for item in category_analysis:
            cat = item['category']
            budget = item['budget']
            actual = item['actual']
            remaining = item['remaining']
            text_summary += f"   - {cat}: Budgeted Rs.{budget:,.2f}, Spent Rs.{actual:,.2f}.\n"
            if actual > budget:
                text_summary += f"     You overspent by Rs.{actual - budget:,.2f}. It's advisable to keep this in check.\n"
            elif remaining > 0:
                text_summary += f"     You have Rs.{remaining:,.2f} remaining in your budget, which is good.\n"
            else:
                text_summary += f"     You have managed your budget perfectly in this category.\n"
        text_summary += "\n"
    else:
        text_summary += "   No budget or expense data is available for any category.\n\n"

    if monthly_flow:
        text_summary += "6. MONTHLY INCOME AND EXPENSES SUMMARY (LAST 12 MONTHS):\n"
        for month, values in monthly_flow.items():
            income = values['income']
            expense = values['expense']
            balance = income - expense
            text_summary += f"   - {month}: Income Rs.{income:,.2f}, Expenses Rs.{expense:,.2f}.\n"
            if balance > 0:
                text_summary += f"     You saved Rs.{balance:,.2f} this month, which is positive.\n"
            elif balance == 0:
                text_summary += "     You broke even this month, spending exactly what you earned.\n"
            else:
                text_summary += f"     You overspent by Rs.{-balance:,.2f} this month. Consider budgeting better.\n"
        text_summary += "\n"
    elif annual_flow:
        text_summary += "6. ANNUAL INCOME AND EXPENSES SUMMARY (LAST 5 YEARS):\n"
        for year, values in annual_flow.items():
            income = values['income']
            expense = values['expense']
            balance = income - expense
            text_summary += f"   - {year}: Income Rs.{income:,.2f}, Expenses Rs.{expense:,.2f}.\n"
            if balance > 0:
                text_summary += f"     You saved Rs.{balance:,.2f} this year, which is encouraging.\n"
            elif balance == 0:
                text_summary += "     You broke even this year, with income matching expenses.\n"
            else:
                text_summary += f"     You overspent by Rs.{-balance:,.2f} this year. Monitoring spending is recommended.\n"
        text_summary += "\n"

    text_summary += ("- This comprehensive summary helps you see your overall financial health, " 
                     "showing income, expenses, budgeting performance, and how your spending aligns with ideal financial planning. "
                     "Use these insights to improve savings, manage budgets, and plan investments wisely.\n")

    return text_summary






def generate_closing_message():
    closing_text = (
        "Dear Sir,\n\n"
        "Thank you sincerely for trusting us to accompany you on your financial journey. "
        "Your commitment to understanding your finances and striving for better management is truly inspiring. "
        "We recognize the effort and dedication it takes to track your expenses and plan your future wisely. "
        "Remember, every step you take brings you closer to your financial goals and greater freedom. "
        "We are honored to support you in this journey and are always here to guide you towards smarter, more confident decisions. "
        "Stay positive, keep learning, and never hesitate to reach out for assistance. Together, let's create a secure and prosperous tomorrow for you and your loved ones.\n\n"
        "Thank you once again for being a valued part of our community. Wishing you success, happiness, and peace in all your financial endeavors!"
    )
    return closing_text





























# # finance_advisor/dashboard/models.py (or wherever your models are)

# from django.db import models
# from django.contrib.auth import get_user_model # For linking to your User model
# from decimal import Decimal # Import Decimal

# User = get_user_model() # Get the active user model

# class Investment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2) # Use Decimal for money
#     date = models.DateField()
#     # Add other fields as needed, e.g., source, type, asset_name
#     description = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.amount} on {self.date}"

#     class Meta:
#         ordering = ['-date'] # Order by latest investment first


# # this function use after the crate seprate model for investment


# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# from django.db.models import Sum
# import calendar
# from django.utils import timezone
# # Make sure to import your new Investment model here!
# from .models import IncomeTracker, Expense, BudgetLimit, UserProfile, Investment 
# from decimal import Decimal

# def get_combined_financial_analysis(user, period='monthly', custom_start=None, custom_end=None):
#     today = timezone.now().date()
    
#     start_date = today 
#     end_date = today   
    
#     income_qs = IncomeTracker.objects.none() 
#     expense_qs = Expense.objects.none()
#     investment_qs = Investment.objects.none() # Initialize for Investment

#     # --- Determine date range based on period ---
#     if period == 'overall':
#         earliest_income_date = IncomeTracker.objects.filter(user=user).order_by('date').first()
#         earliest_expense_date = Expense.objects.filter(user=user).order_by('date').first()
#         earliest_investment_date = Investment.objects.filter(user=user).order_by('date').first() # Get earliest investment date

#         all_dates = []
#         if earliest_income_date: all_dates.append(earliest_income_date.date)
#         if earliest_expense_date: all_dates.append(earliest_expense_date.date)
#         if earliest_investment_date: all_dates.append(earliest_investment_date.date) # Include investment date

#         start_date = min(all_dates) if all_dates else today
#         end_date = today

#     elif period == 'annual':
#         start_date = today.replace(month=1, day=1) 
#         end_date = today

#     elif period == 'monthly':
#         start_date = today.replace(day=1) 
#         end_date = today

#     elif period == 'custom' and custom_start and custom_end:
#         start_date = custom_start
#         end_date = custom_end

#     else:
#         start_date = today.replace(month=1, day=1) 
#         end_date = today
    
#     if start_date > end_date:
#         start_date, end_date = end_date, start_date

#     income_qs = IncomeTracker.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
#     expense_qs = Expense.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
#     # Filter investments for the specific period
#     investment_qs = Investment.objects.filter(user=user, date__gte=start_date, date__lte=end_date)

#     # --- Total Income, Expense, and Investment for the period ---
#     total_income = income_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
#     total_expense = expense_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
#     # Sum investments for the period
#     actual_investment = investment_qs.aggregate(total=Sum('amount'))['total'] or Decimal('0.0')
    
#     if total_expense > 0:
#         income_expense_ratio = round(total_income / total_expense, 2)
#     elif total_income > 0 and total_expense == 0:
#         income_expense_ratio = float('inf') 
#     else:
#         income_expense_ratio = Decimal('0.0') 

#     # --- Monthly Cash Flow ---
#     monthly_flow = {}
#     current_month_iterator = start_date.replace(day=1) 

#     while current_month_iterator <= end_date:
#         month_label = current_month_iterator.strftime("%b %y")
#         month_end_date = current_month_iterator.replace(day=calendar.monthrange(current_month_iterator.year, current_month_iterator.month)[1])
#         if month_end_date > end_date:
#             month_end_date = end_date

#         current_month_income = IncomeTracker.objects.filter(
#             user=user, date__gte=current_month_iterator, date__lte=month_end_date
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
#         current_month_expense = Expense.objects.filter(
#             user=user, date__gte=current_month_iterator, date__lte=month_end_date
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 

#         monthly_flow[month_label] = { 
#             "income": float(current_month_income), 
#             "expense": float(current_month_expense), 
#             "net_flow": float(current_month_income - current_month_expense) 
#         }
#         current_month_iterator += relativedelta(months=1)

#     # --- Annual Cash Flow for last 5 years (independent of period) ---
#     annual_flow = {}
#     current_year = today.year
#     for y in range(current_year - 4, current_year + 1):
#         year_start = datetime(y, 1, 1).date()
#         year_end = datetime(y, 12, 31).date()

#         annual_income_sum = IncomeTracker.objects.filter(
#             user=user, date__gte=year_start, date__lte=year_end
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
#         annual_expense_sum = Expense.objects.filter(
#             user=user, date__gte=year_start, date__lte=year_end
#         ).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 

#         annual_flow[str(y)] = {
#             "income": float(annual_income_sum), 
#             "expense": float(annual_expense_sum), 
#             "net_flow": float(annual_income_sum - annual_expense_sum) 
#         }

#     # --- Budget vs Actual Category-wise ---
#     category_analysis = []
#     expense_categories = set(expense_qs.values_list('category', flat=True)) 
#     budget_categories = set(BudgetLimit.objects.filter(user=user, frequency='monthly').values_list('category', flat=True))
    
#     all_unique_categories = sorted(list(expense_categories.union(budget_categories)))

#     for cat in all_unique_categories:
#         budget_obj = BudgetLimit.objects.filter(user=user, category=cat, frequency='monthly').first()
#         budget_limit = budget_obj.limit if budget_obj else Decimal('0.0') 
        
#         actual = expense_qs.filter(category=cat).aggregate(total=Sum('amount'))['total'] or Decimal('0.0') 
        
#         remaining = max(Decimal('0.0'), budget_limit - actual) 
        
#         percentage_used = Decimal('0.0') 
#         if budget_limit > 0:
#             percentage_used = (actual / budget_limit) * Decimal('100.0') 
        
#         over_budget = Decimal('0.0') 
#         if actual > budget_limit:
#             over_budget = actual - budget_limit 

#         category_analysis.append({
#             "category": cat,
#             "budget": float(budget_limit), 
#             "actual": float(actual),       
#             "remaining": float(remaining), 
#             "percentage_used": round(float(percentage_used), 2), 
#             "over_budget": float(over_budget) 
#         })

#     # --- Budget Accuracy Score ---
#     accuracy_scores = []
#     for item in category_analysis:
#         budget = Decimal(str(item["budget"])) 
#         actual = Decimal(str(item["actual"])) 

#         score = Decimal('0.0') 
#         if budget > 0:
#             score = max(Decimal('0.0'), Decimal('100.0') - abs((actual - budget) / budget) * Decimal('100.0'))
#             accuracy_scores.append(float(score)) 
#         elif budget == 0 and actual == 0:
#             accuracy_scores.append(100.0) 
    
#     avg_accuracy = round(sum(accuracy_scores) / len(accuracy_scores), 2) if accuracy_scores else 0.0

#     # --- Ideal vs Actual Spend-Save-Invest Ratio ---
#     ideal_ratio = {"spend": 50, "save": 30, "invest": 20} 
#     actual_spend_percent = Decimal('0.0') 
#     actual_save_percent = Decimal('0.0') 
#     actual_invest_percent = Decimal('0.0') 

#     if total_income > Decimal('0.0'): 
#         # Calculate actual savings: what's left after expenses and investments from income
#         actual_savings = max(Decimal('0.0'), total_income - total_expense - actual_investment)
        
#         actual_spend_percent = (total_expense / total_income) * Decimal('100.0')
#         actual_save_percent = (actual_savings / total_income) * Decimal('100.0')
#         actual_invest_percent = (actual_investment / total_income) * Decimal('100.0')
    
#     actual_ratio = {
#         "spend": round(float(actual_spend_percent), 2), 
#         "save": round(float(actual_save_percent), 2),   
#         "invest": round(float(actual_invest_percent), 2), 
#     }

#     # --- Final result ---
#     result = {
#         "total_income": float(total_income),
#         "total_expense": float(total_expense),
#         "income_expense_ratio": float(income_expense_ratio) if isinstance(income_expense_ratio, Decimal) else income_expense_ratio, 
#         "budget_accuracy_score": float(avg_accuracy),
#         "ideal_vs_actual_ratio": {
#             "ideal": ideal_ratio,
#             "actual": actual_ratio
#         },
#         "budget_vs_actual": category_analysis, 
#         "monthly_cash_flow": monthly_flow, 
#         "annual_cash_flow": annual_flow,   
#     }

#     return result