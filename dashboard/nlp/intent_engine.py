# dashboard/nlp/intent_engine.py 

import spacy
import string
import re
from datetime import date
from dashboard.chat_support import parse_month
# Assuming Expense model and IncomeTracker model are accessible for choices
# from .models import Expense, IncomeTracker # Uncomment if not already imported/accessible globally


nlp = spacy.load("en_core_web_sm")

def clean_text(text: str) -> str:
    """Lowercases, removes punctuation, and strips whitespace from text."""
    return text.lower().translate(str.maketrans('', '', string.punctuation)).strip()

# Example sentences per intent (for semantic similarity)
INTENT_EXAMPLES = {
    "greeting": [
        "hi", "hello", "hey", "hey there", "hi there", "good morning",
        "good afternoon", "good evening", "yo", "hola"
    ],
    "get_mobile": [
        "what is my mobile number", "tell me my phone number", "show my contact number",
    ],
    "get_savings": [
        "how much savings do I have", "show my savings amount", "what are my current savings",
        "my savings details"
    ],
    "get_risk_appetite": [
        "what is my risk appetite", "tell me my risk level", "am I a low risk investor",
        "show my risk preference"
    ],
    "get_investment_goals": [
        "what are my investment goals", "show my financial goals", "tell me my investment objectives",
        "my investment targets"
    ],
    "get_preferred_investments": [
        "what are my preferred investments", "show me my investment preferences",
        "tell me which investments I like", "my favorite investment types"
    ],
    "get_dob": [
        "what is my date of birth", "tell me my birthdate", "when is my birthday",
        "show my dob", "what date was I born", "when is my birth date"
    ],
    "get_gender": [
        "what is my gender", "am I male or female", "tell me my gender",
        "show my gender", "what sex am I"
    ],
    "get_existing_investments": [
        "how much have I invested", "what are my total investments", "show my investments",
        "tell me my current investments", "what is my investment amount"
    ],
    "get_profile_summary": [
        "show my profile summary", "tell me about my profile", "give me my profile details",
        "display my profile summary", "what is in my profile"
    ],
    "get_created_at": [
        "when was my profile created", "show profile creation date", "tell me when I joined",
        "when did I create my profile", "profile created on which date"
    ],
    "get_updated_at": [
        "when was my profile last updated", "show last profile update", "tell me when I updated my profile",
        "when did I last update profile", "profile last changed on"
    ],
    "guide_update_profile": [
        "how do I update my profile", "guide me to update profile",
        "help me change my profile details", "how to edit profile info"
    ],
    "guide_update_mobile": [
        "how do I update my mobile number", "guide me to change phone number",
        "help me update contact number", "how to edit my mobile"
    ],
    "guide_update_savings": [
        "how can I update my savings", "guide me to change savings amount",
        "help me update savings details", "how to edit savings info"
    ],
    "guide_update_risk_appetite": [
        "how to update risk appetite", "guide me to change risk level",
        "help me update my risk preference", "how do I edit risk appetite"
    ],
    "guide_update_investment_goals": [
        "how do I update investment goals", "help me change my financial goals",
        "guide to edit investment targets", "how to modify investment goals"
    ],
    "guide_update_preferred_investments": [
        "how to update preferred investments", "guide me to change my investment types",
        "help me update my investment preferences", "how do I edit preferred investments"
    ],
    "guide_update_dob": [
        "how to update date of birth", "guide me to change my birthdate",
        "help me edit my DOB", "how do I update birthday info"
    ],
    "guide_update_gender": [
        "how to update my gender", "guide me to change gender info",
        "help me edit gender", "how do I update gender details"
    ],
    "guide_update_existing_investments": [
        "how to update existing investments", "guide me to change invested amount",
        "help me edit my investments", "how do I update total investments"
    ],
    "guide_delete_account": [
        "how do I delete my account", "guide me to delete account",
        "help me remove my profile", "how to delete my account permanently"
    ],
    "guide_view_profile": [
        "how do I view my profile", "show me how to see my profile",
        "guide me to check profile details", "how to open my profile page"
    ],
    "change_password": [
        "how do I change my password", "help me update my password",
        "guide me to change password", "how to reset my password"
    ],
    "get_total_expense": [
        "what is my total expense", "show my overall expenses", "how much did I spend",
        "total spending till now", "give me total current_month expense",
        "how much did I spend this month", "show last_month expenses",
        "expense report for February", "how much did I spend in January",
        "tell me expenses for 2023", "total current_year expense",
        "how much did I spend this year", "total expense this current_month",
        "my overall spending", "spending last_month", "how much did i spend on food",
        "my spending on groceries", "expense for travel in april"
    ],

    "guide_add_expense": [
        "how do i add an expense",
        "i want to log an expense",
        "can i record a new expense",
        "add my food expense",
        "enter a travel expense",
        "how to register spending"
    ],
    
    "guide_delete_expense": [
        "how do i delete an expense",
        "i want to remove an expense",
        "can i delete my expense entry",
        "delete my last grocery expense",
        "remove that transaction",
        "how to erase expense"
    ],

    "get_total_income": [
        "what is my total income", "show my overall income", "how much did I earn",
        "total earnings till now", "give me total current_month income",
        "how much did I earn this month", "show last_month income",
        "income report for March", "how much did I earn in April",
        "tell me income for 2024", "total current_year income",
        "how much did I earn this year", "how much salary did I get this month",
        "what was my freelance income in May", "total investment income",
        "show business earnings for last year", "my overall income",
        "income last_month", "how much did I earn from salary",
        "my freelance earnings for this month"
    ],

    "guide_add_income": [
        "how do i add income",
        "i got salary, how to record it",
        "i want to log income",
        "can i register money earned",
        "enter a new income",
        "how to add earnings"
    ],
    
    "guide_delete_income": [
        "how do i delete income",
        "i want to remove an income record",
        "can i delete salary entry",
        "remove income log",
        "delete an income",
        "how to erase income data"
    ],

    # --- NEW BUDGET-RELATED INTENTS ---
    "get_budget_limit": [
        "what is my budget limit",
        "show me my budget for food",
        "tell me my monthly budgets",
        "what's my annual travel budget",
        "show all my budget limits",
        "how much is my budget for groceries this month",
        "what are my current budgets",
        "do I have a budget for transportation",
        "show my budget for utilities",
        "what's my budget for shopping annually"
    ],
    "guide_set_budget_limit": [
        "how do I set a budget",
        "I want to set a new budget",
        "how can I create a budget limit",
        "guide me to set a budget",
        "how to add a budget",
        "I need to update my monthly food budget", # User asks for update directly
        "can I change my travel budget", # User asks for change directly
        "how do I modify a budget",
        "help me set a new budget"
    ],
    "guide_delete_budget_limit": [
        "how do I delete a budget",
        "I want to remove a budget limit",
        "how can I delete my monthly food budget",
        "guide me to delete a budget",
        "how to remove a budget",
        "can I delete my budget for entertainment"
    ],
    "guide_generate_report": [
      "How can I download my report?",
      "I want to generate a report",
      "How to create a monthly report?",
      "Guide me to export my report",
      "How to view annual summary?",
      "Can I get an overall report?",
      "Where can I download income vs expense report?",
      "Help me download a budget report",
      "How do I get last month's report?",
      "Show me how to generate a report"
    ]
}

# Cache the processed example docs for performance
EXAMPLE_DOCS = {
    intent: [nlp(clean_text(ex)) for ex in examples]
    for intent, examples in INTENT_EXAMPLES.items()
}

SIMILARITY_THRESHOLD = 0.7  # Tune as needed

def keyword_fallback(user_input: str) -> str:
    user_input_lower = user_input.lower()

    # --- NEW: Prioritize budget guide intents for setting/deleting ---
    if "set budget" in user_input_lower or "create budget" in user_input_lower or "add budget" in user_input_lower:
        return "guide_set_budget_limit"
    if "update budget" in user_input_lower or "change budget" in user_input_lower or "modify budget" in user_input_lower:
        return "guide_set_budget_limit" # Guide for update also points to setting process
    if "delete budget" in user_input_lower or "remove budget" in user_input_lower:
        return "guide_delete_budget_limit"

    # Prioritize general "expense" or "income" keywords first, if present
    if "expense" in user_input_lower or "spend" in user_input_lower:
        return "get_total_expense"
    if "income" in user_input_lower or "earn" in user_input_lower:
        return "get_total_income"


    # Specific update guides - longer phrases checked first
    fallback_keywords = {
        "investment goal": "guide_update_investment_goals",
        "preferred investment": "guide_update_preferred_investments",
        "date of birth": "guide_update_dob",
        "risk appetite": "guide_update_risk_appetite",
        "delete account": "guide_delete_account",
        "change password": "change_password",
        "reset password": "change_password",
        "update mobile": "guide_update_mobile",
        "update savings": "guide_update_savings",
        "update gender": "guide_update_gender",
        "update existing investments": "guide_update_existing_investments",
        "view profile": "guide_view_profile",
    }
    for phrase in sorted(fallback_keywords.keys(), key=len, reverse=True):
        if phrase in user_input_lower:
            return fallback_keywords[phrase]

    # Other keywords grouped by intent (shorter, single-word matches)
    keywords_map = {
        # --- NEW: Budget-related general keywords, leading to 'get_budget_limit' if not set/delete ---
        "budget": "get_budget_limit",
        "limit": "get_budget_limit",
        "expenses": "get_total_expense", # Catch if "budget" isn't present
        "spending": "get_total_expense",
        "income": "get_total_income", # Catch if "earn" isn't present
        "earnings": "get_total_income",
        "add expense": "guide_add_expense",
        "log expense": "guide_add_expense",
        "record expense": "guide_add_expense",
        "delete expense": "guide_delete_expense",
        "remove expense": "guide_delete_expense",
        "add income": "guide_add_income",
        "log income": "guide_add_income",
        "record income": "guide_add_income",
        "delete income": "guide_delete_income",
        "remove income": "guide_delete_income",

        # Categories that might hint at budget/expense
        "food": "get_budget_limit",
        "groceries": "get_budget_limit",
        "travel": "get_budget_limit",
        "entertainment": "get_budget_limit",
        "utilities": "get_budget_limit",
        "housing": "get_budget_limit",
        "shopping": "get_budget_limit",
        "transportation": "get_budget_limit",


        # greeting
        "hello": "greeting", "hi": "greeting", "hey": "greeting", "hiii": "greeting", "heyy": "greeting",

        # get_mobile
        "mobile": "get_mobile", "phone": "get_mobile", "contact": "get_mobile", "number": "get_mobile",

        # get_savings
        "saving": "get_savings", "savings": "get_savings", "saved": "get_savings", "balance": "get_savings",

        # get_risk_appetite
        "risk": "get_risk_appetite", "appetite": "get_risk_appetite", "level": "get_risk_appetite",
        "preference": "get_risk_appetite",

        # get_investment_goals
        "goal": "get_investment_goals", "goals": "get_investment_goals", "target": "get_investment_goals",
        "objective": "get_investment_goals",

        # get_preferred_investments
        "preferred": "get_preferred_investments", "favorite": "get_preferred_investments",
        "investment type": "get_preferred_investments",

        # get_dob
        "dob": "get_dob", "birthday": "get_dob", "birthdate": "get_dob", "born": "get_dob",

        # get_gender
        "gender": "get_gender", "male": "get_gender", "female": "get_gender", "sex": "get_gender",

        # get_existing_investments
        "invested": "get_existing_investments", "investment": "get_existing_investments",

        # get_profile_summary
        "profile": "get_profile_summary", "summary": "get_profile_summary", "details": "get_profile_summary",
        "info": "get_profile_summary",

        # get_created_at
        "created": "get_created_at", "joined": "get_created_at", "signup": "get_created_at",
        "registered": "get_created_at",

        # get_updated_at
        "updated": "get_updated_at", "modified": "get_updated_at",

        # guide_delete_account
        "delete": "guide_delete_account", "remove": "guide_delete_account", "close": "guide_delete_account",

        # guide_view_profile
        "view": "guide_view_profile", "show": "guide_view_profile", "open": "guide_view_profile",

        "report": "guide_generate_report",
        "financial report": "guide_generate_report",
        "generate report": "guide_generate_report",
        "download report": "guide_generate_report",
        "pdf report": "guide_generate_report",
        "excel report": "guide_generate_report",
        "expense report": "guide_generate_report",
        "income report": "guide_generate_report"

    }

    # Check longer phrases first (sorted by length desc)
    for phrase in sorted(keywords_map.keys(), key=len, reverse=True):
        if phrase in user_input_lower:
            return keywords_map[phrase]

    return "unknown"


def classify_intent(user_input: str) -> str:
    cleaned_input = clean_text(user_input)
    input_doc = nlp(cleaned_input)
    max_similarity = 0
    best_intent = "unknown"

    for intent, example_docs in EXAMPLE_DOCS.items():
        for example_doc in example_docs:
            if not example_doc.vector_norm:
                continue

            similarity = input_doc.similarity(example_doc)
            if similarity > max_similarity:
                max_similarity = similarity
                best_intent = intent

    if max_similarity < SIMILARITY_THRESHOLD:
        return keyword_fallback(user_input)
    else:
        return best_intent


def extract_entities(user_input: str, detected_intent: str = None) -> dict:
    entities = {}
    text = user_input.lower()

    # --- Period/Frequency Detection ---
    if "this month" in text:
        entities["period"] = "current_month"
        entities["frequency"] = "monthly" # Add for budget context
    elif "last month" in text:
        entities["period"] = "last_month"
        entities["frequency"] = "monthly" # Add for budget context
    elif "this year" in text or "current year" in text:
        entities["period"] = "current_year"
        entities["frequency"] = "annually" # Add for budget context
    elif "overall" in text or "till now" in text:
        entities["period"] = "all_time"

    # Explicit frequency keywords for budget limits
    if "monthly" in text:
        entities["frequency"] = "monthly"
    elif "annual" in text or "yearly" in text: # Added 'yearly' for annual
        entities["frequency"] = "annually"

    # --- Month Detection ---
    month_pattern = r"\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b"
    month_match = re.search(month_pattern, text)
    if month_match:
        entities["month"] = parse_month(month_match.group())

    # --- Year Detection (4-digit) ---
    year_match = re.search(r"\b(20\d{2})\b", text)
    if year_match:
        entities["year"] = int(year_match.group())

    # --- Amount Detection (Relevant for guide_set_budget_limit) ---
    amount_match = re.search(r"(?:₹|rs\.?|inr)?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)", text)
    if amount_match:
        try:
            entities["amount"] = float(amount_match.group(1).replace(',', ''))
        except ValueError:
            pass

    # --- Category Detection (Specific to Expense & Budget) ---
    # You need to ensure Expense.CATEGORY_CHOICES is accessible here.
    # If not, you might need to import the Expense model.
    try:
        from dashboard.models import Expense, IncomeTracker # Assuming these are in dashboard/models.py
        expense_categories = [choice[0].lower() for choice in Expense.CATEGORY_CHOICES]
    except ImportError:
        # Fallback if models aren't directly importable in this context (e.g., for testing)
        # In a real Django setup, these imports should work from .models
        print("Warning: Could not import Expense model for categories in intent_engine.py. Using dummy categories.")
        expense_categories = ["food", "groceries", "travel", "entertainment", "utilities", "housing", "shopping", "transportation"]


    if detected_intent in ["get_total_expense", "get_budget_limit", "guide_set_budget_limit", "guide_delete_budget_limit"]:
        for category in expense_categories:
            if re.search(r'\b' + re.escape(category) + r'\b', text):
                entities["category"] = category.title()
                break

    # --- Source Detection (Specific to Income) ---
    try:
        from dashboard.models import IncomeTracker # Assuming this is in dashboard/models.py
        income_sources = [choice[0].lower() for choice in IncomeTracker.SOURCE_CHOICES]
    except ImportError:
        print("Warning: Could not import IncomeTracker model for sources in intent_engine.py. Using dummy sources.")
        income_sources = ["salary", "freelance", "business", "investment", "gift", "other"]

    if detected_intent == "get_total_income" or (not entities and any(s in text for s in income_sources)):
        for source in income_sources:
            if source in text:
                entities["source"] = source.title()
                break

    return entities


def parse_input(user_input: str) -> tuple:
    intent = classify_intent(user_input)
    entities = extract_entities(user_input, detected_intent=intent)
    return intent, entities