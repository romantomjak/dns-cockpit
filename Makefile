include .env
export

.PHONY: configure run

configure:
	@pip install -r requirements.txt
	@pip install -e .

run:
	@python dnscockpit/main.py

