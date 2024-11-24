from fastapi import FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()
db = Prisma()

# Initialize Prisma
@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Pydantic models
class TaskCreate(BaseModel):
    taskHeading: str
    completedNote: str = ""

class TaskResponse(BaseModel):
    id: int
    taskHeading: str
    completedNote: str

class TaskMove(BaseModel):
    taskId: int
    completedNote: str = ""

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to Task Management API"}

# Add a new task to Today's Tasks
@app.post("/addnewTask", response_model=TaskResponse)
async def add_new_task(task: TaskCreate):
    new_task = await db.todaytask.create(
        data={
            "taskHeading": task.taskHeading,
            "completedNote": task.completedNote
        }
    )
    return new_task

@app.post("/moveToCompleted", response_model=TaskResponse)
async def move_to_completed(task_id: int):
    # Find the task in today's tasks
    task = await db.todaytask.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Create in completed tasks
    completed_task = await db.completedtask.create(
        data={
            "taskHeading": task.taskHeading,
            "completedNote": task.completedNote  # Preserve the original completedNote
        }
    )
    
    # Delete from today's tasks
    await db.todaytask.delete(where={"id": task_id})
    
    return completed_task

@app.post("/moveToIncomplete", response_model=TaskResponse)
async def move_to_incomplete(task_id: int):
    # Find the task in today's tasks
    task = await db.todaytask.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Create in incompleted tasks
    incomplete_task = await db.incompletedtask.create(
        data={
            "taskHeading": task.taskHeading,
            "completedNote": task.completedNote  # Preserve the original completedNote
        }
    )
    
    # Delete from today's tasks
    await db.todaytask.delete(where={"id": task_id})
    
    return incomplete_task

# Fetch all Today Task headings
@app.get("/fetchtodayHeadings", response_model=List[str])
async def fetch_today_headings():
    today_tasks = await db.todaytask.find_many()
    return [task.taskHeading for task in today_tasks]

# Fetch all Today's Tasks
@app.get("/fetchtodayTask", response_model=List[TaskResponse])
async def fetch_today_tasks():
    today_tasks = await db.todaytask.find_many()
    return today_tasks

# Fetch all Incompleted Tasks
@app.get("/fetchincompletetask", response_model=List[TaskResponse])
async def fetch_incomplete_tasks():
    incompleted_tasks = await db.incompletedtask.find_many()
    return incompleted_tasks

# Fetch all Completed Tasks
@app.get("/fetchcompletedtask", response_model=List[TaskResponse])
async def fetch_completed_tasks():
    completed_tasks = await db.completedtask.find_many()
    return completed_tasks

# Move task to Completed Task and remove from Incompleted Task
@app.post("/notepush", response_model=TaskResponse)
async def note_push(task_id: int):
    # Find the task in IncompletedTask
    task = await db.incompletedtask.find_unique(where={"id": task_id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Move task to Completed Task
    completed_task = await db.completedtask.create(
        data={
            "taskHeading": task.taskHeading,
            "completedNote": task.completedNote
        }
    )

    # Remove the task from IncompletedTask
    await db.incompletedtask.delete(where={"id": task_id})

    return completed_task



