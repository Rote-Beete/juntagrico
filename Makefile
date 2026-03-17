.PHONY: lint-check
lint-check:
	uv sync --no-default-groups --group dev
	uv run ruff check .
	uv run ruff format --check .
	uv run djlint --exclude '--none--' --use-gitignore --check . 

.PHONY: ruff
ruff:
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: djlint
djlint:
	uv run djlint --exclude '--none--' --use-gitignore --reformat .

.PHONY: test
test:
	uv sync --group test
	uv run python manage.py collectstatic --noinput
	uv run pytest
