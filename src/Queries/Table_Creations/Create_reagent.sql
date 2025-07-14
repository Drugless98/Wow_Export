

CREATE TABLE IF NOT EXISTS reagents(
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    recipe_id       INTEGER REFERENCES recipes(id),
    reagent_item_id INTEGER,
    reagent_count   INTEGER
)