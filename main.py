tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False},
    {"id": 3, "title": "Push project to GitHub", "done": True}
]

from fastapi import FastAPI , Request
from fastapi.responses import JSONResponse ,Response

app = FastAPI()

@app.get("/") # "@" decorator , takes the function below and does something with it , in this case --> path "/" operation "get" decorator "@"
async def root(): # async == in hury , momken nshelha 3ady 
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{id}")
async def taskid(id:int):
    for task in tasks :
        if task["id"]== id:
            return task

    return JSONResponse(
        status_code=404, content={"error":f"task {id} not found "}
    )

@app.post("/tasks")
async def create_tasks(request: Request):
    data = await request.json()

    #vaidate title
    if "title" not in data or not data["title"].strip():
        return JSONResponse(status_code=400 , content={"error": "title is required"})

    #create the new task 
    new_task={
        "id":max(task["id"]for task in tasks)+1 , # akbar id 7 +1 --> new id 8 
        "title":data["title"],
        "done":False
    }


    #add it to our in memory list 
    tasks.append(new_task)

    #return 201 created 
    return JSONResponse(
        status_code=201, content = new_task
    )

@app.put("/tasks/{id}")
async def update_task(id:int , request: Request):
    #find the task 
    task = next ((task for task in tasks if task["id"]==id), None)

    if task is None:
        return JSONResponse(
            status_code=404, content={"error":"task id not found"}
        )

    try:
        body = await request.json()
    except:
        return JSONResponse(
            status_code=404,content={"error":"invalid request body"}

        )
    #body myst be non empty dictionary 
    if not isinstance(body,dict) or len(body)==0:
        return JSONResponse(
            status_code=404,content={"error":"invalid request body"}

        )
    #must contain either title or done 
    if "title" not in body or "done" not in body:
        return JSONResponse(
            status_code=400,
            content={"error": "Body must contain title and/or done"}
        )

    #validate title
    if "title" in body :
        if not isinstance(body["title"],str) or not body["title"].strip():
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid title"}
            )
        task["title"]=body["title"]

    #validate done
    if "done" in body :
        if not isinstance(body["done"],bool):
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid title"}
            )
    task["done"]=body["done"]

    return task

@app.delete("tasks/{id}")
async def delete_task(id:int):
    task = next((task for task in tasks if task["id"]==id), None)
    if task is None:
        return JSONResponse(
                status_code=404,
                content={"error": "task not found"}
            )
    tasks.remove(task)

    return Response(status_code=204)




