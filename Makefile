build:
	sudo docker build -t fastapi-template .

run:
	sudo docker run --rm -it -p 8080:80 fastapi-template

dev: 
	fastapi dev app/main.py