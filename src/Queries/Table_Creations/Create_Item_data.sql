CREATE TABLE IF NOT EXISTS item_data (
    item_id         INTEGER PRIMARY KEY,
    marketvalue     BIGINT NOT NULL,
    petSpeciesId    TEXT,
    quantity        BIGINT,
    avg_sale_price  BIGINT,
    sale_rate       FLOAT,
    sold_perday     FLOAT
)