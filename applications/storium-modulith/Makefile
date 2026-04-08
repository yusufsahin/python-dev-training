.PHONY: run migrate shell test superuser static reset-db seed docker-up docker-down docker-logs docker-ps

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

shell:
	python manage.py shell

test:
	python manage.py test

superuser:
	python manage.py createsuperuser

static:
	python manage.py collectstatic --noinput

seed:
	python manage.py seed_catalog

seed-demo-user:
	python manage.py seed_catalog --with-demo-user

reset-db:
	python manage.py flush --noinput
	python manage.py migrate
	python manage.py createsuperuser

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f web

docker-ps:
	docker compose ps
