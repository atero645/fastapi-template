WRK ?= wrk
HOST ?= http://localhost:8000
SCRIPT ?= ./benchmarks/user_random_id.lua
DURATION ?= 30s
CONNECTIONS ?= 50
THREADS ?= 4


VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := . $(VENV_DIR)/bin/activate

.PHONY: venv install test clean

venv:
	if [ ! -d $(VENV_DIR) ]; then python3 -m venv $(VENV_DIR); fi

install: venv
	$(PIP) install -e .[dev]

build:
	docker build -t fastapi-template .

run:
	docker run --rm -it -p 8080:80 fastapi-template

dev: 
	uvicorn app.main:create_app --factory --reload

start: 
	uvicorn app.main:create_app --factory

benchmark:
	$(WRK) -t$(THREADS) -c$(CONNECTIONS) -d$(DURATION) -s $(SCRIPT) $(HOST)

test: venv
	$(PYTHON) -m pytest

seed-users:
	$(PYTHON) ./seeders/users_seeder.py

clean:
	rm -rf $(VENV_DIR)