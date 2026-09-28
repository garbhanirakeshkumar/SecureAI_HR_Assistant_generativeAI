import os

from dotenv import load_dotenv
from google import genai

from .semantic_search import search_policies

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=API_KEY)

# Use a current Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"


# Questions that should be answered as normal conversation
CASUAL_PATTERNS = [
    "hello",
    "hi",
    "hey",
    "how are you",
    "how are you doing",
    "what are you doing",
    "good morning",
    "good afternoon",
    "good evening",
    "who are you",
    "what can you do",
    "thanks",
    "thank you",
    "bye",
]


def is_casual_question(question):
    question = question.lower().strip()

    return any(
        pattern in question
        for pattern in CASUAL_PATTERNS
    )


def generate_casual_answer(question):

    prompt = f"""
You are SecureAI HR Assistant.

The user is having a casual conversation with you.

User message:
{question}

Reply naturally, politely, and briefly.
Do not invent HR policies.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text

        return "I could not generate a response."

    except Exception as e:
        print("Gemini casual response error:", e)
        return "Sorry, I am unable to respond right now. Please try again."


def generate_hr_answer(question):

    try:

        # Handle casual conversation separately
        if is_casual_question(question):
            return generate_casual_answer(question)

        # Search HR policies
        results = search_policies(question, top_k=3)

        context = "\n\n".join(
            [
                f"Policy: {result['filename']}\n"
                f"{result['content']}"
                for result in results
            ]
        )

        # If no policy was found
        if not context.strip():
            return "I could not find this information in the available HR policies."

        prompt = f"""
You are SecureAI HR Assistant.

Answer the user's question using ONLY the HR policy information below.

HR POLICY INFORMATION:
{context}

USER QUESTION:
{question}

Rules:
1. Answer clearly and professionally.
2. Use only the provided HR policy information for HR-related facts.
3. Do not invent company rules.
4. If the policy does not contain the answer, say:
   "I could not find this information in the available HR policies."
5. Keep the answer concise.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text

        return "I could not generate a response."

    except Exception as e:

        print("Gemini HR response error:", e)

        return (
            "Sorry, I am unable to process your request right now. "
            "Please try again."
        )