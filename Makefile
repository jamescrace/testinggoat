IMAGE_NAME := superlists
PORT := 8888
DB_FILE := container.db.sqlite3
DB_TARGET := /home/nonroot/db.sqlite3

DOCKER_RUN := docker run \
	-e DJANGO_SECRET_KEY=DJANGO_SECRET_KEY \
	-e DJANGO_ALLOWED_HOST=localhost \
	-e DJANGO_DB_PATH=$(DB_TARGET) \
	--mount type=bind,source="$(PWD)/$(DB_FILE)",target=$(DB_TARGET)

$(DB_FILE):
	touch $(DB_FILE)
	sudo chown 1234 $(DB_FILE)
	sudo chmod g+rw $(DB_FILE)

build:
	docker build -t $(IMAGE_NAME) .

run: $(DB_FILE) build
	$(DOCKER_RUN) -p $(PORT):$(PORT) -it $(IMAGE_NAME)

migrate: $(DB_FILE) build
	$(DOCKER_RUN) -it $(IMAGE_NAME) python manage.py migrate

test: $(DB_FILE) build
	$(DOCKER_RUN) -it $(IMAGE_NAME) python manage.py test

ft:
	TEST_SERVER=localhost:$(PORT) python src/manage.py test functional_tests --failfast
