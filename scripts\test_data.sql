-- Пользователи
INSERT INTO users (name, email) VALUES 
  ('John Doe', 'john@example.com'),
  ('Jane Smith', 'jane@example.com'),
  ('Alice Johnson', 'alice@example.com'),
  ('Bob Brown', 'bob@example.com');

-- Заказы
INSERT INTO orders (user_id, product_name, quantity) VALUES 
  (1, 'Product A', 2),
  (1, 'Product B', 1),
  (2, 'Product C', 5),
  (3, 'Product D', 3),
  (4, 'Product E', 4);
