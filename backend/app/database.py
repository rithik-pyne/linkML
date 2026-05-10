"""
Database connection and query utilities for SQLite
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

# Database path relative to backend directory
DB_PATH = Path(__file__).parent.parent / "clinical_data.db"


def get_db_connection() -> sqlite3.Connection:
    """
    Get SQLite database connection with row factory for dict-like access

    Returns:
        sqlite3.Connection: Database connection with Row factory
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def execute_query(sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute SQL query and return results as list of dicts

    Args:
        sql: SQL query string
        params: Query parameters (use ? placeholders)

    Returns:
        List of dictionaries with query results
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        # Convert Row objects to dicts
        return [dict(row) for row in rows]
    finally:
        conn.close()


def execute_query_one(sql: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """
    Execute SQL query and return single result as dict

    Args:
        sql: SQL query string
        params: Query parameters (use ? placeholders)

    Returns:
        Dictionary with query result or None if no result
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def test_connection() -> Dict[str, Any]:
    """
    Test database connection and return basic stats

    Returns:
        Dictionary with database statistics
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Get table counts
        tables = [
            'Patient', 'ImagingStudy', 'Biopsy', 'MolecularTest',
            'Mutation', 'Treatment', 'ImagingResponse', 'MolecularResponse',
            'ClinicalResponse', 'ClinicalAssessment'
        ]

        stats = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = cursor.fetchone()
            stats[table] = result['count'] if result else 0

        # Get patient IDs
        cursor.execute("SELECT patient_id FROM Patient ORDER BY patient_id LIMIT 5")
        patients = [row['patient_id'] for row in cursor.fetchall()]

        return {
            "status": "connected",
            "database": str(DB_PATH),
            "table_counts": stats,
            "sample_patients": patients
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        conn.close()