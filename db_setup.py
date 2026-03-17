#!/usr/bin/env python3
"""Create the tasks table and stored procedures in PostgreSQL."""

from db.connection import get_connection


def setup():
    conn = get_connection()
    cur = conn.cursor()

    # Create tasks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          SERIAL PRIMARY KEY,
            task_name   TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            deadline    DATE NOT NULL,
            is_done     BOOLEAN NOT NULL DEFAULT FALSE,
            created_at  TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """)

    # Stored procedure: add a new task
    cur.execute("""
        CREATE OR REPLACE PROCEDURE sp_add_task(
            p_task_name   TEXT,
            p_assigned_to TEXT,
            p_deadline    DATE
        )
        LANGUAGE plpgsql AS $$
        BEGIN
            INSERT INTO tasks (task_name, assigned_to, deadline)
            VALUES (p_task_name, p_assigned_to, p_deadline);
        END;
        $$;
    """)

    # Stored procedure: mark a task as done
    cur.execute("""
        CREATE OR REPLACE PROCEDURE sp_mark_task_done(p_task_id INT)
        LANGUAGE plpgsql AS $$
        BEGIN
            UPDATE tasks SET is_done = TRUE WHERE id = p_task_id;
        END;
        $$;
    """)

    # Stored function: get pending tasks
    cur.execute("""
        CREATE OR REPLACE FUNCTION fn_get_pending_tasks()
        RETURNS TABLE(
            id          INT,
            task_name   TEXT,
            assigned_to TEXT,
            created_at  TIMESTAMP,
            deadline    DATE,
            is_done     BOOLEAN
        )
        LANGUAGE plpgsql AS $$
        BEGIN
            RETURN QUERY
            SELECT t.id, t.task_name, t.assigned_to, t.created_at, t.deadline, t.is_done
            FROM tasks t
            WHERE t.is_done = FALSE
            ORDER BY t.deadline ASC;
        END;
        $$;
    """)

    # Stored function: get completed tasks
    cur.execute("""
        CREATE OR REPLACE FUNCTION fn_get_completed_tasks()
        RETURNS TABLE(
            id          INT,
            task_name   TEXT,
            assigned_to TEXT,
            created_at  TIMESTAMP,
            deadline    DATE,
            is_done     BOOLEAN
        )
        LANGUAGE plpgsql AS $$
        BEGIN
            RETURN QUERY
            SELECT t.id, t.task_name, t.assigned_to, t.created_at, t.deadline, t.is_done
            FROM tasks t
            WHERE t.is_done = TRUE
            ORDER BY t.created_at DESC;
        END;
        $$;
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Table 'tasks' and stored procedures created successfully.")


if __name__ == "__main__":
    setup()
