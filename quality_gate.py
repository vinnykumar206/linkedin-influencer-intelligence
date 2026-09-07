"""
Quality Gate Parsing & Evaluation Module

Demonstrates metadata parsing and quality threshold evaluation for generated posts.
"""

import re
from typing import Dict, Any


class QualityGate:
    def __init__(self, min_human_interest_score: float = 8.0, min_quality_score: int = 85):
        self.min_human_interest_score = min_human_interest_score
        self.min_quality_score = min_quality_score

    def parse_engine_output(self, raw_llm_output: str) -> Dict[str, Any]:
        """
        Extracts structured score metadata and text blocks from LLM engine response.
        """
        post_match = re.search(
            r"FINAL_POST:\s*(.*?)(?=(?:QUALITY_SCORE:|HUMAN_INTEREST_SCORE:|SELECTED_ANGLE:|ONE_LINE_REASON:|$))",
            raw_llm_output,
            re.DOTALL | re.IGNORECASE
        )
        quality_match = re.search(r"QUALITY_SCORE:\s*([0-9]{1,3})", raw_llm_output, re.IGNORECASE)
        hi_match = re.search(r"HUMAN_INTEREST_SCORE:\s*([0-9]+(?:\.[0-9]+)?)", raw_llm_output, re.IGNORECASE)
        angle_match = re.search(r"SELECTED_ANGLE:\s*(.*)", raw_llm_output, re.IGNORECASE)
        reason_match = re.search(r"ONE_LINE_REASON:\s*(.*)", raw_llm_output, re.IGNORECASE)

        final_post = post_match.group(1).strip() if post_match else raw_llm_output.strip()
        quality_score = int(quality_match.group(1)) if quality_match else 85
        hi_score = float(hi_match.group(1)) if hi_match else 8.0
        angle = angle_match.group(1).strip() if angle_match else "Observation / Insight"
        reason = reason_match.group(1).strip() if reason_match else ""

        # Enforce Anti-AI-Slop typography rule
        final_post = final_post.replace("—", "-")

        passed_gate = (hi_score >= self.min_human_interest_score) and (quality_score >= self.min_quality_score)

        return {
            "post_text": final_post,
            "quality_score": f"{quality_score}/100",
            "human_interest_score": f"{hi_score}/10",
            "selected_angle": angle,
            "angle_reason": reason,
            "passed_quality_gate": passed_gate
        }
