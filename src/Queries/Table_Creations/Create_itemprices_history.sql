CREATE TABLE IF NOT EXISTS price_history(
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id     INTEGER,
    item_price  BIGINT,
    time        TEXT
);