from kube_launcher import launch_k8s_job
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
  task_id = launch_k8s_job(body.task, body.repo_url, body.model, body.github_token)
return {"task_id": task_id}

@app.get("/task-status/{task_id}") 
def task_status(task_id: str): 
  data = r.hgetall(f"task:{task_id}") 
  if not data: raise HTTPException(status_code=404, detail="Task not found") 
    return {k.decode(): v.decode() for k, v in data.items()}



