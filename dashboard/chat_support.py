from dashboard.models import UserProfile
from typing import Optional
from django.utils.timesince import timesince
import random
from datetime import datetime



def get_greeting(user, entities=None) -> str:
    """
    Generates a personalized greeting for the user, potentially
    considering the time of day and user preferences.

    Args:
        user: An object with a 'first_name' attribute (e.g., a user object from a database).
              If 'first_name' is not available, 'there' will be used as a fallback.
        entities: (Optional) A dictionary of entities that could provide
                  context for a more specific greeting (e.g., time of day).

    Returns:
        A personalized greeting string.
    """

    # Determine the name to use in the greeting
    name = getattr(user, 'first_name', '').strip()
    if not name:
        name = 'there'

    # Get the current hour for time-based greetings
    current_hour = datetime.now().hour

    time_based_greetings = {
        (5, 12): "Good morning, {name}!",    # 5 AM to 11:59 AM
        (12, 18): "Good afternoon, {name}!", # 12 PM to 5:59 PM
        (18, 24): "Good evening, {name}!",   # 6 PM to 11:59 PM
        (0, 5): "Hello {name}!"              # 12 AM to 4:59 AM (fallback or night owls)
    }

    # Determine time-based greeting
    selected_time_greeting = None
    for (start, end), greeting_text in time_based_greetings.items():
        if start <= current_hour < end:
            selected_time_greeting = greeting_text
            break
    
    # Fallback to general greetings if no specific time-based greeting is found
    general_greetings = [
        "👋 Hello {name}, great to see you!",
        "😊 Hi {name}, how can I help you today?",
        "Hey {name}! 👋 What would you like to do today?",
        "Hiya {name}! Ready to manage your finances?",
        "Hello {name}! Hope you're having a great day!"
    ]

    if selected_time_greeting:
        greetings_to_choose_from = [selected_time_greeting] + general_greetings
    else:
        greetings_to_choose_from = general_greetings

    # Add entity-based greetings if applicable (example placeholder)
    if entities and "topic" in entities:
        if entities["topic"] == "finance":
            greetings_to_choose_from.append("Welcome back, {name}! Ready to check your finances?")
        elif entities["topic"] == "support":
            greetings_to_choose_from.append("Hi {name}, how can I assist you with support today?")

    # Select a random greeting from the available options
    greeting = random.choice(greetings_to_choose_from).format(name=name)
    return greeting


# ---------------------- Utility Functions ---------------------- #

def get_user_profile(user) -> Optional[UserProfile]:
    """Safely get the UserProfile for the given user."""
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        return None

def format_currency(amount: float) -> str:
    """Format currency with commas and show decimals only if needed."""
    if amount == int(amount):
        return f"₹{int(amount):,}"
    else:
        return f"₹{amount:,.2f}"

def format_datetime(dt):
    """Readable datetime format."""
    return dt.strftime("%d %B %Y, %I:%M %p")

def get_profile_field_message(user, field_name: str, field_display_name: str, formatter=None, entities=None) -> str:
    """
    Generic handler to get a field from UserProfile and format response.
    """
    profile = get_user_profile(user)
    if not profile:
        return "⚠️ Profile not found. Please complete your profile in the settings section."

    value = getattr(profile, field_name, None)
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"ℹ️ Your {field_display_name.lower()} is currently not set in your profile."

    if formatter:
        try:
            value = formatter(value)
        except Exception:
            pass  # Fallback to raw value

    return f"✅ Your {field_display_name.lower()} is: {value}"

# ---------------------- Profile Data Handlers ---------------------- #

def get_user_mobile(user, entities=None) -> str:
    return get_profile_field_message(user, "mobile", "Mobile Number", entities=entities)

def get_user_dob(user, entities=None) -> str:
    return get_profile_field_message(user, "dob", "Date of Birth", formatter=format_datetime, entities=entities)

def get_user_gender(user, entities=None) -> str:
    return get_profile_field_message(user, "gender", "Gender", entities=entities)

def get_user_savings(user, entities=None) -> str:
    return get_profile_field_message(user, "savings", "Savings Amount", formatter=format_currency, entities=entities)

def get_existing_investments(user, entities=None) -> str:
    return get_profile_field_message(user, "existing_investments", "Existing Investments", formatter=format_currency, entities=entities)

def get_user_risk_appetite(user, entities=None) -> str:
    return get_profile_field_message(user, "risk_appetite", "Risk Appetite", entities=entities)

def get_investment_goals(user, entities=None) -> str:
    return get_profile_field_message(user, "investment_goals", "Investment Goal", entities=entities)

def get_preferred_investments(user, entities=None) -> str:
    return get_profile_field_message(user, "preferred_investments", "Preferred Investments", entities=entities)

# ---------------------- Summary & Timestamps ---------------------- #

def get_profile_summary(user, entities=None) -> str:
    profile = get_user_profile(user)
    if not profile:
        return "⚠️ Your profile is incomplete. Please update it from the settings."

    summary = f"""
🧾 Profile Summary:
• 📞 Mobile: {profile.mobile or "Not set"}
• 🎂 DOB: {format_datetime(profile.dob) if profile.dob else "Not set"}
• 🚻 Gender: {profile.gender or "Not set"}
• 💰 Savings: {format_currency(profile.savings) if profile.savings else "Not set"}
• 📈 Existing Investments: {format_currency(profile.existing_investments) if profile.existing_investments else "Not set"}
• 📊 Risk Appetite: {profile.risk_appetite or "Not set"}
• 🎯 Investment Goals: {profile.investment_goals or "Not set"}
• 📌 Preferred Investments: {profile.preferred_investments or "Not set"}
"""
    return summary.strip()

def get_created_at(user, entities=None) -> str:
    profile = get_user_profile(user)
    if not profile:
        return "⚠️ Profile not found. Please complete your profile to view this information."

    return f"🎉 Your profile was created on {format_datetime(profile.created_at)} ({timesince(profile.created_at)} ago)."

def get_updated_at(user, entities=None) -> str:
    profile = get_user_profile(user)
    if not profile:
        return "⚠️ Profile not found. Please complete your profile to view this information."

    return f"🛠️ Your profile was last updated on {format_datetime(profile.updated_at)} ({timesince(profile.updated_at)} ago)."




def guide_update_profile(field: str = None) -> str:
    general_msg = (
        "🛠️ To update your profile details:\n"
        "1️⃣ Log into your dashboard.\n"
        "2️⃣ Navigate to Settings or Profile.\n"
        "3️⃣ Edit the fields you wish to update.\n"
        "4️⃣ Click Save to apply changes.\n\n"
        "💡 Need help with a specific field like savings or mobile? Just ask!"
    )

    guides = {
        "mobile": (
            "📱 To update your mobile number:\n"
            "1️⃣ Go to Settings > Profile.\n"
            "2️⃣ Find the Mobile Number field.\n"
            "3️⃣ Enter your new number.\n"
            "4️⃣ Tap Save.\n\n"
            "✅ Make sure it's correct to receive important updates!"
        ),
        "savings": (
            "💰 To update your savings amount:\n"
            "1️⃣ Open Profile Settings.\n"
            "2️⃣ Locate the Savings field.\n"
            "3️⃣ Enter your updated amount.\n"
            "4️⃣ Click Save to update."
        ),
        "risk_appetite": (
            "⚖️ To change your risk appetite:\n"
            "1️⃣ Go to Settings > Profile.\n"
            "2️⃣ Look for Risk Appetite.\n"
            "3️⃣ Choose your level: Low, Medium, or High.\n"
            "4️⃣ Save your preference."
        ),
        "investment_goals": (
            "🎯 To update your investment goals:\n"
            "1️⃣ Head to Profile Settings.\n"
            "2️⃣ Find the Investment Goals section.\n"
            "3️⃣ Edit your goals.\n"
            "4️⃣ Click Save to apply."
        ),
        "preferred_investments": (
            "📊 To change preferred investments:\n"
            "1️⃣ Go to Settings > Profile.\n"
            "2️⃣ Scroll to Preferred Investments.\n"
            "3️⃣ Select or unselect investment types.\n"
            "4️⃣ Hit Save to confirm."
        ),
        "dob": (
            "🎂 To update your date of birth (DOB):\n"
            "1️⃣ Navigate to Profile Settings.\n"
            "2️⃣ Edit the DOB field.\n"
            "3️⃣ Click Save to confirm.\n\n"
            "⚠️ DOB might be locked after registration in some cases."
        ),
        "gender": (
            "🚻 To change your gender info:\n"
            "1️⃣ Open Profile Settings.\n"
            "2️⃣ Choose the correct gender.\n"
            "3️⃣ Click Save to update."
        ),
        "existing_investments": (
            "📈 To update existing investments:\n"
            "1️⃣ Open your Profile Settings.\n"
            "2️⃣ Find the Investments section.\n"
            "3️⃣ Enter your current total.\n"
            "4️⃣ Click Save to record it."
        ),
    }

    if field:
        return guides.get(field.lower(), general_msg)
    return general_msg


def guide_update_mobile(user, entities=None):
    return guide_update_profile("mobile")

def guide_update_savings(user, entities=None):
    return guide_update_profile("savings")

def guide_update_risk_appetite(user, entities=None):
    return guide_update_profile("risk_appetite")

def guide_update_investment_goals(user, entities=None):
    return guide_update_profile("investment_goals")

def guide_update_preferred_investments(user, entities=None):
    return guide_update_profile("preferred_investments")

def guide_update_dob(user, entities=None):
    return guide_update_profile("dob")

def guide_update_gender(user, entities=None):
    return guide_update_profile("gender")

def guide_update_existing_investments(user, entities=None):
    return guide_update_profile("existing_investments")

def guide_delete_account(user, entities=None):
    return (
        "⚠️ Warning: Account Deletion is Permanent\n"
        "Here's how to delete your account:\n"
        "1️⃣ Go to Settings.\n"
        "2️⃣ Scroll to the bottom and click Delete Account.\n"
        "3️⃣ Verify your identity (OTP/email confirmation).\n"
        "4️⃣ Confirm deletion.\n\n"
        "❗ Please reconsider before proceeding. This action cannot be undone."
    )

def guide_view_profile(user, entities=None):
    return (
        "👤 To view your profile:\n"
        "1️⃣ Log into your account.\n"
        "2️⃣ Go to Profile or Settings.\n"
        "3️⃣ You can see your personal details like mobile, savings, goals, and more."
    )

def guide_change_password(user, entities=None):
    return (
        "🔐 To change your password:\n"
        "1️⃣ Go to Settings > Security.\n"
        "2️⃣ Enter your current password.\n"
        "3️⃣ Set a new password and confirm it.\n"
        "4️⃣ Tap Save to apply the changes.\n\n"
        "💡 Choose a strong password to keep your account safe."
    )









from datetime import date
from dateutil.relativedelta import relativedelta
from calendar import monthrange # Used for getting days in month for range calculation
from django.db.models import Sum
from .models import Expense # Assuming Expense model is correctly imported

def parse_month(month_input):
    """Accepts int or string month, returns integer month or None."""
    if isinstance(month_input, int):
        return month_input if 1 <= month_input <= 12 else None

    if isinstance(month_input, str):
        month_input = month_input.strip().lower()
        months = {
            "jan": 1, "january": 1,
            "feb": 2, "february": 2,
            "mar": 3, "march": 3,
            "apr": 4, "april": 4,
            "may": 5,
            "jun": 6, "june": 6,
            "jul": 7, "july": 7,
            "aug": 8, "august": 8,
            "sep": 9, "sept": 9, "september": 9,
            "oct": 10, "october": 10,
            "nov": 11, "november": 11,
            "dec": 12, "december": 12,
        }
        return months.get(month_input)
    return None

def get_total_expense_response(user, period=None, month=None, year=None) -> str:
    """
    Calculates and returns the total expense for a given user based on period,
    month, and year, with a detailed breakdown by category.
    """
    today = date.today()
    expenses = Expense.objects.filter(user=user)
    response_lines = []
    query_description = ""

    parsed_month = parse_month(month)
    parsed_year = int(year) if year else None

    # Determine the date range for the query
    start_date = None
    end_date = None

    if parsed_month is not None and parsed_year is not None:
        start_date = date(parsed_year, parsed_month, 1)
        # Get the last day of the month
        _, last_day = monthrange(parsed_year, parsed_month)
        end_date = date(parsed_year, parsed_month, last_day)
        query_description = f"for {start_date.strftime('%B %Y')}"
    elif parsed_month is not None:
        # If only month is provided, assume current year
        start_date = date(today.year, parsed_month, 1)
        _, last_day = monthrange(today.year, parsed_month)
        end_date = date(today.year, parsed_month, last_day)
        query_description = f"for {start_date.strftime('%B %Y')}"
    elif parsed_year is not None:
        # If only year is provided
        start_date = date(parsed_year, 1, 1)
        end_date = date(parsed_year, 12, 31)
        query_description = f"for year {parsed_year}"
    elif period == "current_month":
        start_date = date(today.year, today.month, 1)
        end_date = today # Up to current day for "so far"
        query_description = f"for {today.strftime('%B %Y')} (so far)"
    elif period == "last_month":
        last_month_date = today - relativedelta(months=1)
        start_date = date(last_month_date.year, last_month_date.month, 1)
        _, last_day = monthrange(last_month_date.year, last_month_date.month)
        end_date = date(last_month_date.year, last_month_date.month, last_day)
        query_description = f"for {last_month_date.strftime('%B %Y')}"
    elif period == "current_year":
        start_date = date(today.year, 1, 1)
        end_date = today # Up to current day for "so far"
        query_description = f"for year {today.year} (so far)"
    elif period == "all_time" or (not period and not month and not year):
        # Default to all-time if no specific period, month, or year is provided
        query_description = "overall"
    else:
        # Fallback for unrecognized period or invalid combination
        return "I couldn't understand the period you specified for expenses. Please try again with 'current month', 'last month', 'current year', a specific month (e.g., 'January' or '1'), or a year (e.g., '2023')."

    # Apply date filters
    if start_date and end_date:
        expenses = expenses.filter(date__range=(start_date, end_date))
    elif query_description == "overall": # For all_time, no specific date range filter needed
        pass
    else:
        # This case should ideally be caught by the initial `if/elif` chain
        # but as a safeguard or if no period could be determined
        return "I couldn't precisely determine the period for your expenses. Please try a simpler query like 'expenses this month' or 'expenses for January 2023'."


    total_expense = expenses.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    if not expenses.exists():
        return f"You have no recorded expenses {query_description}."

    # --- Constructing the informative response ---
    response_lines.append(f"💸 Your total expense {query_description} is ₹{total_expense:,.2f}.")

    # Add a breakdown by category
    if expenses.count() > 0:
        expense_breakdown = expenses.values('category').annotate(sum_amount=Sum('amount')).order_by('-sum_amount')

        if expense_breakdown:
            response_lines.append("\nHere's a breakdown by category:")
            for item in expense_breakdown:
                # Assuming category names should be title-cased for display
                response_lines.append(f"• {item['category'].title()}: ₹{item['sum_amount']:,.2f}")

    # Suggest next actions
    response_lines.append("\n_Need to see your budget limits? Try 'show me my budget for food'._")
    response_lines.append("_Want to add an expense? You can do that directly in the app!_")

    return "\n".join(response_lines) # Use single newline for list items, double for sections


def total_expense_handler(user, entities=None):
    """
    Handles parsing entities and calling the get_total_expense_response function.
    """
    period = None
    month = None
    year = None

    if entities:
        period = entities.get("period")
        month = entities.get("month")
        year = entities.get("year")

    return get_total_expense_response(user, period=period, month=month, year=year)


# --- Guide functions for Expenses ---

def guide_add_expense(user, entities: dict = None) -> str:
    """
    Guides the user on how to add new expense.
    """
    amount = entities.get("amount") if entities else None
    category = entities.get("category") if entities else None
    date_info = entities.get("date") if entities else None

    if amount and category and date_info:
        return (f"To add an expense of ₹{amount:,.2f} for {category.title()} on {date_info}, "
                "please go to the 'Expenses' section in your app or visit our website's expense management page. "
                "You'll find easy options to record your expense details there.")
    elif amount and category:
        return (f"To add an expense of ₹{amount:,.2f} for {category.title()}, "
                "please go to the 'Expenses' section in your app or visit our website's expense management page. "
                "You can specify the date and other details there.")
    elif amount:
        return (f"To add ₹{amount:,.2f} to your expenses, "
                "please go to the 'Expenses' section in your app or visit our website's expense management page. "
                "You can specify the category and date there.")
    else:
        return ("To add a new expense, please go to the 'Expenses' section in your app "
                "or visit our website's expense management page. There you can easily specify the amount, "
                "category, and date of your expense.")


def guide_delete_expense(user, entities: dict = None) -> str:
    """
    Guides the user on how to delete an expense entry.
    """
    amount = entities.get("amount") if entities else None
    category = entities.get("category") if entities else None
    date_info = entities.get("date") if entities else None

    if amount and category and date_info:
        return (f"To delete the expense entry of ₹{amount:,.2f} for {category.title()} on {date_info}, "
                "please navigate to the 'Expenses' section in your app or our website. "
                "You'll find options to manage and remove your existing expense records there.")
    elif amount and category:
        return (f"To delete the expense of ₹{amount:,.2f} for {category.title()}, "
                "please navigate to the 'Expenses' section in your app or our website. "
                "You can select the specific entry to remove there.")
    elif category:
        return (f"To delete expense entries for {category.title()}, "
                "please navigate to the 'Expenses' section in your app or our website. "
                "You can view and remove all entries for that category there.")
    else:
        return ("To delete an expense entry, please navigate to the 'Expenses' section in your app or our website. "
                "You'll find options to manage and remove your existing expense records there.")
    





from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import IncomeTracker, Expense, BudgetLimit # Make sure to import all necessary models

def parse_month(month_input):
    """Accepts int or string month, returns integer month or None."""
    if isinstance(month_input, int):
        return month_input if 1 <= month_input <= 12 else None

    if isinstance(month_input, str):
        month_input = month_input.strip().lower()
        months = {
            "jan": 1, "january": 1,
            "feb": 2, "february": 2,
            "mar": 3, "march": 3,
            "apr": 4, "april": 4,
            "may": 5,
            "jun": 6, "june": 6,
            "jul": 7, "july": 7,
            "aug": 8, "august": 8,
            "sep": 9, "sept": 9, "september": 9,
            "oct": 10, "october": 10,
            "nov": 11, "november": 11,
            "dec": 12, "december": 12,
        }
        return months.get(month_input)
    return None

def get_total_income_response(user, period=None, month=None, year=None, source=None) -> str:
    """
    Calculates and returns the total income for a given user based on period,
    month, year, and optionally source, with detailed breakdown.
    """
    today = date.today()
    incomes = IncomeTracker.objects.filter(user=user)
    response_lines = []
    query_description = ""
    
    parsed_month = parse_month(month)
    parsed_year = int(year) if year else None

    # Determine the date range for the query
    start_date = None
    end_date = None

    if parsed_month is not None and parsed_year is not None:
        start_date = date(parsed_year, parsed_month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        query_description = f" for {start_date.strftime('%B %Y')}"
    elif parsed_month is not None:
        start_date = date(today.year, parsed_month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        query_description = f" for {start_date.strftime('%B %Y')}"
    elif parsed_year is not None:
        start_date = date(parsed_year, 1, 1)
        end_date = date(parsed_year, 12, 31)
        query_description = f" for year {parsed_year}"
    elif period == "current_month":
        start_date = date(today.year, today.month, 1)
        end_date = today # Upto current day
        query_description = f" for {today.strftime('%B %Y')} (so far)"
    elif period == "last_month":
        last_month_date = today - relativedelta(months=1)
        start_date = date(last_month_date.year, last_month_date.month, 1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        query_description = f" for {last_month_date.strftime('%B %Y')}"
    elif period == "current_year":
        start_date = date(today.year, 1, 1)
        end_date = today # Upto current day
        query_description = f" for year {today.year} (so far)"
    elif period == "all_time" or (not period and not month and not year and not source):
        # No date filter means all time, but we won't set start/end for simplicity here
        query_description = " overall"
    else:
        return "I couldn't understand the income period or source you specified. Please try again."

    # Apply date filters
    if start_date and end_date:
        incomes = incomes.filter(date__range=(start_date, end_date))
    elif query_description == " overall": # For all_time, no specific date range filter needed
        pass
    else:
        # Fallback for complex date parsing issues or if no specific period was correctly identified
        return "I couldn't precisely determine the period for your income. Please try a simpler query like 'income this month' or 'income for January 2023'."

    # Apply source filter if provided
    source_label = ""
    if source:
        incomes = incomes.filter(source__iexact=source.strip())
        source_label = f" from {source.title()}"

    total_income = incomes.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    if not incomes.exists():
        if source:
            return f"You have no recorded income{source_label}{query_description}."
        else:
            return f"You have no recorded income{query_description}."

    response_lines.append(f"💰 Your total income{source_label}{query_description} is ₹{total_income:,.2f}.")

    # Add a breakdown by source if it's not already filtered by source and there are multiple incomes
    if not source and incomes.count() > 0: # Only show breakdown if not already filtered by a single source
        # Get distinct sources and their sums for the filtered incomes
        income_breakdown = incomes.values('source').annotate(sum_amount=Sum('amount')).order_by('-sum_amount')

        if income_breakdown: # Only add breakdown if there's actual data
            response_lines.append("\nHere's a breakdown by source:")
            for item in income_breakdown:
                response_lines.append(f"• {item['source'].title()}: ₹{item['sum_amount']:,.2f}")
    
    # Suggest next actions (optional, but makes it more interactive)
    response_lines.append("\n_Need to see expenses? Try 'show me my expenses this month'._")
    response_lines.append("_Want to add income? I can't do that here, but you can do it from the app!_")


    return "\n".join(response_lines) # Use single newline for list items, double for sections

def total_income_handler(user, entities=None):
    """
    Handles parsing entities and calling the get_total_income_response function.
    """
    period = None
    month = None
    year = None
    source = None

    if entities:
        period = entities.get("period")        # e.g., "current_month", "current_year", "last_month", "all_time"
        month = entities.get("month")          # e.g., "jan", "january", 1
        year = entities.get("year")            # e.g., 2024
        source = entities.get("source")        # e.g., "salary", "freelance"

    return get_total_income_response(user, period=period, month=month, year=year, source=source)




# --- Guide functions for Income ---

def guide_add_income(user, entities: dict = None) -> str:
    """
    Guides the user on how to add new income.
    """
    amount = entities.get("amount") if entities else None
    source = entities.get("source") if entities else None
    date_info = entities.get("date") if entities else None # Captures if a specific date was mentioned

    if amount and source and date_info:
        return (f"To add ₹{amount:,.2f} income from {source.title()} recorded on {date_info}, "
                "please go to the 'Income' section in your app or visit our website's income management page. "
                "You'll find easy options to record your income details there.")
    elif amount and source:
        return (f"To add ₹{amount:,.2f} income from {source.title()}, "
                "please go to the 'Income' section in your app or visit our website's income management page. "
                "You can specify the date and other details there.")
    elif amount:
        return (f"To add ₹{amount:,.2f} to your income, "
                "please go to the 'Income' section in your app or visit our website's income management page. "
                "You can specify the source and date there.")
    else:
        return ("To add new income, please go to the 'Income' section in your app "
                "or visit our website's income management page. There you can easily specify the amount, "
                "source, and date of your income.")

def guide_delete_income(user, entities: dict = None) -> str:
    """
    Guides the user on how to delete an income entry.
    """
    amount = entities.get("amount") if entities else None
    source = entities.get("source") if entities else None
    date_info = entities.get("date") if entities else None

    if amount and source and date_info:
        return (f"To delete the income entry of ₹{amount:,.2f} from {source.title()} on {date_info}, "
                "please navigate to the 'Income' section in your app or our website. "
                "You'll find options to manage and remove your existing income records there.")
    elif amount and source:
        return (f"To delete income from {source.title()} amounting to ₹{amount:,.2f}, "
                "please navigate to the 'Income' section in your app or our website. "
                "You can select the specific entry to remove there.")
    elif source:
        return (f"To delete income entries from {source.title()}, "
                "please navigate to the 'Income' section in your app or our website. "
                "You can view and remove all entries from that source there.")
    else:
        return ("To delete an income entry, please navigate to the 'Income' section in your app or our website. "
                "You'll find options to manage and remove your existing income records there.")


# Existing parse_month function and guide functions from your previous code
# ... (parse_month, get_budget_limit_data, budget_limit_handler, guide_set_budget_limit, guide_delete_budget_limit) ...
# Assuming these are also in chat_support.py


from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from .models import BudgetLimit, Expense # Assuming Expense model is also available for CATEGORY_CHOICES

# --- Core Budget Data Retrieval Function ---
def get_budget_limit_data(user, category: str = None, frequency: str = None) -> str:
    """
    Retrieves and displays the budget limit for a user, optionally by category and frequency.
    If category is provided, it also shows current spending against the limit.
    """
    budgets = BudgetLimit.objects.filter(user=user)
    today = date.today()

    # Filter by category if specified
    if category:
        category_lower = category.lower()
        valid_categories = [choice[0].lower() for choice in Expense.CATEGORY_CHOICES]
        if category_lower not in valid_categories:
            return f"I don't recognize the category '{category}'. Available categories are: {', '.join(choice[0] for choice in Expense.CATEGORY_CHOICES)}."
        budgets = budgets.filter(category__iexact=category_lower)

    # Filter by frequency if specified
    if frequency:
        frequency_lower = frequency.lower()
        if frequency_lower not in dict(BudgetLimit.FREQUENCY_CHOICES).keys():
            return "Invalid frequency. Please specify 'monthly' or 'annually'."
        budgets = budgets.filter(frequency=frequency_lower)

    # If specific filters lead to no budget
    if not budgets.exists():
        if category and frequency:
            return f"You don't have a {frequency} budget limit set for {category.title()} yet."
        elif category:
            return f"You don't have any budget limits set for {category.title()} yet."
        elif frequency:
            return f"You don't have any {frequency} budget limits set yet."
        else:
            return "You haven't set any budget limits yet."

    response_lines = ["📊 Here are your budget limits "]
    # Handle the "specific category, no frequency" case if multiple frequencies exist for that category
    # This was in your previous version, let's re-incorporate it cleanly.
    if category and not frequency:
        monthly_budget = budgets.filter(frequency='monthly').first()
        annual_budget = budgets.filter(frequency='annually').first()

        if monthly_budget:
            current_spending = Expense.objects.filter(
                user=user,
                category=monthly_budget.category,
                date__year=today.year,
                date__month=today.month
            ).aggregate(total=Sum('amount'))['total'] or 0

            remaining = monthly_budget.limit - current_spending
            status = "within budget" if remaining >= 0 else "over budget"

            response_lines.append(
                f"📆 Monthly Budget for {monthly_budget.category.title()}: ₹{monthly_budget.limit:,.2f}\n"
                f"💸 Spent this month: ₹{current_spending:,.2f}\n"
                f"🧮 Remaining: ₹{remaining:,.2f} ({status})"
            )
        if annual_budget:
            # Avoid duplicating if only annual was asked or monthly was not present
            if not monthly_budget or (monthly_budget and annual_budget and monthly_budget.id != annual_budget.id):
                 # For annual budget, calculate spending for the year
                current_spending = Expense.objects.filter(
                    user=user,
                    category=annual_budget.category,
                    date__year=today.year
                ).aggregate(total=Sum('amount'))['total'] or 0
                remaining = annual_budget.limit - current_spending
                status = "within budget" if remaining >= 0 else "over budget"
                response_lines.append(
                    f"📅 Annual Budget for {annual_budget.category.title()}: ₹{annual_budget.limit:,.2f}\n"
                    f"💸 Spent this year: ₹{current_spending:,.2f}\n"
                    f"🧮 Remaining: ₹{remaining:,.2f} ({status})"
                )
        return "\n\n".join(response_lines)
    
    # If a specific frequency was requested or if showing all budgets
    for budget in budgets:
        limit_amount = budget.limit
        current_spending = 0

        # Calculate current spending for the relevant period
        if budget.frequency == 'monthly':
            current_spending = Expense.objects.filter(
                user=user,
                category=budget.category,
                date__year=today.year,
                date__month=today.month
            ).aggregate(total=Sum('amount'))['total'] or 0
            period_label = "this month"
        elif budget.frequency == 'annually':
            current_spending = Expense.objects.filter(
                user=user,
                category=budget.category,
                date__year=today.year
            ).aggregate(total=Sum('amount'))['total'] or 0
            period_label = "this year"
        else:
            current_spending = 0 # Should not happen with current choices
            period_label = "this period"

        remaining = limit_amount - current_spending
        status = "within budget" if remaining >= 0 else "over budget"

        line = (
            f"📈 {budget.category.title()} {budget.frequency.capitalize()} Limit: ₹{limit_amount:,.2f}\n"
            f"💸 Spent {period_label}: ₹{current_spending:,.2f}\n"
            f"🧮 Remaining: ₹{remaining:,.2f} ({status})"
        )
        response_lines.append(line)

    return "\n\n".join(response_lines) # Use double newline for better separation

# --- Handler for get_budget_limit intent ---
def budget_limit_handler(user, entities: dict = None) -> str:
    """
    Handles parsing entities for budget limit retrieval and calls the core function.
    """
    category = None
    frequency = None

    if entities:
        category = entities.get("category")
        frequency = entities.get("frequency")

    return get_budget_limit_data(user, category=category, frequency=frequency)

# --- Guide functions (remain mostly the same, just included for completeness) ---

def guide_set_budget_limit(user, entities: dict = None) -> str:
    """
    Guides the user on how to set a new budget limit or update an existing one.
    """
    category = entities.get("category") if entities else None
    amount = entities.get("amount") if entities else None
    frequency = entities.get("frequency") if entities else None

    if category and amount and frequency:
        return (f"To set or update your {frequency} budget of ₹{amount:,.2f} for {category.title()}, "
                "please go to the 'Budgeting' section in your app or visit our website's budget management page. "
                "You'll find easy options to set or adjust your limits there.")
    elif category and amount:
        return (f"To set or update your budget of ₹{amount:,.2f} for {category.title()}, "
                "please go to the 'Budgeting' section in your app or visit our website's budget management page. "
                "You can specify the frequency (monthly/annually) there.")
    else:
        return ("To set a new budget or update an existing one, please go to the 'Budgeting' section in your app "
                "or visit our website's budget management page. There you can easily specify the category, "
                "amount, and frequency.")

def guide_delete_budget_limit(user, entities: dict = None) -> str:
    """
    Guides the user on how to delete a budget limit.
    """
    category = entities.get("category") if entities else None
    frequency = entities.get("frequency") if entities else None

    if category and frequency:
        return (f"To delete your {frequency} budget limit for {category.title()}, "
                "please navigate to the 'Budgeting' section in your app or our website. "
                "You'll find options to manage and remove your existing budgets there.")
    elif category:
        return (f"To delete your budget limit for {category.title()}, "
                "please navigate to the 'Budgeting' section in your app or our website. "
                "You can select the specific budget to remove there.")
    else:
        return ("To delete a budget limit, please navigate to the 'Budgeting' section in your app or our website. "
                "You'll find options to manage and remove your existing budgets there.")
    










def guide_download_report(user, entities=None) -> str:
    """
    Provides a complete step-by-step guide to download the financial report.
    """
    return (
        "📥 To generate and download your financial report, follow these steps:\n\n"
        "🔐 First, log in to your financial dashboard.\n"
        "📁 Then, navigate to the Reports section from the sidebar or dashboard menu.\n\n"
        "▶️ Once you're on the report page:\n"
        "1️⃣ Choose the report duration from the dropdown — options include:\n"
        "   • `Monthly` (last 30 days)\n"
        "   • `Annual` (this year)\n"
        "   • `Overall` (all-time summary)\n"
        "2️⃣ Select the desired file format:\n"
        "   • `PDF` (for printable reports)\n"
        "   • `Excel` (for detailed spreadsheets)\n"
        "   • `CSV` (for raw data handling)\n"
        "3️⃣ Finally, click on the Download Report button to get your report.\n\n"
        "📊 Your report will include:\n"
        "• Income & Expense summaries\n"
        "• Budget vs Actual comparisons\n"
        "• Cash flow trends and charts\n"
        "• Helpful visual insights for smarter decisions\n\n"
        "💡 *Tip:* Want reports for a specific month or year? Use the filter options above the report form before downloading."
    )
