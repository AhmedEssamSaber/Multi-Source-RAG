import cohere
import os
from dotenv import load_dotenv

from app.core.enums import SourceType

load_dotenv()


class RouterService:

    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def route(self, question: str) -> SourceType:

        prompt = f"""
Choose the best source for answering the question.

Sources:
- pdf
- wiki
- docs

Return ONLY one word.

Question: {question}
"""

        try:
            response = self.co.chat(
                message=prompt,
                temperature=0
            )

            output = response.text.strip().lower()

            if "pdf" in output:
                return SourceType.PDF

            elif "wiki" in output:
                return SourceType.WIKI

            elif "docs" in output:
                return SourceType.DOCS

            return SourceType.DOCS

        except:
            return SourceType.DOCS