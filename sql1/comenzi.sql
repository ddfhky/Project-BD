SELECT order_id, o.customer_id, SUM(b.price) FROM order_book o JOIN order_to_book USING(order_id) JOIN book b USING(book_id) GROUP BY order_id, o.customer_id;

SELECT o.order_id, b.title FROM order_to_book o JOIN book b USING (book_id) ORDER BY o.order_id;

commit;

SELECT order_id, c.first_name || ' ' || c.last_name, SUM(b.price) FROM order_book o JOIN order_to_book USING(order_id) JOIN book b USING(book_id) JOIN customer c USING(customer_id) GROUP BY order_id, c.first_name, c.last_name;
commit;

