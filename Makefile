shell:
	python manage.py shell


docker-run:
	docker run -it -p 8030:8030 padelanalytics


docker-build:
	docker build . -f ./Dockerfile -t padelanalytics


docker-tag:
	docker tag padelanalytics paconte/padelanalytics:$(VERSION)


docker-push:
	# make docker-push VERSION=0.0.2
	docker push paconte/padelanalytics:$(VERSION)


runserver:
	python3 manage.py runserver


delete_db:
	rm padelanalytics/db.sqlite3


setup:
	rm -rf .venv ; \
	python3 -m venv .venv/padel ; \
	source ./.venv/padel/bin/activate ; \
	pip install --upgrade pip && pip install -r requirements.txt


lint:
	ruff check --select I --fix .


format: lint
	ruff format .


mypy: format
	mypy ./tournaments --explicit-package-bases
