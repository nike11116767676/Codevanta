import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from config import DB_PATH, BASE_DIR

ERRORS_JSON_PATH = BASE_DIR / "database" / "errors.json"
CONCEPTS_JSON_PATH = BASE_DIR / "database" / "concepts.json"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create errors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS errors (
            id TEXT PRIMARY KEY,
            language TEXT,
            pattern TEXT,
            error_type TEXT,
            title TEXT,
            explanation TEXT,
            cause TEXT,
            solution TEXT,
            concept TEXT,
            difficulty TEXT
        )
    """)

    # Create concepts & quizzes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concepts (
            id TEXT PRIMARY KEY,
            title TEXT,
            language TEXT,
            what_happened TEXT,
            why_it_happened TEXT,
            wrong_example TEXT,
            correct_example TEXT,
            memory_rule TEXT,
            quiz_json TEXT
        )
    """)

    # Create error history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            language TEXT,
            error_id TEXT,
            error_title TEXT,
            line INTEGER,
            code_snippet TEXT
        )
    """)

    conn.commit()

    # Seed errors if empty
    cursor.execute("SELECT COUNT(*) FROM errors")
    if cursor.fetchone()[0] == 0 and ERRORS_JSON_PATH.exists():
        with open(ERRORS_JSON_PATH, "r", encoding="utf-8") as f:
            errors_data = json.load(f)
            for err in errors_data:
                cursor.execute("""
                    INSERT OR REPLACE INTO errors (id, language, pattern, error_type, title, explanation, cause, solution, concept, difficulty)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    err["id"], err["language"], err.get("pattern", ""), err["error_type"],
                    err["title"], err["explanation"], err["cause"], err["solution"],
                    err.get("concept", ""), err.get("difficulty", "beginner")
                ))

    # Seed concepts if empty
    cursor.execute("SELECT COUNT(*) FROM concepts")
    if cursor.fetchone()[0] == 0 and CONCEPTS_JSON_PATH.exists():
        with open(CONCEPTS_JSON_PATH, "r", encoding="utf-8") as f:
            concepts_data = json.load(f)
            for c in concepts_data:
                quiz_str = json.dumps(c.get("quiz", {}))
                cursor.execute("""
                    INSERT OR REPLACE INTO concepts (id, title, language, what_happened, why_it_happened, wrong_example, correct_example, memory_rule, quiz_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    c["id"], c["title"], c.get("language", "all"),
                    c["what_happened"], c["why_it_happened"],
                    c["wrong_example"], c["correct_example"],
                    c["memory_rule"], quiz_str
                ))

    conn.commit()
    conn.close()

def find_error_rule(language: str, raw_message: str) -> Optional[Dict[str, Any]]:
    """Matches a compiler/runtime error message against patterns in the knowledge base."""
    import re
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM errors WHERE language = ?", (language.lower(),))
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        pattern = row["pattern"]
        if pattern and re.search(pattern, raw_message, re.IGNORECASE):
            return dict(row)

    return None

def get_concept(concept_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concepts WHERE id = ?", (concept_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        data = dict(row)
        if data.get("quiz_json"):
            data["quiz"] = json.loads(data["quiz_json"])
        return data
    return None

def record_error_history(language: str, error_id: str, error_title: str, line: Optional[int], code_snippet: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO error_history (language, error_id, error_title, line, code_snippet)
        VALUES (?, ?, ?, ?, ?)
    """, (language, error_id, error_title, line or 0, code_snippet[:200]))
    conn.commit()
    conn.close()

def get_all_error_history(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM error_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
