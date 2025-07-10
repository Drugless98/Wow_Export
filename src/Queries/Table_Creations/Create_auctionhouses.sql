CREATE TABLE auctionhouses (
    id          INTEGER PRIMARY KEY,
    realm_id    INTEGER REFERENCES realms(id),
    faction     TEXT NOT NULL
);