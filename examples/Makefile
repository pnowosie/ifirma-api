PYTHON := .venv/bin/python 

venv:
	python3 -m venv .venv

install: venv
	${PYTHON} -m pip install ..

# I'm using 1password-cli to inject environment variables to the python
# process. You can do without 1password by preparing `.env` file and task:
# `env $$(cat ".env") ${PYTHON} script-file.py`
invoice:
	op run --env-file op.env \
	 ${PYTHON} main.py consensius.yml

check-month:
	op run --env-file op.env \
	 ${PYTHON} check_accounting_month.py

list-invoices:
	op run --env-file op.env \
	 ${PYTHON} list_invoices.py

clean:
	rm -rf .venv
