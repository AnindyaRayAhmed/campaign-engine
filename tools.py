"""Simulated MCP-style tools.

These are plain Python functions that ADK can call as tools.
"""

from typing import Any, Dict, List

from db import fetch_campaigns, init_db, insert_campaign

# Ensure DB is initialized as soon as tools module is loaded.
init_db()


def save_campaign(data: Dict[str, Any]) -> Dict[str, Any]:
    """Save one campaign and return a small confirmation payload.

    Expected data format:
    {
      "product": "...",
      "idea": {...},
      "copy": {...},
      "plan": {...}
    }
    """
    required_keys = ["product", "idea", "copy", "plan"]
    missing = [k for k in required_keys if k not in data]
    if missing:
        return {
            "ok": False,
            "error": f"Missing keys: {', '.join(missing)}",
        }

    campaign_id = insert_campaign(
        product=str(data["product"]),
        idea=dict(data["idea"]),
        copy=dict(data["copy"]),
        plan=dict(data["plan"]),
    )
    return {"ok": True, "campaign_id": campaign_id}


def get_campaigns() -> List[Dict[str, Any]]:
    """Return previously saved campaigns."""
    return fetch_campaigns()
