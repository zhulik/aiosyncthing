lint: black isort pylint flake8

format:
	pipenv run black .
	pipenv run isort .

black:
	pipenv run black --check .

isort:
	pipenv run isort --check .

flake8:
	pipenv run flake8 aiophotoprism

pylint:
	pipenv run pylint aiophotoprism

lint: pylint flake8 isort black

test:
	pipenv run pytest

check: lint test

dist:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine check dist/*

.PHONY: black isort flake8 pylint lint format dist lint check
