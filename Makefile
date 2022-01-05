package_name = webhook_telegram_bot
repository = toolen/webhook-telegram-bot
version = $(shell poetry version -s)
tag = $(repository):$(version)
hadolint_version=2.8.0
trivy_version=0.22.0

fmt:
	poetry run black .
	poetry run isort .
fmt-check:
	poetry run black . --check
	poetry run isort . --check
pre-commit:
	make fmt
	make lint
ci:
	make fmt-check
	make lint
lint:
	poetry run flake8 --ignore E501,W503 $(package_name)/ tests/
	make mypy
	make pydocstyle
	make test
	poetry run bandit -r $(package_name)
	poetry run safety check
	make radon
mypy:
	poetry run mypy --strict --no-warn-return-any $(package_name)
pydocstyle:
	poetry run pydocstyle --add-ignore=D104 $(package_name)/
test:
	poetry run pytest --cov=$(package_name) tests/
radon:
	poetry run radon cc --min C --show-complexity $(package_name)
	poetry run radon mi --min B $(package_name)
	poetry run radon raw --summary $(package_name) | tail -n12
image:
	export DOCKER_BUILDKIT=1
	make hadolint
	docker build --pull --no-cache -t $(tag) .
	make trivy
	make size
size:
	docker images | grep $(repository) | grep $(version)
trivy:
	trivy image $(tag)
hadolint:
	docker run --rm -i hadolint/hadolint:$(hadolint_version) < Dockerfile
push:
	docker trust sign $(tag)
ngrok:
	ngrok http --region=eu 8080