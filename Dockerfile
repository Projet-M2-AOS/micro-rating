FROM python:3.10.0-alpine3.14

ENV PYTHONPATH "${PYTHONPATH}:/code"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 3005

CMD ["python", "app/main.py"]