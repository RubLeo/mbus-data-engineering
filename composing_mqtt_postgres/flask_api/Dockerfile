FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.app

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
