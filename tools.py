"""Simulated MCP-style tools (DB + memory + brand store).

These are plain Python functions that ADK can call as tools.
"""

from typing import Any, Dict, List

from .db import fetch_campaigns, init_db, insert_campaign, save_brand, get_brand, init_brand_table

# Ensure DB is initialized as soon as tools module is loaded.
init_db()
init_brand_table()


def save_campaign(product: str, idea: Dict[str, Any], copy: Dict[str, Any], plan: Dict[str, Any]):
    try:
        campaign_id = insert_campaign(
            product=product,
            idea=idea,
            copy=copy,
            plan=plan,
        )
        return {"campaign_id": campaign_id}
    except Exception as e:
        return {"error": str(e)}


def get_campaigns() -> List[Dict[str, Any]]:
    """Return previously saved campaigns."""
    return fetch_campaigns()

def save_brand_tool(brand: str, tone: str, colors: str):
    return save_brand(brand, tone, colors)


def get_brand_tool(brand: str):
    return get_brand(brand)


def get_campaigns_tool():
    return fetch_campaigns()

def schedule_campaign_tool(product: str, schedule: str):
    return {
        "status": "scheduled",
        "product": product,
        "schedule": schedule
    }
