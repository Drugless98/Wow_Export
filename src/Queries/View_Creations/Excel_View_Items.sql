CREATE VIEW excel_export AS
    SELECT 
        item_D.id,
        item_D.name,
        item_D.vendor_sell_price,
        item_D.vendor_buy_price,
        item_P.marketvalue,
        item_P.quantity,
        item_P.avg_sale_price,
        item_P.sale_rate,
        item_P.sold_perday,
        item_P.min_buyout
    FROM
        item_prices item_P
    JOIN
        items item_D ON item_P.item_id = item_D.id
    WHERE
        item_P.sale_rate > 0.1;
