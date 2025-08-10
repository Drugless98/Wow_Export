CREATE VIEW tradeskill_history AS 
SELECT 
    ph.item_id,
    ph.item_price,
    ph.time,
    items.name,
    items.class,
    items.subclass
FROM 
    price_history AS ph
LEFT JOIN items as items   
    ON ph.item_id = items.id
WHERE 
    items.class = 'Tradeskill';