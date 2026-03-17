# To-Do App

A simple task tracking web application built with **Python**, **Streamlit**, and **PostgreSQL**.

---

## Features

### Page 1 — Home (Active Tasks)
- **Add Task** form at the top with three fields:
  - Task Name
  - Assigned To
  - Deadline (date)
  - Save button to persist the task
- **Active task list** showing only incomplete tasks, each row displaying:
  - An `isDone` toggle (circle/radio button) — clicking it marks the task as complete and **immediately removes it from the home page**
  - Task Name
  - Notes / description field
- Only pending (incomplete) tasks are visible here

### Page 2 — All Tasks
- **Two tabs:**
  - `Completed Tasks` — tasks marked as done
  - `Pending Tasks` — tasks not yet completed
- **Table columns:**
  | Column | Description |
  |---|---|
  | Task Name | Name of the task |
  | Assigned To | Person responsible |
  | Create Date | Date the task was created |
  | Deadline | Target completion date |
  | Over Due By | Number of days past the deadline (e.g. `2 days`, `0 days`) |
- All columns are **sortable** and **searchable** directly from the column headers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Streamlit (Python) |
| Backend | Python |
| Database | PostgreSQL |

---

## Data Model (Overview)

The app stores tasks with the following attributes:

| Field | Type | Notes |
|---|---|---|
| `id` | integer | Primary key, auto-increment |
| `task_name` | text | Name of the task |
| `assigned_to` | text | Person the task is assigned to |
| `deadline` | date | Target completion date |
| `is_done` | boolean | False = pending, True = completed |
| `created_at` | timestamp | Auto-set on insert |

---

## Pages / Navigation

```
App
├── Home          (Page 1 — active/pending tasks + add task form)
└── All Tasks     (Page 2 — completed & pending tabs with full table)
```

---

## Setup & Installation

> Prerequisites: Python 3.9+, PostgreSQL running locally or via a connection string.

```bash
# 1. Clone the repo
git clone <repo-url>
cd To-Do-App

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure the database connection
#    Copy the example env file and fill in your PostgreSQL credentials
cp .env.example .env

# 5. Run database migrations / setup
python db_setup.py

# 6. Launch the app
streamlit run app.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `DB_HOST` | PostgreSQL host (e.g. `localhost`) |
| `DB_PORT` | PostgreSQL port (default `5432`) |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASSWORD` | Database password |

---

## Project Structure (Planned)

```
To-Do-App/
├── app.py              # Streamlit entry point, page routing
├── pages/
│   ├── home.py         # Page 1 — active tasks + add task form
│   └── all_tasks.py    # Page 2 — completed & pending tabs
├── db/
│   ├── connection.py   # PostgreSQL connection helper
│   └── queries.py      # All SQL queries
├── db_setup.py         # Creates tables on first run
├── requirements.txt
├── .env.example
└── README.md
```
