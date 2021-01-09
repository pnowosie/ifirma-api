venv:
	python -m venv .venv

install:
	# assumes venv activation
	pip install -U pip
	pip install -r requirements.txt

invoice:
	.venv/bin/python main.py consensius.yml

clean:
	rm -rf .venv
