CREATE TABLE IF NOT EXISTS item_prices (
    id              INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    item_id         INTEGER UNIQUE,
    marketvalue     BIGINT,
    min_buyout      BIGINT,
    quantity        BIGINT,
    avg_sale_price  BIGINT,
    sale_rate       FLOAT,
    sold_perday     FLOAT
)