include .env
export

.PHONY: configure run alembic-migration alembic-upgrade alembic-downgrade unit-tests

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

unit-tests:
	@pytest -sv tests/
