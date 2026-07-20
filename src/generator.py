import json
from google import genai

from src.config import GEMINI_API_KEY
from src.database import query_database
from src.search import get_live_news_context

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_quiz(sport, difficulty):
    """
    Generate a sports quiz using ChromaDB + DDGS + Gemini.
    """

    # -----------------------------
    # Retrieve historical facts
    # -----------------------------
    db_results = query_database(
        query_text=f"{sport} records championships history",
        sport=sport,
        difficulty=difficulty,
        n_results=5
    )

    documents = db_results.get("documents", [[]])[0]
    historical_context = "\n".join(documents)

    # -----------------------------
    # Retrieve latest news
    # -----------------------------
    live_context = get_live_news_context(sport)

    # -----------------------------
    # Combined RAG context
    # -----------------------------
    context = f"""
================ HISTORICAL FACTS ================

{historical_context}

================ LATEST SPORTS NEWS ================

{live_context}
"""

    # -----------------------------
    # Prompt
    # -----------------------------
    prompt = f"""
You are an expert sports quiz creator.

Generate exactly FIVE multiple-choice questions.

Rules:

- Sport: {sport}
- Difficulty: {difficulty}

Return ONLY valid JSON.

The JSON format MUST be:

{{
  "sport": "{sport}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "question": "...",
      "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      }},
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}
- Use ONLY the information in the Context.
- Never invent facts.
- Each question must contain:
  - Question
  Each question MUST contain exactly four options:
A
B
C
D

Do not skip any option.
Do not repeat options.
Do not leave any option empty.
  - Correct Answer
  - Explanation
- Include at least one question from the latest sports news if possible.
- Output ONLY JSON.
- Do NOT include markdown.
- Do NOT wrap the JSON inside triple backticks.


Context:

{context}
"""

    # -----------------------------
    # Gemini Generation
    # -----------------------------
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    quiz = json.loads(response.text)
    return quiz  