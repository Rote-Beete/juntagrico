DOCKER_COMPOSE=docker compose -f docker-compose.dev.yml


.PHONY: lint-check
lint-check:
	uv sync --no-default-groups --group dev
	uv run ruff check .
	uv run ruff format --check .
	uv run djlint --exclude '--none--' --use-gitignore --check ./biddings 

.PHONY: ruff
ruff:
	uv run ruff check . --fix
	uv run ruff format .

.PHONY: djlint
djlint:
	uv run djlint --exclude '--none--' --use-gitignore --reformat ./biddings 


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
	${DOCKER_COMPOSE} up --build --watch
	${DOCKER_COMPOSE} down

.PHONY: pre-push
pre-push:
	$(MAKE) lint-check
	$(MAKE) test

.PHONY: replace-db
replace-db:
	@test -n "$(DUMP_FILE)" || (echo "Error: DUMP_FILE is required"; exit 1)

	${DOCKER_COMPOSE} exec postgres psql -U rb -d postgres -c "DROP DATABASE rb;"
	${DOCKER_COMPOSE} exec postgres psql -U rb -d postgres -c "CREATE DATABASE rb;"
	cat ${DUMP_FILE} | ${DOCKER_COMPOSE} exec -T postgres pg_restore -U rb -d rb --no-owner --no-privileges --disable-triggers

.PHONY: remove-biddings-tables
remove-biddings-tables:
	${DOCKER_COMPOSE} exec backend rotebeete migrate biddings zero
