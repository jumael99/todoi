# Todoi: A minimalistic todo list application

# Usage guideline
- Clone the repository
- In the root run: `pip install venv venv`
- Run `venv/bin/activate` to enter the virtual environment if you're using powershell(Google it to use virtual environment. Virtual environment helps to manage dependencies and packages)
- Run `pip install -r requirements.txt` to install the dependencies
- Run `uvicorn main:app --reload` to run the app

## Database Connection Details

- **Host**: `sql.freedb.tech`
- **Port**: `3306`
- **Database Name**: `freedb_qweqwe`
- **Database User**: `freedb_newxa`
- **Password**: `qHS5aHPr*%D!r6Z`


# API Reference

### Add Tasks

#### Create Today's Task
POST /addnewTask

Request body:
{
    "taskHeading": "Complete project documentation",
    "completedNote": ""
}

### Move Tasks

#### Move to Completed
POST /moveToCompleted/{task_id}
Moves a task from today's list to completed list

#### Move to Incomplete
POST /moveToIncomplete/{task_id}
Moves a task from today's list to incomplete list

#### Move Incomplete to Completed
POST /notepush/{task_id}
Moves a task from incomplete list to completed list

### Fetch Tasks

#### Get Today's Tasks
GET /fetchtodayTask
Returns full task objects

#### Get Today's Task Headings
GET /fetchtodayHeadings
Returns only task titles

#### Get Incomplete Tasks
GET /fetchincompletetask

#### Get Completed Tasks
GET /fetchcompletedtask

### Response Format

All task responses follow this format:
{
    "id": 1,
    "taskHeading": "Task title",
    "completedNote": "Optional completion note"
}

### Error Responses

- 404: Task not found
- 422: Invalid input data