FROM python:3.13-alpine

WORKDIR /app
COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./main.py /app/main.py

CMD ["python3", "-u", "main.py"]