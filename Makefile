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


PYTEST_MARKERS ?= not wip
.PHONY: test
test:
	uv sync --group test
	ROTEBEETE_ENV_FILE=.env.test uv run python manage.py collectstatic --noinput
	ROTEBEETE_ENV_FILE=.env.test uv run pytest -m "$(PYTEST_MARKERS)"

.PHONY: test-only
test-only:
	$(MAKE) test PYTEST_MARKERS="only"

.PHONY: dev
dev:
	docker compose -f docker-compose.dev.yml up --pull always  --build --watch
	docker compose -f docker-compose.dev.yml down

.PHONY: pre-push
pre-push:
# 	$(MAKE) lint-check
	$(MAKE) test
