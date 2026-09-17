from fastapi import FastAPI, HTTPException

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