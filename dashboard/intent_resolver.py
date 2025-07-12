# # dashboard/intent_resolver.py

# from rapidfuzz import fuzz
# from .chat_intents import INTENT_MAP

# FUZZY_THRESHOLD = 70
# UPDATE_KEYWORDS = ["update", "change", "how to", "edit"]

# def resolve_intent(user_input):
#     user_input = user_input.lower().strip()

#     if user_input in INTENT_MAP:
#         print(f"Exact match found for: {user_input}")
#         return INTENT_MAP[user_input]

#     best_match = None
#     highest_score = 0

#     for phrase in INTENT_MAP:
#         score = fuzz.partial_ratio(user_input, phrase)
#         if score > highest_score:
#             highest_score = score
#             best_match = phrase

#     if highest_score >= FUZZY_THRESHOLD:
#         print(f"Fuzzy match found for: {best_match} with score {highest_score}")
#         return INTENT_MAP[best_match]

#     print("No intent match found.")
#     return None
