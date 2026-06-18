
### Запустить все сервисы
```bash
cd debezium-lab
docker-compose up -d

# Ждём ~30-60 сек пока всё поднимется
docker-compose ps  # все должны быть Up (healthy)


### Зарегистрировать Debezium Connector

# Ждём пока connect будет готов (проверяем curl)
sleep 15

curl -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @config/postgres-connector.json


### Проверить статус коннектора

curl -s http://localhost:8083/connectors/postgres-users-orders-connector/status | python3 -m json.tool

# Должно быть: "state": "RUNNING"



###  Добавить тестовые данные

# Способ 1: через docker exec
docker exec -i postgres psql -U postgres -d testdb < scripts/test_data.sql

# Способ 2: вручную
docker exec -it postgres psql -U postgres -d testdb
# затем вставить SQL из test_data.sql


### Запустить consumer

pip install -r requirements.txt
python scripts/consumer.py


### Проверить мониторинг

rometheus: http://localhost:9090 → Query: debezium_connector_TotalNumberOfEventsSeen
Grafana: http://localhost:3000 (admin/admin) → Dashboard → "Debezium CDC Monitor"

# 1. Коннектор запущен?
curl -s http://localhost:8083/connectors/postgres-users-orders-connector/status | grep -q RUNNING && echo " Connector OK" || echo " Connector FAIL"

# 2. Топики Kafka созданы?
docker exec kafka kafka-topics --bootstrap-server localhost:9092 --list | grep -E "cdc\.public\.(users|orders)" && echo " Topics OK" || echo " Topics FAIL"

# 3. Метрики собираются?
curl -s http://localhost:9404/metrics | grep -q debezium && echo " Metrics OK" || echo " Metrics FAIL"



# Обновить пользователя
docker exec -i postgres psql -U postgres -d testdb -c "UPDATE users SET name='John Updated' WHERE email='john@example.com';"

# Добавить новый заказ
docker exec -i postgres psql -U postgres -d testdb -c "INSERT INTO orders (user_id, product_name, quantity) VALUES (1, 'New Product', 10);"

# Удалить заказ
docker exec -i postgres psql -U postgres -d testdb -c "DELETE FROM orders WHERE id=1;"
