# Variables
VENV = . venv/bin/activate;

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
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-rebuild:
	docker-compose up --build -d
