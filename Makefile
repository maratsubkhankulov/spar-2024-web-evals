IMAGE_NAME := akkadeeemikk/agent-web-eval
DOCKER_TAG := latest

build:
	docker build -f docker/app/Dockerfile -t $(IMAGE_NAME) docker/app/.
  		
run_agent:
	docker compose up -d
  		
jupyter:
	jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=agent

stop:
	docker compose down

create_env:
	cp .env_template .env

linter:
	flake8 .


