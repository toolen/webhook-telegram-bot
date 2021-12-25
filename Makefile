package_name = webhook_telegram_bot
repository = toolen/webhook-telegram-bot
version = $(shell poetry version -s)
tag = $(repository):$(version)

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
	poetry run flake8 --ignore E501 $(package_name)/ tests/
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
	docker build -t $(tag) .
size:
	docker images | grep $(repository) | grep $(version)
scan:
	trivy image $(tag)
push:
	docker trust sign $(tag)
ngrok:
	ngrok http --region=eu 8080