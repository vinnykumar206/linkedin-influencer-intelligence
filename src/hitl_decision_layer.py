"""
Human-in-the-Loop (HITL) Decision Layer Module

Demonstrates event callback routing for interactive mobile preview approvals, edits, and alternate angle generation.
"""

from typing import Dict, Any, Callable, Optional


class HITLWorkflowManager:
    def __init__(self, reframing_fn: Callable, publish_fn: Callable):
        self.reframing_fn = reframing_fn
        self.publish_fn = publish_fn
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def handle_callback_action(self, action_key: str, post_id: str, payload: Optional[str] = None) -> Dict[str, Any]:
        """
        Routes user mobile callback actions (Approve, Re-angle, Edit, Discard).
        """
        session_data = self.active_sessions.get(post_id, {})

        if action_key == "reframe":
            # Initiate primary AI reframing
            result = self.reframing_fn(session_data.get("original_text", ""))
            session_data.update(result)
            session_data["status"] = "Pending Approval"
            return {"status": "preview_updated", "data": session_data}

        elif action_key == "another_angle":
            # Re-run reframing with alternate candidate mandate
            result = self.reframing_fn(
                session_data.get("original_text", ""),
                mandate="Select alternative candidate angle from 7-Angle Lab"
            )
            session_data.update(result)
            session_data["status"] = "Angle Updated"
            return {"status": "preview_updated", "data": session_data}

        elif action_key == "custom_edit" and payload:
            # Re-run reframing incorporating user editorial text feedback
            result = self.reframing_fn(
                session_data.get("original_text", ""),
                custom_instructions=payload
            )
            session_data.update(result)
            session_data["status"] = "Edits Applied"
            return {"status": "preview_updated", "data": session_data}

        elif action_key == "publish":
            # Initiate publication pipeline
            success = self.publish_fn(session_data.get("post_text", ""))
            session_data["status"] = "Published" if success else "Publish Failed"
            return {"status": "published", "success": success}

        elif action_key == "skip":
            session_data["status"] = "Skipped"
            return {"status": "skipped"}

        return {"status": "unknown_action"}
