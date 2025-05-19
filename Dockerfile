FROM docker.io/python:3.13-slim

RUN apt update -y && apt install -y libpq-dev python3-dev gcc && apt clean
WORKDIR /service

COPY ./pyproject.toml .
COPY ./README.md .
RUN pip install --no-cache-dir -e .


COPY app /service/app
RUN python -m compileall .

CMD ["uvicorn", "app.main:create_app", "--factory", "--port", "80", "--host", "0.0.0.0"]