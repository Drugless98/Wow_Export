SELECT
	time::date AS day,
	SUM(item_price) as total
FROM
	price_history
GROUP BY day
ORDER BY day;