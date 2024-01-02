PYTHON := ../.venv/bin/python 

venv:
	python3 -m venv .venv

install: venv
	${PYTHON} -m pip install -e git+https://github.com/pnowosie/ifirma-api.git#egg=pnowosie.ifirma-api

invoice:
	${PYTHON} main.py consensius.yml

check-month:
	@env $$(cat ".env") ${PYTHON} check_accounting_month.py

list-invoices:
	@env $$(cat ".env") ${PYTHON} list_invoices.py

clean:
	rm -rf .venv

clean-env:
	rm .env
	@echo "unset IFIRMA_API_KEY IFIRMA_abonent_API_KEY IFIRMA_API_USERNAME"
