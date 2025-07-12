from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, ExpenseActivityLog, IncomeTracker

# Expense Logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Expense, ExpenseActivityLog

# Expense Logging
@receiver(post_save, sender=Expense)
def log_expense_add(sender, instance, created, **kwargs):
    if created:
        details = (
            f"Action: Expense added\n"
            f"Amount: ₹{instance.amount:.2f}\n"
            f"Category: {instance.get_category_display()}\n"
            f"Date:"
        )
        ExpenseActivityLog.objects.create(
            user=instance.user,
            action="Added",
            details=details
        )

@receiver(post_delete, sender=Expense)
def log_expense_delete(sender, instance, **kwargs):
    details = (
        f"Action: Expense removed\n"
        f"Amount: ₹{instance.amount:.2f}\n"
        f"Category: {instance.get_category_display()}\n"
        f"Date:"
    )
    ExpenseActivityLog.objects.create(
        user=instance.user,
        action="Removed",
        details=details
    )



# Income Logging
@receiver(post_save, sender=IncomeTracker)
def log_income_add(sender, instance, created, **kwargs):
    if created:
        details = (
            f"Action: Income added\n"
            f"Amount: ₹{instance.amount}\n"
            f"Source: {instance.get_source_display()}\n"
            f"Date:"
        )
        ExpenseActivityLog.objects.create(
            user=instance.user,
            action="Added",
            details=details
        )

@receiver(post_delete, sender=IncomeTracker)
def log_income_delete(sender, instance, **kwargs):
    details = (
        f"Action: Income removed\n"
        f"Amount: ₹{instance.amount}\n"
        f"Source: {instance.get_source_display()}\n"
        f"Date:"
    )
    ExpenseActivityLog.objects.create(
        user=instance.user,
        action="Removed",
        details=details
    )



from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserProfile, ExpenseActivityLog

@receiver(pre_save, sender=UserProfile)
def store_old_userprofile(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = UserProfile.objects.get(pk=instance.pk)
        except UserProfile.DoesNotExist:
            instance._old_instance = None

@receiver(post_save, sender=UserProfile)
def log_userprofile_update(sender, instance, created, **kwargs):
    if created:
        return

    old = getattr(instance, '_old_instance', None)
    if not old:
        return

    fields_to_check = {
        'mobile': 'Mobile Number',
        'dob': 'Date of Birth',
        'gender': 'Gender',
        'savings': 'Savings',
        'existing_investments': 'Existing Investments',
        'risk_appetite': 'Risk Appetite',
        'investment_goals': 'Investment Goals',
        'preferred_investments': 'Preferred Investments',
    }

    for field, label in fields_to_check.items():
        old_val = getattr(old, field)
        new_val = getattr(instance, field)

        # Date of change (now)
        changed_date = instance.updated_at if hasattr(instance, 'updated_at') else instance.pk and instance.user.date_joined.date()  # fallback, or you can use timezone.now()

        # For float comparison
        if isinstance(old_val, float) and isinstance(new_val, float):
            if round(old_val, 2) != round(new_val, 2):
                details = (
                    f"Action: {label} Updated\n"
                    f"Old: ₹{old_val:.2f}\n"
                    f"New: ₹{new_val:.2f}\n"
                    f"Date:"
                )
                ExpenseActivityLog.objects.create(
                    user=instance.user,
                    action=f"{label} Updated",
                    details=details
                )
        elif str(old_val) != str(new_val):
            details = (
                f"Action: {label} Updated\n"
                f"Old: {old_val}\n"
                f"New: {new_val}\n"
                f"Date:"
            )
            ExpenseActivityLog.objects.create(
                user=instance.user,
                action=f"{label} Updated",
                details=details
            )




# signals.py
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import ExpenseActivityLog
from django.utils.timezone import now

# ------------------------- STORE OLD USER BEFORE SAVE -------------------------

@receiver(pre_save, sender=User)
def store_old_user(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            instance._old_instance = None

# ------------------------- LOG EMAIL CHANGE -------------------------

@receiver(post_save, sender=User)
def log_user_email_change(sender, instance, created, **kwargs):
    if created:
        return

    old = getattr(instance, '_old_instance', None)
    if old and old.email != instance.email:
        log_details = (
            "Action: Email Updated\n"
            f"Old Email: {old.email}\n"
            f"New Email: {instance.email}\n"
            f"Date:"
        )
        ExpenseActivityLog.objects.create(
            user=instance,
            action="Updated",
            details=log_details
        )

# ------------------------- LOG PASSWORD CHANGE -------------------------

@receiver(post_save, sender=User)
def log_user_password_change(sender, instance, created, **kwargs):
    if created:
        return

    old = getattr(instance, '_old_instance', None)
    if old and old.password != instance.password:
        log_details = (
            "Action: Password Updated\n"
            f"Date:"
        )
        ExpenseActivityLog.objects.create(
            user=instance,
            action="Updated",
            details=log_details
        )




from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import BudgetLimit, ExpenseActivityLog

# ------------------------- BUDGET LIMIT CHANGE LOGGING -------------------------

@receiver(pre_save, sender=BudgetLimit)
def store_old_budget_limit(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_instance = BudgetLimit.objects.get(pk=instance.pk)
        except BudgetLimit.DoesNotExist:
            instance._old_instance = None

@receiver(post_save, sender=BudgetLimit)
def log_budget_limit_change(sender, instance, created, **kwargs):
    user = getattr(instance, 'user', None)
    if not user:
        return

    freq = instance.get_frequency_display()
    cat = instance.get_category_display()

    if created:
        log_details = (
            "Action: Budget Limit Created\n"
            f"Category: {cat}\n"
            f"Frequency: {freq}\n"
            f"Limit: ₹{instance.limit:.2f}\n"
            f"Date:"
        )
        ExpenseActivityLog.objects.create(
            user=user,
            action="Created",
            details=log_details
        )
    else:
        old = getattr(instance, '_old_instance', None)
        if old:
            notes = []

            if old.limit != instance.limit:
                notes.append(f"Note: Limit changed from ₹{old.limit:.2f} to ₹{instance.limit:.2f}")
            if old.category != instance.category:
                notes.append(f"Note: Category changed from '{old.get_category_display()}' to '{cat}'")
            if old.frequency != instance.frequency:
                notes.append(f"Note: Frequency changed from '{old.get_frequency_display()}' to '{freq}'")

            if not notes:
                notes.append("Note: No values were changed, but the limit was re-saved.")

            log_details = (
                "Action: Budget Limit Updated\n"
                f"Category: {cat}\n"
                f"Frequency: {freq}\n"
            )

            for note in notes:
                log_details += f"{note}\n"

            log_details += "Date:"

            ExpenseActivityLog.objects.create(
                user=user,
                action="Updated",
                details=log_details
            )

@receiver(post_delete, sender=BudgetLimit)
def log_budget_limit_delete(sender, instance, **kwargs):
    user = getattr(instance, 'user', None)
    if not user:
        return

    log_details = (
        "Action: Budget Limit Deleted\n"
        f"Category: {instance.get_category_display()}\n"
        f"Frequency: {instance.get_frequency_display()}\n"
        f"Limit: ₹{instance.limit:.2f}\n"
        f"Date:"
    )
    ExpenseActivityLog.objects.create(
        user=user,
        action="Deleted",
        details=log_details
    )




from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models import Sum
from .models import Expense, BudgetLimit, ExpenseActivityLog

@receiver(post_save, sender=Expense)
def log_budget_usage_signal(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    category = instance.category
    today = now().date()

    # Get all budget limits for this user and category
    limits = BudgetLimit.objects.filter(user=user, category=category)

    for limit in limits:
        # Calculate the start date of the budget period based on frequency
        if limit.frequency == 'monthly':
            start_date = today.replace(day=1)
        elif limit.frequency == 'annually':
            start_date = today.replace(month=1, day=1)
        else:
            # Skip if frequency is not monthly or annually
            continue

        # Sum total expenses in this category during the current budget period
        total_spent = Expense.objects.filter(
            user=user,
            category=category,
            date__gte=start_date,
            date__lte=today
        ).aggregate(total=Sum('amount'))['total'] or 0

        if limit.limit == 0:
            continue  # Avoid division by zero

        percentage = (total_spent / limit.limit) * 100

        # Define thresholds to check
        thresholds = [50, 90, 100]

        # Check if threshold crossed and not already logged in current budget period
        for threshold in thresholds:
            if percentage >= threshold:
                # Compose unique identifier string for this log entry
                log_action = f"Budget Limit {threshold}% Crossed"
                category_display = limit.get_category_display()
                freq_display = limit.get_frequency_display()

                # Check if a log entry already exists in this budget period
                already_logged = ExpenseActivityLog.objects.filter(
                    user=user,
                    action=log_action,
                    details__icontains=f"{category_display} ({freq_display})",
                    # Optional: filter logs created since start_date for accuracy
                    created_at__gte=start_date
                ).exists()

                if not already_logged:
                    ExpenseActivityLog.objects.create(
                        user=user,
                        action=log_action,
                        details=(
                            f"Alert: You have crossed {threshold}% of your budget for "
                            f"'{category_display}' ({freq_display}). "
                            f"Spent: ₹{total_spent:,.2f} out of ₹{limit.limit:,.2f} "
                            f"({percentage:.2f}%).\n"
                            f"Date:"
                        )
                    )
