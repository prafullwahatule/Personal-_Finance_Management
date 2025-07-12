# dashboard/nlp/response_router.py

from .intent_engine import parse_input
from dashboard import chat_support # Assuming your budget functions are now in chat_support

INTENT_TO_FUNCTION = {

    "greeting": chat_support.get_greeting,
    # Data retrieval intents:
    "get_mobile": chat_support.get_user_mobile,
    "get_savings": chat_support.get_user_savings,
    "get_risk_appetite": chat_support.get_user_risk_appetite,
    "get_investment_goals": chat_support.get_investment_goals,
    "get_preferred_investments": chat_support.get_preferred_investments,
    "get_dob": chat_support.get_user_dob,
    "get_gender": chat_support.get_user_gender,
    "get_existing_investments": chat_support.get_existing_investments,
    "get_profile_summary": chat_support.get_profile_summary,
    "get_created_at": chat_support.get_created_at,
    "get_updated_at": chat_support.get_updated_at,

    # Update guidance intents:
    "guide_update_mobile": chat_support.guide_update_mobile,
    "guide_update_savings": chat_support.guide_update_savings,
    "guide_update_risk_appetite": chat_support.guide_update_risk_appetite,
    "guide_update_investment_goals": chat_support.guide_update_investment_goals,
    "guide_update_preferred_investments": chat_support.guide_update_preferred_investments,
    "guide_update_dob": chat_support.guide_update_dob,
    "guide_update_gender": chat_support.guide_update_gender,
    "guide_update_existing_investments": chat_support.guide_update_existing_investments,

    # Other guides:
    "guide_delete_account": chat_support.guide_delete_account,
    "guide_view_profile": chat_support.guide_view_profile,
    "change_password": chat_support.guide_change_password, # Assuming this is a guide as well

    # Expense intent:
    "get_total_expense": chat_support.total_expense_handler,
    "guide_add_expense": chat_support.guide_add_expense, # Guide for setting/updating
    "guide_delete_expense": chat_support.guide_delete_expense, # Guide for deleting

    # Income intent:
    "get_total_income": chat_support.total_income_handler,
    "guide_add_income": chat_support.guide_add_income, # Guide for setting/updating
    "guide_delete_income": chat_support.guide_delete_income, # Guide for deleting

    # 🔥 Budget Intents (NEW) 🔥
    "get_budget_limit": chat_support.budget_limit_handler, # Direct retrieval
    "guide_set_budget_limit": chat_support.guide_set_budget_limit, # Guide for setting/updating
    "guide_delete_budget_limit": chat_support.guide_delete_budget_limit, # Guide for deleting


    "guide_generate_report": chat_support.guide_download_report,
}


def get_chatbot_response(user, user_input: str) -> str:
    intent, entities = parse_input(user_input)

    if intent == "unknown":
        return "Sorry, I couldn't understand that. Could you please rephrase?"

    func = INTENT_TO_FUNCTION.get(intent)
    if not func:
        return f"Intent '{intent}' recognized but no response function available."

    try:
        # Pass entities to the handler if it expects them
        # total_expense_handler and total_income_handler expect 'entities'
        # guide_set_budget_limit and guide_delete_budget_limit also expect 'entities'
        if intent in ["get_total_expense", "get_total_income", "guide_set_budget_limit", "guide_delete_budget_limit"]:
            return func(user, entities=entities)
        elif intent == "get_budget_limit": # get_budget_limit_response expects category and frequency
            return func(user, category=entities.get('category'), frequency=entities.get('frequency'))
        else: # Most other functions just expect 'user'
            return func(user)
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error processing intent '{intent}' with user input '{user_input}': {e}")
        return f"⚠️ An error occurred while processing your request. Please try again later."