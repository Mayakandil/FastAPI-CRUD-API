CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY ,
    title TEXT NOT NULL ,
    done BOOLEAN NOT NULL DEFAULT FALSE 

);
-- SERIAL --> ID automaticaly 1,2,3 , auto increment 