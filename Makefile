include .env
export

.PHONY: configure run migration

configure:
	@pip install -r requirements.txt
	@pip install -e .

run:
	@python dnscockpit/main.py

migration:
	@alembic revision --autogenerate -m "$(m)"
