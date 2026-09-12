import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DATABASE_URL)

#get all tasks
def get_all_tasks():
    with get_connection() as conn:# opens a connection with the data base 
        with conn.cursor(row_factory=dict_row) as cursor:   #cursor howa el connection aw el tool el btt3amel m3 el sql commandas and returns the answer
            cursor.execute("SELECT id , title , done FROM tasks ORDER BY id")
            tasks = cursor.fetchall() 
    return tasks   

            #returns all the rows into tasks
# we use with so that when el curson is done excuting it automaticaly closes men gher ma a7tag a2felo ana 

    
#get one task by ID
def get_task_by_id(task_id):
    with get_connection() as conn:
        with conn.cursor(row_factory = dict_row) as cursor:
            cursor.execute("SELECT id , title , done FROM tasks WHERE id = %s",(task_id,))
            task= cursor.fetchone()
    return task



#create task 
def create_task(title,done):
    with get_connection()as conn:
        with conn.cursor(row_factory=dict_row)as cursor:
            cursor.execute("INSERT INTO tasks (title , done) VALUES (%s,%s) RETURNING id , title , done ",(title,done))
            new_task = cursor.fetchone()
    return new_task



#update task
def update_task(task_id , title , done):
    with get_connection()as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("UPDATE tasks SET title=%s , done=%s WHERE id = %s RETURNING id , title , done" , (title , done , task_id))
            updated_task= cursor.fetchone()
    return updated_task


#delet task
def delete_task(task_id):
    with get_connection()as conn:
        with conn.cursor(row_factory=dict_row)as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            deleted_task= cursor.rowcount > 0 # kam satr et2asar bel command da if more than zero hayreturn true else false 
    return deleted_task
    
#sqlite --> WHERE id=? 
#postgresql --> WHERE id= %s

 