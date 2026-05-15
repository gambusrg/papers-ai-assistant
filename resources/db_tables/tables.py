sql_statements = ["""CREATE TABLE IF NOT EXISTS conversations (
    id          TEXT PRIMARY KEY,
    paper_id    TEXT NOT NULL,
    user_id     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS messages (
    id                  TEXT PRIMARY KEY,
    conversation_id     TEXT NOT NULL REFERENCES conversations(id),
    role                TEXT NOT NULL,  -- 'user' | 'assistant'
    content             TEXT NOT NULL,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""]
