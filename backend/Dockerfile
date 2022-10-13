FROM python:3.7-slim
RUN mkdir /app
COPY . /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app/foodgram
RUN python3 manage.py makemigrations
RUN python3 manage.py collectstatic --no-input
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "backend:8000"]
