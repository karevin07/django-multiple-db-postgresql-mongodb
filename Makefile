IMAGE_NAME=mydjango
PROJECT_NAME=myproject

EXAMPLE_APP=example

##@ Build image
.PHONY: build-django-image
build-django-image: ## Build django image
	docker build -t $(IMAGE_NAME) -f django/Dockerfile .

##@ Django start project and start app
.PHONY: start-project start-application
start-project: ## Start project
	docker-compose run --rm django django-admin startproject $(PROJECT_NAME) .

start-application: ## Start example app
	docker-compose run --rm django python manage.py startapp $(EXAMPLE_APP)_user
	docker-compose run --rm django python manage.py startapp $(EXAMPLE_APP)_app

##@ Django data migrate
.PHONY: migrate-db

migrate-db:| migrate-admin migrate-auth migrate-contenttypes migrate-sessions migrate-user migrate-app ## migrate all db

migrate-all:| migrate-db make-migrate

make-migrate: ## Make migrations
	docker-compose run --rm django python manage.py makemigrations --settings=myproject.multiple_db_settings

migrate-admin: ## Migrate admin table
	docker-compose run --rm django python manage.py migrate admin --database=default --settings=myproject.multiple_db_settings

migrate-auth: ## Migrate auth table
	docker-compose run --rm django python manage.py migrate auth --database=default --settings=myproject.multiple_db_settings

migrate-contenttypes: ## Migrate contenttypes table
	docker-compose run --rm django python manage.py migrate contenttypes --database=default --settings=myproject.multiple_db_settings

migrate-sessions: ## Migrate sessions table
	docker-compose run --rm django python manage.py migrate sessions --database=default --settings=myproject.multiple_db_settings

migrate-user: ## Migrate user table
	docker-compose run --rm django python manage.py migrate example_user --database=default --settings=myproject.multiple_db_settings

migrate-app: ## Migrate app table
	docker-compose run --rm django python manage.py migrate example_app --database=mongo_db --settings=myproject.multiple_db_settings

##@ Django create superuser
.PHONY: create-superuser
create-superuser-local: ## Create superuser
	docker-compose run --rm django python manage.py createsuperuser --database=default  --settings=myproject.multiple_db_settings

##@ Debug
.PHONY: restart-django show-env kill-container

show-env: ## Show env
	cat example_env

kill-container: ## Kill stop containers
	docker rm -f $$(docker ps -a -q  --filter "status=exited")

##@ Jupyerlab with Django
.PHONY: run-jupyter-with-django kill-jupyter-django

kill-jupyter-django: ## Kill jupyterlab-django containers
	docker rm -f $$(docker ps -a -q  --filter "name=jupyterlab-django")

run-jupyter-with-django: ## Run jupyterlab with django kernel
	docker-compose run -d -p 8888:8888 --name jupyterlab-django -v ./notebooks:/home/notebooks django python manage.py shell_plus --notebook --settings=myproject.multiple_db_settings
	sleep 5
	echo $$(docker logs --tail 3 jupyterlab-django)

##@ Help
.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help