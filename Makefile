# Don't afraid a Makefile
.PHONY: test dist

install:
	@asdf install
	@echo "Make sure your python interpreter matches the project version"
	@echo "Shell -> $$(python -V) == $$(head -1 .tool-versions) <- Required"

proj_bootstrap:
	pip install --upgrade pip
	pip install --user --upgrade pipenv

deps:
	pipenv install --dev
	@echo "Source to project venv:  pipenv shell"

clear-dist:
	rm -rf ./dist

dist:
	python3 setup.py sdist bdist_wheel

publish: clear-dist dist
	python3 -m twine upload dist/*

test:
	@python -m pytest -vv
