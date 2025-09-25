FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# COPY sub.py sub.py
COPY sub_timescale.py sub_timescale.py

# CMD [ "python", "-u", "sub.py" ]
CMD [ "python", "-u", "sub_timescale.py" ]
