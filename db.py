"""SQLite storage helpers for campaign data.

This module keeps database code simple and separate from agent logic.
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

DEFAULT_DB_PATH = os.getenv("CAMPAIGN_DB_PATH", "campaigns.db")


def _get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create a SQLite connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Create the campaigns table if it does not exist."""
    with _get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                idea_json TEXT NOT NULL,
                copy_json TEXT NOT NULL,
                plan_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_campaign(
    product: str,
    idea: Dict[str, Any],
    copy: Dict[str, Any],
    plan: Dict[str, Any],
    db_path: str = DEFAULT_DB_PATH,
) -> int:
    """Insert one campaign record and return its ID."""
    created_at = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    with _get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO campaigns (product, idea_json, copy_json, plan_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                product,
                json.dumps(idea),
                json.dumps(copy),
                json.dumps(plan),
                created_at,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def fetch_campaigns(db_path: str = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """Return all campaigns, newest first."""
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT id, product, idea_json, copy_json, plan_json, created_at
            FROM campaigns
            ORDER BY id DESC
            """
        ).fetchall()

    campaigns: List[Dict[str, Any]] = []
    for row in rows:
        campaigns.append(
            {
                "id": row["id"],
                "product": row["product"],
                "idea": json.loads(row["idea_json"]),
                "copy": json.loads(row["copy_json"]),
                "plan": json.loads(row["plan_json"]),
                "created_at": row["created_at"],
            }
        )
    return campaigns

def init_brand_table():
    conn = sqlite3.connect("campaigns.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS brand (
        brand TEXT PRIMARY KEY,
        tone TEXT,
        colors TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_brand(brand, tone, colors):
    conn = sqlite3.connect("campaigns.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO brand (brand, tone, colors)
    VALUES (?, ?, ?)
    """, (brand, tone, colors))

    conn.commit()
    conn.close()

    return {"status": "brand_saved"}


def get_brand(brand):
    conn = sqlite3.connect("campaigns.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM brand WHERE brand=?", (brand,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return {
            "brand": result[0],
            "tone": result[1],
            "colors": result[2]
        }
    return {"status": "not_found"}
