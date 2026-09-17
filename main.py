from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

app = FastAPI()
tasks = [{"id": 1, "title": "Clg Studies", "done": True}, {"id": 2, "title": "Workout", "done": True}, {"id": 3, "title": "Grocery Shopping", "done": False}]


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0.0", "endpoints":["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task in tasks:
       if task["id"] == id:
          return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title is required")
    new_task = {"id": len(tasks) + 1, "title": task.title, "done": False}
    tasks.append(new_task)
    return new_task