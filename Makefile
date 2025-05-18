WRK ?= wrk
HOST ?= http://localhost:8000
SCRIPT ?= ./benchmarks/user_random_id.lua
DURATION ?= 30s
CONNECTIONS ?= 50
THREADS ?= 4

build:
	sudo docker build -t fastapi-template .

run:
	sudo docker run --rm -it -p 8080:80 fastapi-template

dev: 
	fastapi dev app/main.py

benchmark:
	$(WRK) -t$(THREADS) -c$(CONNECTIONS) -d$(DURATION) -s $(SCRIPT) $(HOST)
