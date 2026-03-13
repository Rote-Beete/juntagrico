.PHONY: lint-check
lint-check:
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run djlint --exclude '--none--' --use-gitignore --check . 

.PHONY: ruff
ruff:
	poetry run ruff check . --fix
	poetry run ruff format .

.PHONY: djlint
djlint:
	poetry run djlint --exclude '--none--' --use-gitignore --reformat .

.PHONY: test
test:
	poetry install --with=test
	poetry run python manage.py collectstatic --noinput
	poetry run pytest
