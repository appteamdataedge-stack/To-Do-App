"""All database operations — calls stored procedures/functions in PostgreSQL."""

from datetime import date
from db.connection import get_connection


def add_task(task_name: str, assigned_to: str, deadline: date) -> None:
    """Call sp_add_task stored procedure."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("CALL sp_add_task(%s, %s, %s)", (task_name, assigned_to, deadline))
        conn.commit()
        cur.close()
    finally:
        conn.close()


def get_pending_tasks() -> list[dict]:
    """Call fn_get_pending_tasks stored function."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM fn_get_pending_tasks()")
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return rows
    finally:
        conn.close()


def get_completed_tasks() -> list[dict]:
    """Call fn_get_completed_tasks stored function."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM fn_get_completed_tasks()")
        columns = [desc[0] for desc in cur.description]
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        cur.close()
        return rows
    finally:
        conn.close()


def mark_task_done(task_id: int) -> None:
    """Call sp_mark_task_done stored procedure."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("CALL sp_mark_task_done(%s)", (task_id,))
        conn.commit()
        cur.close()
    finally:
        conn.close()
