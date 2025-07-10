CREATE TABLE IF NOT EXISTS realms (
    id          INTEGER PRIMARY KEY,
    region_id   INTEGER REFERENCES regions(id),
    realm_name  TEXT NOT NULL,
    locale      TEXT NOT NULL
)