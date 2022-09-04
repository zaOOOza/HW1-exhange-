FROM python:3.10.4

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY . /app
EXPOSE 5000

CMD ["python", "app.py"]
