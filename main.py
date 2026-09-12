from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response
from repository import ( get_all_tasks , get_task_by_id , create_task , delete_task  as delete_task_from_db, update_task as update_task_from_db)

app = FastAPI()

@app.get("/", description="Welcome message for the Task API")
async def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
async def health():
    return {"status": "ok"}

# GET all tasks
@app.get("/tasks", description="Get all tasks")
async def get_tasks():
    return get_all_tasks()
    

#GET task by id 
@app.get("/tasks/{id}", description="Get a task by ID")
async def taskid(id: int):
    task = get_task_by_id(id)
    if task is None:
        return JSONResponse(
            status_code=404, content={"error":f"task {id} not found"}
        )
    return task
  

# CREATE taks 
@app.post("/tasks", description="Create a new task")
async def create_tasks(data: dict = Body(...)): # el data el hategy men request body fel url w (...) m3naha enha required 

    # validate title
    if (
        "title" not in data # body mafhosh klmet data aslan returns true or false
        or not isinstance(data["title"], str) #title is not string 
        or not data["title"].strip()
    ):
        return JSONResponse(
            status_code=400, # bad request , el user b3at data ghalat 
            content={"error": "title is required"}
        )

    title = data["title"].strip()
    done = data.get("done", False)
    #get done 3alshan done de optional aslon momken matb2ash mawgoda fa in this case hanakhod el default which is False --> dictionary.get(key, default_value) 

    # validate done if provided
    if not isinstance(done, bool): # law done msh true or false -->
        return JSONResponse(
            status_code=400,
            content={"error": "done must be boolean"}
        )

    new_task= create_task(title , done)


    return JSONResponse(
        status_code=201,
        content=new_task
    )

#UPDATE task 
@app.put("/tasks/{id}", description="Update an existing task by ID")
async def update_task(id: int, body: dict = Body(...)):

    # validate body
    if not isinstance(body, dict) or len(body) == 0:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid request body"}
        )

    if "title" not in body and "done" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "Body must contain title and/or done"}
        )

    existing_task = get_task_by_id(id)

    if existing_task is None:
        return JSONResponse(
            status_code=404,
            content={"error": "task id not found"}
        )

    title = existing_task["title"]
    done = existing_task["done"]

    # validate title
    if "title" in body:
        if (
            not isinstance(body["title"], str)
            or not body["title"].strip()
        ):
           
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid title"}
            )

        title = body["title"].strip()

    # validate done
    if "done" in body:
        if not isinstance(body["done"], bool):
            
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid done value"}
            )

        done = body["done"]
    uptask = update_task_from_db(id,title, done)

    return uptask


#DELETE task
@app.delete("/tasks/{id}", description="Delete a task")
async def delete_task(id: int):
    existing_task = get_task_by_id(id)
    if existing_task is None:
        return JSONResponse(
                    status_code=404,
                    content={"error": "task not found"}
                )
    delete_task_from_db(id)
    return Response(status_code=204)





