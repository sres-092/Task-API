from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
app = FastAPI(title="Task API", description="A simple task management API", version="1.0.0")
#tasks = [{"id": 1, "title": "Clg Studies", "done": True}, {"id": 2, "title": "Workout", "done": True}, {"id": 3, "title": "Grocery Shopping", "done": False}]
def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            done BOOLEAN 
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()["count"]
    if count == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Clg Studies", True))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Workout", True))
        cursor.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Grocery Shopping", False))
    conn.commit()
    conn.close()

init_db()

@app.get("/", summary="Get API information")
async def root():
    return {"name": "Task API", "version": "1.0.0", "endpoints":["/tasks"]}

@app.get("/health", summary="Check the API is running")
async def health_check():
    return {"status": "ok"}

@app.get("/tasks", summary="Get all tasks")
async def get_tasks():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/tasks/{id}", summary="Get a task by ID", responses={404: {"description": "Task not found"}})
async def get_task(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)

@app.post("/tasks", status_code=201, summary="Create a new task", responses={400: {"description": "Task title is required"}})
async def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, False))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "title": task.title, "done": False}

@app.delete("/tasks/{id}", status_code=204, summary="Delete a task", responses={404: {"description": "Task not found"}})
async def delete_task(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{id}", summary="Update a task", responses={400: {"description": "Task title is required"}, 404: {"description": "Task not found"}})
async def update_task(id: int, task_update: TaskUpdate):
    if not task_update.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (task_update.title, task_update.done, id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": id, "title": task_update.title, "done": task_update.done}
