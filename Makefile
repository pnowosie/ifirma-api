# Don't afraid a Makefile
.PHONY: clear-dist dist publish test

clear-dist:
	rm -rf ./dist

dist:
	tox

publish: clear-dist dist
	py -m twine upload dist/*

test:
	py -m pytest -vv
