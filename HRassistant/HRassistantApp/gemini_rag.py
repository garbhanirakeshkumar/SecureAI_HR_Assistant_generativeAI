import os

from dotenv import load_dotenv
from google import genai

from .semantic_search import search_policies


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

client = genai.Client(
    api_key=API_KEY
)

MODEL_NAME = "gemini-3.5-flash-lite"


# =========================================================
# CASUAL CONVERSATION
# =========================================================

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
    """
    Check whether the user message
    is a casual conversation.
    """

    question = question.lower().strip()

    return any(
        pattern in question
        for pattern in CASUAL_PATTERNS
    )


def generate_casual_answer(question):
    """
    Generate a short response for
    casual conversations.
    """

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
        print(
            "Gemini casual response error:",
            e
        )

        return (
            "Sorry, I am unable to respond right now. "
            "Please try again."
        )


# =========================================================
# HR RAG ANSWER
# =========================================================

def generate_hr_answer(question):
    """
    Generate an HR answer using only
    documents uploaded by HR.
    """

    try:

        # -------------------------------------------------
        # Casual conversation
        # -------------------------------------------------

        if is_casual_question(question):
            return generate_casual_answer(question)

        # -------------------------------------------------
        # Search HR-uploaded documents
        # -------------------------------------------------

        results = search_policies(
            question,
            top_k=3
        )

        # -------------------------------------------------
        # No relevant documents
        # -------------------------------------------------

        if not results:
            return (
                "I could not find this information "
                "in the available HR policies."
            )

        # -------------------------------------------------
        # Build context
        # -------------------------------------------------

        context_parts = []

        for result in results:
            context_parts.append(
                f"""
Document: {result['filename']}

Content:
{result['content']}
"""
            )

        context = "\n".join(context_parts)

        # -------------------------------------------------
        # Gemini prompt
        # -------------------------------------------------

        prompt = f"""
You are SecureAI HR Assistant.

Answer the user's question using ONLY the
HR policy information provided below.

HR POLICY INFORMATION:

{context}

USER QUESTION:

{question}

Rules:

1. Answer clearly and professionally.

2. Use only the provided HR policy information
   for HR-related facts.

3. Do not invent company rules, benefits,
   leave balances, salary rules, or procedures.

4. If the provided documents do not contain
   enough information to answer the question,
   say exactly:

"I could not find this information in the
available HR policies."

5. Keep the answer concise.

6. Do not mention similarity scores,
   embeddings, vector databases, or RAG
   implementation details.

7. If multiple documents contain relevant
   information, combine the information
   accurately.
"""

        # -------------------------------------------------
        # Generate Gemini response
        # -------------------------------------------------

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text

        return "I could not generate a response."

    except Exception as e:
        print(
            "Gemini HR response error:",
            e
        )

        return (
            "Sorry, I am unable to process your "
            "request right now. Please try again."
        )