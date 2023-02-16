# check secrets to inject into .env
# VALUES: my (default) | kasia
# EXAMPLE: make env who=kasia 
who := my

PYTHON := ../.venv/bin/python 

venv:
	python -m venv .venv

install:
	# assumes venv activation
	pip install -U pip
	pip install -r requirements.txt

invoice:
	${PYTHON} main.py consensius.yml

check-month:
	@env $$(cat ".env") ${PYTHON} check_accounting_month.py

list-invoices:
	@env $$(cat ".env") ${PYTHON} list_invoices.py

# pseudo-automatic secret set
env:
	op inject -i "${who}.env" > .env
	@echo "env file created, don't forget to 'clean-env'"

clean-env:
	rm .env
	@echo "unset IFIRMA_API_KEY IFIRMA_abonent_API_KEY IFIRMA_API_USERNAME"
