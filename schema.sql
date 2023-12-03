
CREATE TABLE users (                                                        CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
    id SERIAL PRIMARY KEY,
    username TEXT,
    password VARCHAR(255)
);


CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT,
    group_id INTEGER REFERENCES groups(id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content VARCHAR(255)
);


CREATE TABLE project_files (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    audio BYTEA,
    comment TEXT
    
);

CREATE TABLE group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups(id),
    user_id INTEGER REFERENCES users(id)
);  