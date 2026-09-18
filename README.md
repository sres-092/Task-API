# Task API
I have built a task api which uses CRUD steps for a to do list a simple to do list which add uodate remove and take confirmation for task completion using boolean 

## Setup

```
git clone https://github.com/sres-092/Task-API.git
cd task-api
python -m venv venv
venv\Scripts\Activate.ps1 # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
fastapi dev main.py
```

Runs at http://127.0.0.1:8000 — interactive docs at /docs

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Get API information |
| GET | /health | Check the API is running |
| GET | /tasks | Get all tasks |
| GET | /tasks/{id} | Get a task by ID |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
 
## Swagger UI

![alt text](Swagger_1.png) ![alt text](Swagger_2.png)


## Example request

```
curl.exe -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{\"title\": \"Buy bread\"}'

HTTP/1.1 201 Created
date: Fri, 18 Sep 2026 08:55:09 GMT
server: uvicorn
content-length: 41
content-type: application/json

{"id":5,"title":"Buy bread","done":false}
```