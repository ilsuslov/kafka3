-- Пользователь для Debezium
CREATE USER debezium WITH REPLICATION PASSWORD 'debezium';

-- Права
GRANT CONNECT ON DATABASE testdb TO debezium;
GRANT USAGE ON SCHEMA public TO debezium;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO debezium;

-- Публикация для logical replication (только нужные таблицы!)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'dbz_pub') THEN
        CREATE PUBLICATION dbz_pub FOR TABLE users, orders;
    END IF;
END $$;

-- Права на публикацию
ALTER PUBLICATION dbz_pub OWNER TO debezium;
