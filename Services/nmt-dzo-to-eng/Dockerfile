FROM python:3.12

WORKDIR /nmt-dzo-to-eng

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 app:app