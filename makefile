# Variables
VENV = . venv/bin/activate;

# Load environment variables
include .env
export $(shell sed 's/=.*//' .env)

# Backend Commands
run:
	$(VENV) uvicorn app.main:app --reload

install:
	$(VENV) pip install -r requirements.txt

freeze:
	$(VENV) pip freeze > requirements.txt

lint:
	$(VENV) flake8 app

test:
	$(VENV) pytest

format:
	$(VENV) black app

# Docker Commands
docker-up:
	# Start the containers with ports from .env
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-rebuild:
	# Rebuild containers with ports from .env
	docker-compose up --build -d
