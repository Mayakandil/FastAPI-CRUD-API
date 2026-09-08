import sqlite3
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, Response

app = FastAPI()


def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Learn FastAPI", False),
                ("Build CRUD API", False),
                ("Push to GitHub", False)
            ]
        )

    conn.commit()
    conn.close()


init_db()


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


@app.get("/tasks", description="Get all tasks")
async def get_tasks():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        })

    return tasks


@app.get("/tasks/{id}", description="Get a task by ID")
async def taskid(id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"task {id} not found"}
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }


@app.post("/tasks", description="Create a new task")
async def create_tasks(data: dict = Body(...)):

    # validate title
    if (
        "title" not in data
        or not isinstance(data["title"], str)
        or not data["title"].strip()
    ):
        return JSONResponse(
            status_code=400,
            content={"error": "title is required"}
        )

    title = data["title"].strip()
    done = data.get("done", False)

    # validate done if provided
    if not isinstance(done, bool):
        return JSONResponse(
            status_code=400,
            content={"error": "done must be boolean"}
        )

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, done)
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    new_task = {
        "id": task_id,
        "title": title,
        "done": done
    }

    return JSONResponse(
        status_code=201,
        content=new_task
    )


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

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "task id not found"}
        )

    title = row["title"]
    done = bool(row["done"])

    # validate title
    if "title" in body:
        if (
            not isinstance(body["title"], str)
            or not body["title"].strip()
        ):
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid title"}
            )

        title = body["title"].strip()

    # validate done
    if "done" in body:
        if not isinstance(body["done"], bool):
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid done value"}
            )

        done = body["done"]

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
        """,
        (title, done, id)
    )

    conn.commit()
    conn.close()

    return {
        "id": id,
        "title": title,
        "done": done
    }


@app.delete("/tasks/{id}", description="Delete a task")
async def delete_task(id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()

        return JSONResponse(
            status_code=404,
            content={"error": "task not found"}
        )

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return Response(status_code=204)