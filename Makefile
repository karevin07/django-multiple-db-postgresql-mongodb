IMAGE_NAME=mydjango
PROJECT_NAME=myproject

EXAMPLE_APP=example

.PHONY: build-django-image

build-django-image: ## build django image
	docker build -t $(IMAGE_NAME) -f django/Dockerfile .

##@ Debug Django
.PHONY: run-django-container test-django-container kill-django-container

run-django-container: ## run django container for test
	docker run --name $(IMAGE_NAME) -it $(IMAGE_NAME)  /bin/bash

test-django-container: ## run django container for test with docker-compose run
	docker-compose run django /bin/bash

kill-django-container: ## kill django containers
	docker rm -f $$(docker ps -a -q  --filter "status=exited")

##@ Django start project and start app
.PHONY: start-project start-application

start-project: ## Start project
	docker-compose run django django-admin startproject $(PROJECT_NAME) .

start-application: ## Start example app
	docker-compose run django python manage.py startapp $(EXAMPLE_APP)_user
	docker-compose run django python manage.py startapp $(EXAMPLE_APP)_app

.PHONY: migrate-db

migrate-db:| migrate-admin migrate-auth migrate-contenttypes migrate-sessions migrate-user migrate-app

make-migrate:
	docker-compose run django python manage.py makemigrations --settings=myproject.multiple_db_settings

migrate-admin:
	docker-compose run django python manage.py migrate admin --database=default --settings=myproject.multiple_db_settings

migrate-auth:
	docker-compose run django python manage.py migrate auth --database=default --settings=myproject.multiple_db_settings

migrate-contenttypes:
	docker-compose run django python manage.py migrate contenttypes --database=default --settings=myproject.multiple_db_settings

migrate-sessions:
	docker-compose run django python manage.py migrate sessions --database=default --settings=myproject.multiple_db_settings

migrate-user:
	docker-compose run django python manage.py migrate example_user --database=default --settings=myproject.multiple_db_settings

migrate-app:
	docker-compose run django python manage.py migrate example_app --database=mongo_db --settings=myproject.multiple_db_settings

.PHONY: create-superuser
create-superuser-local: ## Create superuser
	docker-compose run django python manage.py createsuperuser --database=default  --settings=myproject.multiple_db_settings

.PHONY: help
##@ Help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help