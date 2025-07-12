# from .chat_support import (
#     get_mobile_info_and_update_guide,
#     get_dob_info_and_update_guide,
#     get_gender_info_and_update_guide,
#     get_user_savings_info_and_update_guide,
#     get_user_existing_investments_info_and_update_guide,
#     get_user_risk_appetite_info_and_update_guide,
#     get_user_investment_goal_info_and_update_guide,
#     get_user_preferred_investments_info_and_update_guide,
#     suggest_fund_by_risk,
#     suggest_investment_split,
#     get_profile_created_at,
#     get_profile_updated_at,
#     is_profile_complete_check_and_guide,
#     suggest_plan_by_savings,
#     suggest_investment_goal,
#     suggest_investment_type,
#     suggest_investment_strategy,
#     generate_profile_summary,
#     update_profile_summary,
# )

# # ✅ Step 1: Create synonyms map
# SYNONYMS = {
#     # info Mobile number queries
#     "get_mobile_info_and_update_guide": [
#         "how to update mobile number",
#         "update mobile guide",
#         "change my phone number",
#         "your registered mobile number",
#         "what's my phone number",
#         "how to change mobile number",
#         "update my phone number",
#         "phone number",
#         "mobile number",
#         "my mobile",
#         "what is my phone number",
#         "change phone number",
#     ],

#     # info Date of Birth queries
#     "get_dob_info_and_update_guide": [
#         "date of birth",
#         "dob",
#         "birthdate",
#         "my dob",
#         "what is my date of birth",
#         "how to update dob",
#         "change my dob",
#         "update my date of birth",
#         "how can i change dob",
#     ],

#     # info Gender queries
#     "get_gender_info_and_update_guide": [
#         "gender",
#         "my gender",
#         "sex",
#         "what is my gender",
#         "how to update gender",
#         "change my gender",
#         "update gender information",
#         "gender details",
#     ],
    
#     # info about saving
#     "get_user_savings_info_and_update_guide": [
#         "savings",
#         "saving",
#         "how i update my savings",
#         "total savings",
#         "how much have i saved",
#         "current savings",
#     ],

#     # info about existing investment
#     "get_user_existing_investments_info_and_update_guide": [
#         "investment",
#         "investments",
#         "my investments",
#         "existing investments",
#         "current investment value",
#         "how much have i invested",
#     ],

#     # Risk appetite info & update guide
#     "get_user_risk_appetite_info_and_update_guide": [
#         "risk appetite",
#         "my risk appetite",
#         "what is my risk appetite",
#         "risk level",
#         "risk profile",
#         "update risk appetite",
#         "change risk appetite",
#         "modify risk level",
#     ],

#     # Investment goal info & update guide
#     "get_user_investment_goal_info_and_update_guide": [
#         "investment goal",
#         "my investment goal",
#         "what is my investment goal",
#         "goal for investment",
#         "update investment goal",
#         "change investment goal",
#         "modify investment goals",
#     ],

#     # Preferred investments info & update guide
#     "get_user_preferred_investments_info_and_update_guide": [
#         "preferred investments",
#         "my preferred investments",
#         "investment preferences",
#         "what are my preferred investments",
#         "update preferred investments",
#         "change investment preferences",
#         "modify preferred investments",
#     ],

#     # Suggest funds based on risk appetite
#     "suggest_fund_by_risk": [
#         "suggest funds based on risk",
#         "fund suggestions",
#         "best funds for my risk",
#         "fund recommendations",
#         "which funds should I invest in",
#         "funds for my risk appetite",
#     ],

#     # Suggest investment split based on risk appetite
#     "suggest_investment_split": [
#         "suggest investment split",
#         "investment allocation",
#         "ideal investment split",
#         "how to split investments",
#         "investment distribution advice",
#         "asset allocation",
#     ],

#     # 🆕 Profile creation date queries
#     "get_profile_created_at": [
#         "profile created",
#         "when was my profile created",
#         "profile creation date",
#         "account creation date",
#         "when did I create my profile",
#         "created my account"
#     ],

#     # 🔄 Profile last updated date queries
#     "get_profile_updated_at": [
#         "profile updated",
#         "profile last updated",
#         "last profile update",
#         "when was my profile updated",
#         "account last changed",
#         "last time I changed profile"
#     ],

#     # ✅ Checks if the user's profile is fully complete.
#     "is_profile_complete_check_and_guide": [
#         "is my profile complete",
#         "profile completeness",
#         "check profile completeness",
#         "do i need to update profile",
#         "is profile filled",
#         "profile check guide",
#         "what is missing in my profile"
#     ],

#     # 🔍 For viewing full profile summary with all fields (name, mobile, DOB, investments etc.)
#     "generate_profile_summary": [
#         "profile summary",
#         "show my profile",
#         "view my profile",
#         "display profile info",
#         "see profile details",
#         "profile ka details batao",
#         "mera profile kya hai",
#         "check profile",
#         "profile overview",
#         "my complete profile",
#     ],

#     # 🛠️ For guiding the user on how to update/edit their profile if fields are missing
#     "update_profile_summary": [
#         "how to update profile",
#         "update profile guide",
#         "profile update instructions",
#         "edit my profile",
#         "how can I change my profile",
#         "update personal info",
#         "missing profile fields",
#         "profile not complete",
#         "profile incomplete message",
#         "guide to complete profile",
#     ],

#     # Suggest investment plans based on user's savings amount
#     "suggest_plan_by_savings": [
#         "investment plan based on savings",
#         "suggest investment plan",
#         "investment advice for savings",
#         "how to invest my savings",
#         "investment recommendations based on savings",
#         "suggest a plan for my savings",
#         "what investment plan suits my savings",
#         "investment strategy for my savings",
#     ],


#     # Suggest suitable investment goals based on user profile
#     "suggest_investment_goal": [
#         "suggest investment goal",
#         "investment goal suggestion",
#         "which investment goal should I choose",
#         "best investment goal for me",
#         "recommend investment goal"
#     ],
    
#     # Suggest suitable investment types based on user risk appetite
#     "suggest_investment_type": [
#         "suggest investment type",
#         "investment type options",
#         "best investment types",
#         "where should I invest",
#         "recommend investment types"
#     ],
    
#     # Suggest an overall investment strategy based on user profile
#     "suggest_investment_strategy": [
#         "suggest investment strategy",
#         "investment plan",
#         "best investment strategy",
#         "how to invest",
#         "investment approach advice"
#     ],
    
# }


# FALLBACK_MAP = {
#     # 📱 Mobile number-related queries
#     ("phone", "mobile", "contact", "phone number", "mobile number"): get_mobile_info_and_update_guide,

#     # 🎂 Date of Birth-related queries
#     ("dob", "birthdate", "date of birth", "my dob", "birth date"): get_dob_info_and_update_guide,

#     # ⚧ Gender-related queries
#     ("gender", "sex", "my gender"): get_gender_info_and_update_guide,

#     # 💰 Savings info + update
#     ("savings", "my savings", "total savings", "money saved"): get_user_savings_info_and_update_guide,

#     # 📈 Existing investment info (avoid overlapping with 'goal', 'type', 'plan')
#     ("existing investments", "my investments", "current investment value"): get_user_existing_investments_info_and_update_guide,

#     # 📊 Risk appetite info
#     ("risk", "risk appetite", "risk level", "risk profile"): get_user_risk_appetite_info_and_update_guide,

#     # 🎯 Investment goals info
#     ("selected goal", "investment goal", "my investment goal", "financial goal in profile"): get_user_investment_goal_info_and_update_guide,

#     # 🧾 Preferred investment types info
#     ("preferred investments", "investment preferences", "preferred assets", "my preferred investment types"): get_user_preferred_investments_info_and_update_guide,

#     # 🗓️ Profile creation date
#     ("profile created", "profile creation", "account created", "account creation", "created profile", "created account"): get_profile_created_at,

#     # 🔄 Last profile update
#     ("profile updated", "last profile update", "profile last updated", "account updated", "last changed profile"): get_profile_updated_at,

#     # ✅ Profile completeness check
#     ("profile completeness", "is profile complete", "profile check", "update profile", "missing profile info"): is_profile_complete_check_and_guide,

#     # 📋 Profile summary / overview
#     ("profile summary", "show profile", "view profile", "display profile", "profile details", "check profile", "profile overview"): generate_profile_summary,

#     # 🛠️ Profile update instructions
#     ("update profile", "update profile guide", "profile update instructions", "edit profile", "update personal info", "missing profile fields", "profile incomplete"): update_profile_summary,

#     # 📌 Suggest investment plan based on savings
#     ("investment plan based on savings", "suggest investment plan", "investment advice for savings", 
#      "how to invest my savings", "investment recommendations based on savings", "suggest a plan for my savings", 
#      "what investment plan suits my savings", "investment strategy for my savings"): suggest_plan_by_savings,

#     # 🎯 Suggest ideal investment goal
#     ("suggest investment goal", "goal recommendation", "which investment goal", "best investment goal"): suggest_investment_goal,

#     # 💼 Suggest ideal investment type
#     ("suggest investment type", "investment type", "investment type suggestion", "best investment types"): suggest_investment_type,

#     # 📈 Suggest investment strategy
#     ("suggest investment strategy", "investment strategy", "strategy suggestion", "investment approach"): suggest_investment_strategy,
# }




# # Reverse mapping for faster lookups
# REVERSE_SYNONYMS = {}
# for func, phrases in SYNONYMS.items():
#     for phrase in phrases:
#         REVERSE_SYNONYMS[phrase.lower()] = func



# def get_intent_from_input(user_input):
#     input_clean = user_input.strip().lower()
#     return REVERSE_SYNONYMS.get(input_clean, None)



# from . import chat_support
# INTENT_MAP = {}
# for func_name, phrases in SYNONYMS.items():
#     func = getattr(chat_support, func_name, None)
#     if not func:
#         print(f"Warning: Function '{func_name}' not found in chat_support")
#         continue
#     for phrase in phrases:
#         normalized_phrase = phrase.strip().lower()
#         if normalized_phrase in INTENT_MAP:
#             print(f"Warning: Duplicate phrase '{normalized_phrase}' detected")
#         INTENT_MAP[normalized_phrase] = func



# # Dummy usage to silence Pylint (used dynamically via globals())
# _ = [
#     get_mobile_info_and_update_guide,
#     get_dob_info_and_update_guide,
#     get_gender_info_and_update_guide,
#     get_user_savings_info_and_update_guide,
#     get_user_existing_investments_info_and_update_guide,
#     get_user_risk_appetite_info_and_update_guide,
#     get_user_investment_goal_info_and_update_guide,
#     get_user_preferred_investments_info_and_update_guide,
#     suggest_investment_split,
#     get_profile_created_at,
#     get_profile_updated_at,
#     is_profile_complete_check_and_guide,
#     suggest_plan_by_savings,
#     suggest_investment_goal,
#     suggest_investment_type,
#     suggest_investment_strategy,
#     suggest_fund_by_risk,
#     generate_profile_summary,
#     update_profile_summary,
# ]
