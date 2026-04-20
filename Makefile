.PHONY: up down logs migrate test shell-orders kafka-topics kafka-consume redis-cli

up:           ## Levantar toda la infraestructura
	docker compose up -d

down:         ## Detener todo
	docker compose down

logs:         ## Ver logs de todos los servicios
	docker compose logs -f

migrate:      ## Ejecutar migraciones de todos los servicios
	docker compose exec orders-service alembic upgrade head
	docker compose exec users-service alembic upgrade head
	docker compose exec products-service alembic upgrade head
	docker compose exec payments-service alembic upgrade head
	docker compose exec inventory-service alembic upgrade head
	docker compose exec notifications-service alembic upgrade head
	docker compose exec analytics-service alembic upgrade head

test:         ## Ejecutar tests
	docker compose exec orders-service pytest

shell-orders: ## Abrir shell en el servicio de pedidos
	docker compose exec orders-service bash

kafka-topics: ## Listar topics de Kafka
	docker compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

kafka-consume: ## Consumir un topic manualmente (TOPIC=order.order.created)
	docker compose exec kafka kafka-console-consumer \
	--bootstrap-server localhost:9092 \
	--topic $(TOPIC) --from-beginning

redis-cli:    ## Abrir redis CLI
	docker compose exec redis redis-cli
