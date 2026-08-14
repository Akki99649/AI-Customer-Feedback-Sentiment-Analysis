import os
import json
import re

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# API KEY
# ---------------------------------------------------------

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)


# ---------------------------------------------------------
# CREATE GEMINI MODEL
# ---------------------------------------------------------

def get_llm():

    if not GOOGLE_API_KEY:

        raise ValueError(
            "GOOGLE_API_KEY is missing. "
            "Please create a .env file and add your Gemini API key."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2
    )


# ---------------------------------------------------------
# CLEAN JSON RESPONSE
# ---------------------------------------------------------

def clean_json_response(response_text):

    text = response_text.strip()

    # Remove markdown code fences
    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```",
        "",
        text
    )

    text = text.strip()

    # Find JSON object if additional text exists
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    return text


# ---------------------------------------------------------
# ANALYZE FEEDBACK
# ---------------------------------------------------------

def analyze_feedback(feedback):

    if not feedback or not feedback.strip():

        return {
            "error": "Feedback cannot be empty."
        }

    try:

        llm = get_llm()

        prompt = f"""
You are an expert AI customer feedback analyst.

Analyze the following customer feedback.

CUSTOMER FEEDBACK:
{feedback}

Return ONLY a valid JSON object.

Use exactly this structure:

{{
    "sentiment": "Positive, Negative, or Neutral",
    "emotion": "Primary customer emotion",
    "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ],
    "topics": [
        "topic1",
        "topic2"
    ],
    "main_complaint": "Main complaint or issue. If there is no complaint, say No major complaint.",
    "summary": "Short summary in 1-2 sentences.",
    "satisfaction_score": 1,
    "recommended_action": "Recommended action for customer support.",
    "support_reply": "Professional and empathetic response to the customer."
}}

Rules:

1. sentiment must be exactly Positive, Negative, or Neutral.
2. satisfaction_score must be an integer from 1 to 10.
3. Use 1-5 useful keywords.
4. Use 1-5 important topics.
5. Do not invent information that is not present.
6. Keep the summary short.
7. The support reply should be professional and empathetic.
8. Return ONLY JSON.

Now analyze the feedback.
"""

        response = llm.invoke(prompt)

        response_text = response.content

        cleaned = clean_json_response(
            response_text
        )

        result = json.loads(
            cleaned
        )

        # ---------------------------------------------
        # VALIDATE RESULT
        # ---------------------------------------------

        sentiment = result.get(
            "sentiment",
            "Neutral"
        )

        allowed_sentiments = [
            "Positive",
            "Negative",
            "Neutral"
        ]

        if sentiment not in allowed_sentiments:

            sentiment = "Neutral"

        result["sentiment"] = sentiment

        # ---------------------------------------------
        # VALIDATE SCORE
        # ---------------------------------------------

        try:

            score = int(
                result.get(
                    "satisfaction_score",
                    5
                )
            )

        except:

            score = 5

        score = max(
            1,
            min(
                10,
                score
            )
        )

        result["satisfaction_score"] = score

        # ---------------------------------------------
        # VALIDATE LISTS
        # ---------------------------------------------

        if not isinstance(
            result.get("keywords"),
            list
        ):

            result["keywords"] = []

        if not isinstance(
            result.get("topics"),
            list
        ):

            result["topics"] = []

        return result

    except json.JSONDecodeError:

        return {
            "error":
            "The AI returned an invalid response format. Please try again."
        }

    except ValueError as e:

        return {
            "error": str(e)
        }

    except Exception as e:

        return {
            "error":
            f"AI/API error: {str(e)}"
        }