CREATE TABLE IF NOT EXISTS items (
    id                INTEGER PRIMARY KEY,
    name              TEXT,
    rarety            INTEGER,
    vendor_sell_price BIGINT,
    vendor_buy_price  BIGINT
)