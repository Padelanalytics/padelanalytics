FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /django-padel
WORKDIR /django-padel
COPY requirements_production.txt /django-padel
RUN pip install --upgrade pip
RUN pip install -r requirements_production.txt
COPY . /django-padel/
