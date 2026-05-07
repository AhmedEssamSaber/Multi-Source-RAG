from groq import Groq
from app.core.config import settings


class GeneratorService:

    def __init__(self):
        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

    def generate(self, question, context):

        print("\n===== FINAL CONTEXT =====\n")
        print(context[:1000])
        print("\n=========================\n")

        prompt = f"""
You are an AI assistant.

Answer clearly and directly.

Rules:
- Use context if relevant
- If not, answer from your own knowledge
- Do NOT say "based on the context"

Context:
{context}

Question:
{question}

Answer:
"""

        response = self.client.chat.completions.create(
            model=settings.GENERATION_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content.strip()
