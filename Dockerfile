FROM docker.io/python:3.13-slim

WORKDIR /service

COPY ./pyproject.toml .
COPY ./README.md .
RUN pip install --no-cache-dir -e .


COPY app /service/app
RUN python -m compileall .

CMD ["fastapi", "run", "app/main.py", "--port", "80"]