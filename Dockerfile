FROM python:3.7-slim-buster

COPY requirements.txt /dashboard_app/

WORKDIR /dashboard_app

RUN pip install -r requirements.txt

COPY . /dashboard_app/

ENTRYPOINT ["python", "app.py"]