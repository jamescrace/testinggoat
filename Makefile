IMAGE_NAME := superlists
PORT := 8888

build:
	docker build -t $(IMAGE_NAME) .

run: build
	docker run \
		-p $(PORT):$(PORT) \
		--mount type=bind,source="$(PWD)/src/db.sqlite3",target=/src/db.sqlite3 \
		-it $(IMAGE_NAME)

test: build
	docker run \
		--mount type=bind,source="$(PWD)/src/db.sqlite3",target=/src/db.sqlite3 \
		-it $(IMAGE_NAME) \
		python manage.py test

ft:
	TEST_SERVER=localhost:$(PORT) python src/manage.py test functional_tests --failfast
