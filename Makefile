package_name = repository_telegram_bot
repository = toolen/repository-telegram-bot
version = $(shell poetry version -s)
tag = $(repository):$(version)

pre-commit:
	poetry run black .
	poetry run isort .
	poetry run flake8 --ignore E501 $(package_name)/ tests/
	poetry run mypy $(package_name)
	poetry run pydocstyle --add-ignore=D104 $(package_name)/
	poetry run pytest --cov=$(package_name) tests/
	poetry run bandit -r $(package_name)
	poetry run safety check
	poetry run radon cc $(package_name)
	poetry run radon mi $(package_name)
	poetry run radon raw $(package_name)
	poetry run radon hal $(package_name)
pydocstyle:
	poetry run pydocstyle --add-ignore=D104 $(package_name)/
test:
	poetry run pytest --cov=$(package_name) tests/
image:
	docker build -t $(tag) .
size:
	docker images | grep $(repository) | grep $(version)
scan:
	trivy image $(tag)
push:
	docker trust sign $(tag)
ngrok:
	ngrok http 8080