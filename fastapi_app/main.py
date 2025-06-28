from fastapi import FastAPI, BackgroundTasks, HTTPException 
from pydantic import BaseModel 
import redis 
import uuid 
import subprocess 
import os

app = FastAPI() 
r = redis.Redis(host="localhost", port=6379, db=0)

class TaskRequest(BaseModel): 
  repo_url: str = None  # optional; can be blank to create from scratch 
  task: str model: str = "devstral" 
  github_token: str = None  # optional for PR creation

@app.post("/submit-task") 
def submit_task(body: TaskRequest): 
  task_id = str(uuid.uuid4()) 
  r.hset(f"task:{task_id}", mapping={"status": "queued"})

cmd = [
    "docker", "run", "--rm",
    "-v", f"/tmp/projects/{task_id}:/workspace",
    "-e", f"REPO_URL={body.repo_url or ''}",
    "-e", f"TASK={body.task}",
    "-e", f"MODEL={body.model}",
    "-e", f"TASK_ID={task_id}",
    "-e", f"GITHUB_TOKEN={body.github_token or ''}",
    "openhands-runner:latest"
]

subprocess.Popen(cmd)
return {"task_id": task_id}

@app.get("/task-status/{task_id}") 
def task_status(task_id: str): 
  data = r.hgetall(f"task:{task_id}") 
  if not data: raise HTTPException(status_code=404, detail="Task not found") 
    return {k.decode(): v.decode() for k, v in data.items()}

                                                   
