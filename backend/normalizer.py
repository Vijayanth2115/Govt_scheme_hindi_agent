from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def normalize_by_state(user_text: str, state: str):
#     """
#     Normalize Hindi user input into structured values
#     based on the current conversation state.
#     """

#     prompts = {
#         "ASK_AGE": f"""
# Convert the Hindi text into AGE in years.
# Return ONLY a number.

# Text: "{user_text}"
# """,

#         "ASK_INCOME": f"""
# Convert the Hindi text into ANNUAL INCOME in INR.
# Return ONLY a number.

# Text: "{user_text}"
# """,

#         "ASK_STATE": f"""
# Extract the Indian state name from Hindi text.
# Return ONLY the state name in English lowercase snake_case.
# Example: andhra_pradesh, uttar_pradesh, maharashtra

# Text: "{user_text}"
# """,

#         "ASK_CATEGORY": f"""
# From Hindi text, identify caste category.
# Return ONLY one of the following values:
# sc, st, obc, general

# Text: "{user_text}"
# """,

#         "ASK_GENDER": f"""
# From Hindi text, identify gender.
# Return ONLY one of the following values:
# male or female

# Text: "{user_text}"
# """,

#         "ASK_OCCUPATION": f"""
# From Hindi text, identify occupation.
# Return ONLY one of the following values:
# farmer or other

# Text: "{user_text}"
# """
#     }

#     prompt = prompts.get(state)
#     if not prompt:
#         return None

#     try:
#         response = client.responses.create(
#             model="gpt-4o-mini",
#             input=prompt,
#             temperature=0
#         )

#         # Extract clean output
#         value = response.output_text.strip().lower()

#         # Guard against empty or nonsense outputs
#         if not value or value in ["unknown", "none", "null"]:
#             return None

#         return value

#     except Exception as e:
#         # Log if needed
#         # print("Normalizer error:", e)
#         return None


def normalize_by_state(user_text: str, state: str):
    if not user_text or not user_text.strip():
        return None

    prompts = {
        "ASK_AGE": f"""
Convert the Hindi text into AGE in years.
Return ONLY a number.

Text: "{user_text}"
""",

        "ASK_INCOME": f"""
Convert the Hindi text into ANNUAL INCOME in INR.
Return ONLY a number.

Text: "{user_text}"
""",

        "ASK_STATE": f"""
Extract the Indian state name from Hindi text.
Return ONLY the state name in English lowercase snake_case.
Example: uttar_pradesh, maharashtra

Text: "{user_text}"
""",

        "ASK_CATEGORY": f"""
From Hindi text, identify caste category.
Return ONLY one of: sc, st, obc, general

Text: "{user_text}"
""",

        "ASK_GENDER": f"""
From Hindi text, identify gender.
Return ONLY one of: male or female

Text: "{user_text}"
""",

        "ASK_OCCUPATION": f"""
From Hindi text, identify occupation.
Return ONLY one of: farmer or other

Text: "{user_text}"
"""
    }

    prompt = prompts.get(state)
    if not prompt:
        return None

    try:
        r = client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=0
        )

        value = r.output_text.strip().lower()

        # 🔒 HARD FILTERS (CRITICAL)
        INVALID_PHRASES = [
            "please provide",
            "no text provided",
            "i'm sorry",
            "cannot",
            "unable",
            "text provided",
            "analyze"
        ]

        if any(p in value for p in INVALID_PHRASES):
            return None

        # 🔒 STATE-SPECIFIC VALIDATION
        if state in ["ASK_AGE", "ASK_INCOME"]:
            return value if value.isdigit() else None

        if state == "ASK_CATEGORY":
            return value if value in ["sc", "st", "obc", "general"] else None

        if state == "ASK_GENDER":
            return value if value in ["male", "female"] else None

        if state == "ASK_OCCUPATION":
            return value if value in ["farmer", "other"] else None

        if state == "ASK_STATE":
            return value if "_" in value else None

        return None

    except Exception:
        return None
