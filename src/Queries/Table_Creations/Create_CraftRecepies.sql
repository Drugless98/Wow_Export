

CREATE TABLE IF NOT EXISTS recipes (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    crafted_item_id INTEGER UNIQUE,
    spell_id        INTEGER,
    crafted_count   INTEGER      
)