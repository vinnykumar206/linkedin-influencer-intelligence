"""
Taxonomy Classification Module

Demonstrates dynamic category tag assignment using LLM semantic evaluation with fallback keyword matching.
"""

from typing import List, Optional


class TaxonomyClassifier:
    def __init__(self, llm_client: Optional[object] = None):
        self.llm_client = llm_client
        self.standard_categories = [
            "Enterprise Sales", "Sales Psychology", "Marketing",
            "Leadership", "Business Strategy", "Personal Growth",
            "Operations", "AI & Automation", "Human Behavior"
        ]

    def classify_signal(self, text_content: str) -> List[str]:
        """
        Classifies unstructured post text into standardized domain taxonomy tags.
        """
        if self.llm_client:
            try:
                # LLM semantic classification call (Abstracted representation)
                prompt = (
                    f"Analyze the following text and assign applicable categories from: "
                    f"{', '.join(self.standard_categories)}.\n\nText: {text_content[:500]}"
                )
                response = self.llm_client.generate(prompt)
                if response:
                    return [c.strip() for c in response.split(",") if c.strip()]
            except Exception:
                pass  # Fall back to keyword matcher on API error

        # Rule-based fallback matcher
        text_lower = text_content.lower()
        matched = []
        keyword_map = {
            "Enterprise Sales": ["sales", "selling", "prospect", "pipeline", "quota", "deal", "close"],
            "Sales Psychology": ["bias", "psychology", "behavior", "cognitive", "trust"],
            "Marketing": ["brand", "positioning", "copywriting", "audience", "campaign"],
            "Leadership": ["leader", "manage", "culture", "executive", "team", "ceo"],
            "Business Strategy": ["strategy", "revenue", "growth", "saas", "b2b", "profit"]
        }

        for category, keywords in keyword_map.items():
            if any(kw in text_lower for kw in keywords):
                matched.append(category)

        return matched if matched else ["General Business"]
