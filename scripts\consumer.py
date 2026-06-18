#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой консьюмер для чтения CDC событий из Kafka
Запуск: python scripts/consumer.py
"""

from kafka import KafkaConsumer
import json
import sys

BOOTSTRAP = 'localhost:9092'
TOPICS = ['cdc.public.users', 'cdc.public.orders']

def main():
    print(f" Подключение к Kafka: {BOOTSTRAP}")
    print(f" Топики: {', '.join(TOPICS)}\n")
    
    consumer = KafkaConsumer(
        *TOPICS,
        bootstrap_servers=BOOTSTRAP,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=10000,  # 10 сек без данных = выход
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    try:
        for msg in consumer:
            val = msg.value
            op = val.get('op', '?')
            op_map = {'c': ' INSERT', 'u': ' UPDATE', 'd': ' DELETE', 'r': ' SNAPSHOT'}
            
            table = msg.topic.split('.')[-1]
            after = val.get('after', {})
            
            print(f"[{table:6}] {op_map.get(op, op):12} | {json.dumps(after, ensure_ascii=False)}")
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\n Прервано пользователем")
    finally:
        consumer.close()
        print(" Завершено")

if __name__ == '__main__':
    main()
