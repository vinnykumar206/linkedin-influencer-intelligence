"""
Signal Filtering & Deduplication Module

Demonstrates business logic for:
1. Recency Gate: Rejecting signals older than 48 hours to maintain pipeline freshness.
2. Deduplication Ledger: Hashing post attributes to prevent duplicate processing.
"""

import re
import hashlib
from typing import List, Dict, Set


class SignalFilter:
    def __init__(self, processed_hashes: Set[str] = None):
        self.processed_hashes = processed_hashes or set()

    def is_within_48_hours(self, raw_time_descriptor: str) -> bool:
        """
        Parses relative timestamp text descriptors (e.g., '2h', '1d', '3d', '2w')
        to enforce a strict 48-hour recency window.
        """
        if not raw_time_descriptor:
            return True  # Default fallback if timestamp tag is ambiguous

        raw_time = raw_time_descriptor.strip().lower()

        # Reject explicitly stale time indicators (3+ days, weeks, months, years)
        stale_patterns = [
            r"[3-9]d", r"\d{2,}d",       # 3d, 4d, 10d...
            r"\dw", r"week",             # 1w, weeks
            r"\dmo", r"month",           # 1mo, months
            r"\dyr?", r"year",            # 1y, years
            r"[3-9]\s*days?\s*ago",
            r"\d{2,}\s*days?\s*ago"
        ]

        for pattern in stale_patterns:
            if re.search(pattern, raw_time):
                return False

        return True

    def generate_signal_hash(self, source_url: str, text_content: str) -> str:
        """Generates a deterministic hash for signal deduplication."""
        payload = f"{source_url}_{text_content[:120]}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]

    def filter_signals(self, raw_signals: List[Dict]) -> List[Dict]:
        """Filters out stale and duplicate market signals."""
        fresh_signals = []

        for signal in raw_signals:
            time_tag = signal.get("timestamp_descriptor", "")
            if not self.is_within_48_hours(time_tag):
                continue

            sig_hash = self.generate_signal_hash(
                signal.get("source_url", ""),
                signal.get("text", "")
            )

            if sig_hash in self.processed_hashes:
                continue

            self.processed_hashes.add(sig_hash)
            signal["signal_hash"] = sig_hash
            fresh_signals.append(signal)

        return fresh_signals
