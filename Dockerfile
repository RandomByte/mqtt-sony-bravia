FROM python:3.10.7-alpine

WORKDIR /project

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

CMD [ "python", "./main.py" ]
