#!/usr/bin/env python3
"""Super Simple Customer Demo: The 'Goldfish & Elephant' Memory Pattern.

Demonstrates the dramatic contrast between:
1. Pure Goldfish Agent (stateless, forgets across sessions)
2. Goldfish + Elephant Agent (clean working memory + persistent long-term storage)
"""

from __future__ import annotations
import json
import time
from pathlib import Path


class ElephantMemoryStore:
    """The Elephant: Persistent storage across sessions (e.g. SQLite, JSON, or Vector DB)."""

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
        self.memory = self._load()

    def _load(self) -> dict:
        if self.filepath.exists():
            try:
                return json.loads(self.filepath.read_text())
            except Exception:
                return {}
        return {}

    def commit(self, key: str, value: str) -> None:
        """Stores a persistent fact that survives session restarts."""
        self.memory[key] = value
        self.filepath.write_text(json.dumps(self.memory, indent=2))

    def recall(self) -> dict:
        """Retrieves all persistent memories."""
        return self._load()

    def clear(self) -> None:
        if self.filepath.exists():
            self.filepath.unlink()
        self.memory = {}


class PureGoldfishAgent:
    """A standard agent with only in-memory context (RAM)."""

    def __init__(self) -> None:
        self.context_window = []

    def receive_message(self, text: str) -> str:
        self.context_window.append({"user": text})
        return "Understood. Noted in current working session."

    def reset_session(self) -> None:
        """Simulates starting a new chat or closing the window."""
        self.context_window = []  # Amnesia!

    def generate_code(self, prompt: str) -> str:
        # Without persistent memory, it defaults to generic defaults
        return (
            "import sqlite3\n"
            "# Default generic implementation (Forgot user preferences!)\n"
            "conn = sqlite3.connect('app.db')\n"
            "cursor = conn.cursor()\n"
            "cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))"
        )


class GoldfishElephantAgent:
    """The hybrid pattern: Fast Goldfish reasoning backed by persistent Elephant memory."""

    def __init__(self, elephant: ElephantMemoryStore) -> None:
        self.context_window = []  # Goldfish: clean & compact
        self.elephant = elephant  # Elephant: persistent storage

    def receive_message(self, text: str) -> str:
        self.context_window.append({"user": text})
        # Extract and commit key rules to Elephant memory
        if "postgresql" in text.lower():
            self.elephant.commit("database", "PostgreSQL (psycopg3)")
        if "no orm" in text.lower() or "raw sql" in text.lower():
            self.elephant.commit("orm_policy", "Raw SQL only (No ORMs)")
        if "3.11" in text.lower() or "typed" in text.lower():
            self.elephant.commit("language_standard", "Strict Typed Python 3.11+")

        return "Understood. Cached in working memory AND committed to Elephant persistent store."

    def reset_session(self) -> None:
        """Simulates starting a brand-new session tomorrow."""
        self.context_window = []  # Goldfish RAM wiped clean for fresh speed!

    def generate_code(self, prompt: str) -> str:
        # Just-in-time retrieval from the Elephant!
        facts = self.elephant.recall()
        return (
            f"# [ELEPHANT RECALL] Applied Persistent Rules:\n"
            f"# - DB Engine    : {facts.get('database', 'SQLite')}\n"
            f"# - Architecture : {facts.get('orm_policy', 'SQLAlchemy')}\n"
            f"# - Style Guide  : {facts.get('language_standard', 'Python 3')}\n\n"
            f"from typing import List, Dict, Any\n"
            f"import psycopg\n\n"
            f"def get_user_orders(conn: psycopg.Connection, user_id: str) -> List[Dict[str, Any]]:\n"
            f"    with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:\n"
            f"        cur.execute(\n"
            f"            'SELECT id, amount, status FROM orders WHERE user_id = %(uid)s',\n"
            f"            {{'uid': user_id}},\n"
            f"        )\n"
            f"        return cur.fetchall()\n"
        )


def run_demo() -> None:
    db_file = Path(__file__).parent / "elephant_memory.json"
    elephant = ElephantMemoryStore(db_file)
    elephant.clear()

    goldfish = PureGoldfishAgent()
    hybrid = GoldfishElephantAgent(elephant)

    print("=" * 72)
    print(" 🐟 VS 🐘 THE GOLDFISH & ELEPHANT MEMORY PATTERN DEMO")
    print("=" * 72)
    print("\n👉 SCENARIO: An engineering team establishes architectural preferences.")
    time.sleep(1)

    print("\n" + "—" * 72)
    print("📍 STEP 1: DAY 1 - TEACHING SESSION")
    print("—" * 72)
    instruction = (
        "We are migrating to PostgreSQL. Rule: Use strict typed Python 3.11+ "
        "and NEVER use ORMs (raw SQL only)."
    )
    print(f'User says:\n  "{instruction}"\n')

    print("[1] Pure Goldfish Agent response:")
    print("    ", goldfish.receive_message(instruction))
    print("\n[2] Goldfish + Elephant Agent response:")
    print("    ", hybrid.receive_message(instruction))
    print(f"    (Committed to disk: {db_file.name})")

    time.sleep(1.5)

    print("\n" + "—" * 72)
    print("📍 STEP 2: DAY 2 - STARTING A BRAND-NEW SESSION")
    print("—" * 72)
    print("Closing session window... Resetting context RAM...")
    goldfish.reset_session()
    hybrid.reset_session()
    print("Both agents now have an EMPTY active context window!\n")

    time.sleep(1.5)

    print("—" * 72)
    print("📍 STEP 3: DAY 2 - CODE GENERATION REQUEST")
    print("—" * 72)
    query = "Write a function to fetch user orders."
    print(f'User asks:\n  "{query}"\n')

    print("❌ [PURE GOLDFISH AGENT] (Suffers from stateless amnesia):")
    print("-" * 55)
    print(goldfish.generate_code(query))
    print("-" * 55)

    time.sleep(1.5)

    print("\n✅ [GOLDFISH + ELEPHANT AGENT] (Just-in-time long-term recall):")
    print("-" * 55)
    print(hybrid.generate_code(query))
    print("-" * 55)

    print("\n" + "=" * 72)
    print("🎯 TAKEAWAY FOR CUSTOMERS:")
    print("  1. The Goldfish keeps sessions fast, cheap, and hallucination-free.")
    print("  2. The Elephant ensures your enterprise standards are never forgotten.")
    print("=" * 72 + "\n")

    # Cleanup demo file
    elephant.clear()


if __name__ == "__main__":
    run_demo()
