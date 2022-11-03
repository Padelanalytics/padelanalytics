shell:
	python manage.py shell


linters:
	black . && flake8 --config .flake8


docker-run:
	docker run -it -p 8030:8030 padelanalytics


docker-build:
	docker build . -f ./Dockerfile -t padelanalytics


runserver:
	python manage.py runserver


delete_db:
	rm padelanalytics/db.sqlite3


setup:
	rm -rf .venv ; \
	python3 -m venv .venv/padel ; \
    . ./.venv/padel/bin/activate ; \
    pip install --upgrade pip && pip install -r requirements.txt
