"""
Reframing Orchestrator Module (Engine 2.1)

Demonstrates the core AI orchestration pipeline:
1. Idea Extraction (decoupling logic from raw author wording).
2. 7-Angle Lab candidate evaluation.
3. Anti-AI-Slop scrub (removing corporate cliches and em dashes).
"""

from typing import Dict, Any, Optional


class ReframingOrchestrator:
    def __init__(self, llm_client: object, style_guide_content: str):
        self.llm_client = llm_client
        self.style_guide = style_guide_content

    def construct_reframing_prompt(
        self,
        source_text: str,
        category: str,
        target_angle: Optional[str] = None
    ) -> str:
        """Assembles the Engine 2.1 multi-stage reframing prompt."""

        angle_directive = ""
        if target_angle:
            angle_directive = f"\nMANDATE: Select candidate angle: {target_angle}."

        prompt = f"""
You are the Thought Leadership Reframing Engine (Engine 2.1).
Your task is NOT to rewrite or paraphrase the source text.
Your task is to extract the underlying business premise, discover the hidden human tension, and produce an original B2B LinkedIn post.

--- STYLE GUIDE & GOVERNANCE ---
{self.style_guide}

--- INPUT SIGNAL ---
CATEGORY: {category}
RAW TEXT:
{source_text}
{angle_directive}

--- REQUIRED OUTPUT FORMAT ---
FINAL_POST:
[Complete publish-ready post]

QUALITY_SCORE:
[Score 85-100]/100

HUMAN_INTEREST_SCORE:
[Score 8.0-10.0]/10

SELECTED_ANGLE:
[Contrarian | Experience / Story | Observation / Insight]

ONE_LINE_REASON:
[Brief explanation of conversational tension]
"""
        return prompt

    def sanitize_output(self, raw_post: str) -> str:
        """Enforces Anti-AI-Slop rules on generated post text."""
        # Rule: Remove em dashes in favor of standard typography
        cleaned = raw_post.replace("—", "-")

        # Rule: Strip common corporate AI slop phrases
        banned_phrases = [
            "In today's fast-paced world",
            "In the modern business landscape",
            "At the intersection of",
            "Drive meaningful outcomes",
            "Unlock potential"
        ]
        for phrase in banned_phrases:
            cleaned = cleaned.replace(phrase, "")

        return cleaned.strip()
