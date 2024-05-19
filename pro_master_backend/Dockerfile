FROM python:3.10

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN python manage.py collectstatic

RUN cp -r collected_static/* static

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "pro_master_backend.wsgi"]
