shell:
	python manage.py shell


linters:
	black . && flake8 --config .flake8


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
	python manage.py runserver


delete_db:
	rm padelanalytics/db.sqlite3


setup:
	rm -rf .venv ; \
	python3 -m venv .venv/padel ; \
    . ./.venv/padel/bin/activate ; \
    pip install --upgrade pip && pip install -r requirements.txt
