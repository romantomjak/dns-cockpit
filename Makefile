include .env
export

.PHONY: configure run migration

configure:
	@pip install -r requirements.txt
	@pip install -e .

run:
	@python dnscockpit/main.py

alembic-migration:
	@alembic revision --autogenerate -m "$(m)"

alembic-upgrade:
	@alembic upgrade head

alembic-downgrade:
	@alembic downgrade -1
