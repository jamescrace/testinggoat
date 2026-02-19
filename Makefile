IMAGE_NAME := superlists
PORT := 8888
DJANGO_SECRET_KEY ?= secret-key-for-local-docker

container.db.sqlite3:
	touch container.db.sqlite3
	sudo chown 1234 container.db.sqlite3
	sudo chmod g+rw container.db.sqlite3

build:
	docker build -t $(IMAGE_NAME) .

run: container.db.sqlite3 build
	docker run \
		-p $(PORT):$(PORT) \
		-e DJANGO_SECRET_KEY=DJANGO_SECRET_KEY \
		-e DJANGO_ALLOWED_HOST=localhost \
		-e DJANGO_DB_PATH=/home/nonroot/db.sqlite3 \
		--mount type=bind,source="$(PWD)/container.db.sqlite3",target=/home/nonroot/db.sqlite3 \
		-it $(IMAGE_NAME)

test: container.db.sqlite3 build
	docker run \
		-e DJANGO_SECRET_KEY=DJANGO_SECRET_KEY \
		-e DJANGO_ALLOWED_HOST=localhost \
		-e DJANGO_DB_PATH=/home/nonroot/db.sqlite3 \
		--mount type=bind,source="$(PWD)/container.db.sqlite3",target=/home/nonroot/db.sqlite3 \
		-it $(IMAGE_NAME) \
		python manage.py test

ft:
	TEST_SERVER=localhost:$(PORT) python src/manage.py test functional_tests --failfast
